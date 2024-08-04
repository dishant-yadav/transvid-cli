# metadata_extraction.py
import ffmpeg
import json

def extract_metadata(input_file, output_file): # output file=abc_metadata.json
    probe = ffmpeg.probe(input_file)
    print(probe)
    with open(f'{output_file}', 'w') as json_file:
        json.dump(probe, json_file, indent=4)

    return probe
