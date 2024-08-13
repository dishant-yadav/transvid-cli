# ffmpeg_worker.py
import ffmpeg
import json
import datetime
import video_qualities
import os

def convert_seconds_to_hh_mm_ss(seconds):
        seconds=float(seconds)
        # Use timedelta to convert seconds to a duration
        duration = str(datetime.timedelta(seconds=seconds))
        
        # Format the duration to hh:mm:ss
        if '.' in duration:
            duration = duration.split('.')[0]  # Remove microseconds if they exist
        return duration

def transcode_v1(input_file, output_file):
    ffmpeg.input(input_file).output(output_file).run()

def transcode(input_file, output_dir, bitrate, quality):
    try:
        # Use ffmpeg to transcode the video
        file_name = f"{quality}.m3u8"
        output_file = os.path.join(output_dir, file_name)
        ffmpeg.input(input_file).output(
            output_file, 
            format='hls',
            video_bitrate=f"{bitrate}k",
            hls_time=10,  # Duration of each segment in seconds
            hls_playlist_type='vod',  # Video on demand
            hls_segment_filename=os.path.join(output_dir, f"{quality}_%05d.ts"),
            vcodec='libx264',
            acodec='aac',
            preset='fast',
            g=30,  # fps
        ).run()
        print(f"Transcoding to HLS completed: {output_file}")
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf8')}")
        return None
    
    return output_file


def generate_thumbnail_v1(input_file, output_file, timestamp="00:00:10"):
    (ffmpeg.input(input_file, ss=timestamp).output(output_file, vframes=1).run())
    
def generate_thumbnail(input_file, output_dir, timestamp="00:00:10"):
    file_name = "thumbnail.jpg"
    output_file = os.path.join(output_dir, file_name)
    (ffmpeg.input(input_file, ss=timestamp).output(output_file, vframes=1).run())



def get_quality_and_duration(path):
    try:
        # Use ffprobe to get video information
        probe = ffmpeg.probe(path)
        
        # Extract format information
        format_info = probe['format']
        
        # Extract bitrate and duration
        quality = format_info.get('bit_rate', None)
        duration = format_info.get('duration', None)
        
        if quality is not None:
            bitrate = int(quality) / 1000  # Convert to kbps
            quality= video_qualities.bitrate_to_quality(bitrate)

        
        if duration is not None:
            duration = convert_seconds_to_hh_mm_ss(duration)
        
        return quality, duration
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf8')}")
        return None, None


def extract_metadata_v1(input_file, output_file): # output file=abc_metadata.json
    probe = ffmpeg.probe(input_file)
    print(probe)
    with open(f'{output_file}', 'w') as json_file:
        json.dump(probe, json_file, indent=4)

    return probe

def extract_metadata(input_file, output_dir): # output file=metadata.json
    probe = ffmpeg.probe(input_file)
    file_name='metadata.json'

    output_file=os.path.join(output_dir, file_name)
    with open(f'{output_file}', 'w') as json_file:
        json.dump(probe, json_file, indent=4)

    return probe


if __name__ == "__main__":
    # Example usage:
    quality, duration= get_quality_and_duration("input.mp4")
    print(f"Quality: {quality}")
    print(f"Duration: {duration}")


