# thumbnail_generation.py
import ffmpeg


def generate_thumbnail(input_file, output_file, timestamp="00:00:10"):
    (ffmpeg.input(input_file, ss=timestamp).output(output_file, vframes=1).run())
