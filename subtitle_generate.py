import subprocess
import os
import ffmpeg_worker


def generate_subtitle(input_file, output_dir):
    command = [
        "auto_subtitle",
        input_file,
        "--model",
        "tiny",
        "--srt_only",
        "true",
        "--output_dir",
        output_dir
    ]

    try:    
        res = subprocess.run(command, capture_output=True, text=True)
        if res.returncode == 0:
            print("Subtitle generation completed")
            l = input_file.split('.')
            l.pop()
            file_name = '.'.join(l)
            ip_file=file_name+".srt"
            ffmpeg_worker.convert_srt_to_vtt(ip_file, output_dir)
        else:
            print(res.returncode)
            raise RuntimeError("Subtitle generation failed")
    except subprocess.CalledProcessError as e:
        print("Subtitle generation failed")
        print("Error:", e.stderr)

    
    # change the model to medium or high based on pc compute power
    # add support for translation
