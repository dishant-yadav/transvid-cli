from typing import List, Dict

QUALITIES = [
    { "quality": "2160p", "bitrate": 15000},
    { "quality": "1080p", "bitrate": 8000 },
    { "quality": "720p", "bitrate": 5000 },
    { "quality": "480p", "bitrate": 1500 },
    { "quality": "360p", "bitrate": 500 },
    { "quality": "240p", "bitrate": 200 },
    { "quality": "144p", "bitrate": 100 }
]


QUALITY_CHOICES = [q['quality'] for q in QUALITIES]


def bitrate_to_quality(bitrate):
    # bitrates are in kbps
    if bitrate >= 15000:
        return '2160p'
    elif bitrate >= 8000:
        return '1080p'
    elif bitrate >= 5000:
        return '720p'
    elif bitrate >= 1500:
        return '480p'
    elif bitrate >= 500:
        return '360p'
    elif bitrate >= 200:
        return '240p'
    else:
        return '144p'


def get_all_compatible_quality(quality):
    bitrate=0
    for i, q in enumerate(QUALITIES):
        if q['quality'] == quality:
            bitrate=q['bitrate']
    
    ans=[]
    for i, q in enumerate(QUALITIES):
        if q['bitrate'] <= bitrate:
            ans.append(q["quality"])
    return ans

def get_available_qualities(video_quality: str, quality_desired: tuple,)-> List[Dict[str, str]]:
    quality_desired=list(set(quality_desired))
    if video_quality not in quality_desired:
        quality_desired.append(video_quality)
    
    available_quality= get_all_compatible_quality(video_quality)

    final_qualities= [q for q in quality_desired if q in available_quality]

    return [q for q in QUALITIES if q['quality'] in final_qualities]