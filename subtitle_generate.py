import subprocess
import os

def generate_subtitle(input_file, output_dir):
    file_name = "caption.vtt"
    output_file = os.path.join(output_dir, file_name)

    command = [
        "auto_subtitle",
        # "--file",
        input_file,
        "--model",
        "tiny",
        "--srt_only",
        "True",
        "--output",
        output_file,
        "--format",
        "vtt"
    ]

    try:    
        res = subprocess.run(command, capture_output=True, text=True)
        if res.returncode == 0:
            print("Subtitle generation completed")
        else:
            raise RuntimeError("Subtitle generation failed")
    except subprocess.CalledProcessError as e:
        print("Subtitle generation failed")
        print("Error:", e.stderr)

    
    # change the model to medium or high based on pc compute power
    # add support for translation
