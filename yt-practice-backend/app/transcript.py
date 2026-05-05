from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs




def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query).get("v", [None])[0]
    elif "youtu.be" in parsed.netloc:
        return parsed.path.strip("/")
    return None


def fetch_transcript(video_id: str):
    ytt_api = YouTubeTranscriptApi()
    fetched = ytt_api.fetch(video_id, languages=["nl"])

    segments = [
        {
            "text": item.text,
            "start": item.start,
            "duration": item.duration,
        }
        for item in fetched
    ]

    full_text = " ".join(item["text"] for item in segments)

    return {
        "text": full_text,
        "segments": segments,
    }