# cli.py
import click
from rq import Queue
from redis import Redis
from tasks import simple_task
from ffmpeg_transcode import transcode
from metadata_extraction import extract_metadata
from thumbnail_generation import generate_thumbnail

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


@cli.command()
@click.argument("input")
def enqueue_transcode(input):
    q.enqueue(transcode, input, f"{input}_transcoded.mp4")
    click.echo(f"Transcoding task enqueued for {input}")


@cli.command()
@click.argument("input")
def enqueue_metadata(input):
    q.enqueue(extract_metadata, input)
    click.echo(f"Metadata extraction task enqueued for {input}")


@cli.command()
@click.argument("input")
@click.argument("timestamp", default="00:00:10")
def enqueue_thumbnail(input, timestamp):
    output_file = f"{input}_thumbnail.png"
    q.enqueue(generate_thumbnail, input, output_file, timestamp)
    click.echo(f"Thumbnail generation task enqueued for {input}")


if __name__ == "__main__":
    cli()
