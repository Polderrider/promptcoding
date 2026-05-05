from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import re



def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query).get("v", [None])[0]
    elif "youtu.be" in parsed.netloc:
        return parsed.path.strip("/")
    return None


def create_sentences(snippets): 
    
    full_transcript = ""
    # combine snippet text into full transcript
    for item in snippets:
        full_transcript = full_transcript + " " + item.text

    print(f"full_transcript: {full_transcript}")

    # split full text into sentences
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', full_transcript)
    return [s.strip() for s in sentences if s.strip()]
    
    # optionally approximate sentence start time from the first snippet that contributed to it



def fetch_transcript(video_id: str):
    ytt_api = YouTubeTranscriptApi()
    fetched = ytt_api.fetch(video_id, languages=["nl"])
    sentences = create_sentences(fetched)
    # print(f"fetched list: {fetched}")

    # segments = [
    #     {
    #         "text": item.text,
    #         "start": item.start,
    #         "duration": item.duration,
    #     }
    #     for item in fetched
    # ]

    full_text = " ".join(item for item in sentences)
    # full_text = " ".join(item["text"] for item in segments)

    return {
        "text": full_text,
        "sentences": sentences,
    }