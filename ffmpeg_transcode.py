# ffmpeg_transcode.py
import ffmpeg


def transcode(input_file, output_file):
    ffmpeg.input(input_file).output(output_file).run()
