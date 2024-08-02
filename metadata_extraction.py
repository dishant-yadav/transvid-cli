# metadata_extraction.py
import ffmpeg


def extract_metadata(input_file):
    probe = ffmpeg.probe(input_file)
    print(probe)
    return probe
