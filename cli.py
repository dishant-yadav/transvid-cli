# cli.py
import click
from rq import Queue
from redis import Redis
from tasks import simple_task
from ffmpeg_transcode import transcode
from metadata_extraction import extract_metadata
from thumbnail_generation import generate_thumbnail
from upload_to_s3 import upload_to_s3
from subtitle_generate import generate_subtitle

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
    transcode(input, output_file)
    click.echo(f"Transcoded {input} to {output_file}")
    upload_to_s3(
        f"{input}_transcoded.mp4", "video-transcoding-temp-1", f"{input}_transcoded.mp4"
    )
    click.echo(f"Uploaded {output_file} to S3")


@cli.command()
@click.argument("input")
def enqueue_transcode(input):
    transcode_job = q.enqueue(transcode, input, f"{input}_transcoded.mp4")
    click.echo(f"Transcoding task enqueued for {input}")
    q.enqueue(
        upload_to_s3,
        f"{input}_transcoded.mp4",
        "video-transcoding-temp-1",
        f"{input}_transcoded.mp4",
        depends_on=transcode_job,
    )
    click.echo(f"Uploaded transcoded video {input}_transcoded.mp4 to S3")


@cli.command()
@click.argument("input")
def enqueue_metadata(input):
    output_file = f"{input}_metadata.json"
    metadata_job = q.enqueue(extract_metadata, input, output_file)
    click.echo(f"Metadata extraction task enqueued for {input}")
    q.enqueue(
        upload_to_s3,
        output_file,
        "video-metadata-temp-1",
        output_file,
        depends_on=metadata_job,
    )
    click.echo(f"Uploaded metadata {output_file} to S3")


@cli.command()
@click.argument("input")
@click.argument("timestamp", default="00:00:10")
def enqueue_thumbnail(input, timestamp):
    output_file = f"{input}_thumbnail.png"
    thumbnail_job = q.enqueue(generate_thumbnail, input, output_file, timestamp)
    click.echo(f"Thumbnail generation task enqueued for {input}")
    q.enqueue(
        upload_to_s3,
        output_file,
        "video-thumbnail-temp-1",
        output_file,
        depends_on=thumbnail_job,
    )
    click.echo(f"Uploaded thumbnail {output_file} to S3")


@cli.command()
@click.argument("input")
def enqueue_subtitle(input):
    subtitle_job = q.enqueue(generate_subtitle, input)
    click.echo(f"Subtitle generation task enqueued for {input}")
    # q.enqueue(upload_to_s3,f"{input}_transcoded.mp4", "video-transcoding-temp-1", f"{input}_transcoded.mp4", depends_on=subtitle_job)
    click.echo(f"Subtitle generated for video {input}")
    # mp4 to S3")


if __name__ == "__main__":
    cli()
