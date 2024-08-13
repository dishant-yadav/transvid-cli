import subprocess


def generate_subtitle(input_file):
    command = [
        "auto_subtitle",
        # "--file",
        input_file,
        "--model",
        "tiny",
        "--srt_only",
        "True",
    ]

    res = subprocess.run(command, capture_output=True, text=True)
    if res.returncode == 0:
        print("Subtitle generation completed")
    else:
        print("Subtitle generation failed")
    # change the model to medium or high based on pc compute power
    # add support for translation
