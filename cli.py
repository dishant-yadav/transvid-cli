# cli.py
import click
from rq import Queue
from redis import Redis
from tasks import simple_task
from ffmpeg_worker import transcode, transcode_v1, extract_metadata_v1, extract_metadata, generate_thumbnail_v1, generate_thumbnail, get_quality_and_duration
import video_qualities
from upload_to_s3 import upload_to_s3
import db_actions
from pathlib import Path


redis_conn = Redis()
q = Queue(connection=redis_conn)


@click.group()
def cli():
    pass


@cli.command()
def test():
    click.echo("CLI setup works!")


@cli.command()
def enqueue_task():
    q.enqueue(simple_task)
    click.echo("Task enqueued")


@cli.command()
@click.argument("input")
@click.argument("output_file")
def transcode_video(input, output_file):
    transcode_v1(input, output_file)
    click.echo(f"Transcoded {input} to {output_file}")
    upload_to_s3(f"{input}_transcoded.mp4", "video-transcoding-temp-1", f"{input}_transcoded.mp4")
    click.echo(f"Uploaded {output_file} to S3")


@cli.command()
@click.argument("input")
def enqueue_transcode(input):
    transcode_job= q.enqueue(transcode_v1, input, f"{input}_transcoded.mp4")
    click.echo(f"Transcoding task enqueued for {input}")
    q.enqueue(upload_to_s3,f"{input}_transcoded.mp4", "video-transcoding-temp-1", f"{input}_transcoded.mp4", depends_on=transcode_job)
    click.echo(f"Uploaded transcoded video {input}_transcoded.mp4 to S3")


@cli.command()
@click.argument("input")
def enqueue_metadata(input):
    output_file = f"{input}_metadata.json"
    metadata_job= q.enqueue(extract_metadata_v1, input, output_file)
    click.echo(f"Metadata extraction task enqueued for {input}")
    q.enqueue(upload_to_s3, output_file, "video-metadata-temp-1", output_file, depends_on=metadata_job)
    click.echo(f"Uploaded metadata {output_file} to S3")


@cli.command()
@click.argument("input")
@click.argument("timestamp", default="00:00:10")
def enqueue_thumbnail(input, timestamp):
    output_file = f"{input}_thumbnail.png"
    thumbnail_job=q.enqueue(generate_thumbnail_v1, input, output_file, timestamp)
    click.echo(f"Thumbnail generation task enqueued for {input}")
    q.enqueue(upload_to_s3, output_file, "video-thumbnail-temp-1", output_file, depends_on=thumbnail_job)
    click.echo(f"Uploaded thumbnail {output_file} to S3")

# @cli.command()
# @click.argument("input")
# def enqueue_all(input):
#     transcode_job= q.enqueue(transcode, input, f"{input}_transcoded.mp4")
#     metadata_job= q.enqueue(extract_metadata, input, f"{input}_metadata.json")
#     thumbnail_job=q.enqueue(generate_thumbnail, input, f"{input}_thumbnail.png")
#     click.echo(f"All tasks enqueued for {input}")
#     q.enqueue(upload_to_s3, f"{input}_transcoded.mp4", "video-transcoding-temp-1", f"{input}_transcoded.mp4", depends_on=transcode_job)
#     q.enqueue(upload_to_s3, f"{input}_metadata.json", "video-metadata-temp-1", f"{input}_metadata.json", depends_on=metadata_job)
#     q.enqueue(upload_to_s3, f"{input}_thumbnail.png", "video-thumbnail-temp-1", f"{input}_thumbnail.png", depends_on=thumbnail_job)
#     click.echo(f"Uploaded transcoded video {input}_transcoded.mp4, metadata {input}_metadata.json, and thumbnail {input}_thumbnail.png to S3")


@cli.command()
@click.argument("input")
@click.option('--quality',
              type=click.Choice(video_qualities.QUALITY_CHOICES),
              multiple=True,
              help='List of video qualities to transcode. Currently supported: 1080p, 720p, 480p, 360p, 240p')
@click.option('--caption', is_flag=True, help='Generate captions for the video')
@click.option('--thumbnail', is_flag=True, help='Generate thumbnail for the video')
@click.option('--summary', is_flag=True, help='Generate summary for the video')
def enqueue_all(input, quality, caption, thumbnail, summary):

    vid_qual, length= get_quality_and_duration(input)

    # consts
    title= "Video Title"
    description= "Video Description"

    print(f"title: {title}")
    print(f"summary: {summary}")
    print(f"caption: {caption}")
    print(f"thumbnail: {thumbnail}")
    print(f"length: {length}")
    print(f"description: {description}")

    # create video in db
    video= db_actions.create_video(title, summary, caption, thumbnail, length, description)
    video_id= video[0]["id"]

    # Create a folder: video_id
    wd= Path.cwd()
    output_dir= f"{wd}/{video_id}"

    Path(output_dir).mkdir()

    selected_qualities = video_qualities.get_available_qualities(vid_qual, quality)

    # transcode
    transcode_job=[]
    for qual in selected_qualities:
        # transcode in this quality
        click.echo(f"Quality: {qual['quality']}, Bitrate: {qual['bitrate']}")
        q_job= q.enqueue(transcode, input, output_dir, qual['bitrate'], qual['quality'])
        transcode_job.append(q_job)

    # metadata
    metadata_job= q.enqueue(extract_metadata, input, output_dir)

    # thumbnail
    thumbnail_job= q.enqueue(generate_thumbnail, input, output_dir)


if __name__ == "__main__":
    cli()
