time ffmpeg -i input.mp4 -y -loglevel warning -acodec aac -vcodec libx264 -filter:v scale=w=1920:h=1080 -f mp4 video-1080p.mp4
