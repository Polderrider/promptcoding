import feedparser

from app.transcript import extract_video_id, fetch_transcript
from app.nlp import extract_nouns
from app.translate import translate_nouns
from app.questions import generate_mcq
from app.store_in_db import insert_video, insert_noun, insert_question
from app.db import get_connection

import os
print("CWD:", os.getcwd())
print("SCRIPT RUNNING")

feed_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCch2JvY2ZSwcjf5gb93HGQw"

feed = feedparser.parse(feed_url)
latest = feed.entries[0]

video_id = latest.yt_videoid
title = latest.title
url = latest.link
print("video_id:", latest.yt_videoid)
print("title:", latest.title)
print("url:", latest.link)

transcript = fetch_transcript(video_id)

nouns = extract_nouns(transcript["text"])
translated = translate_nouns(nouns)

with get_connection() as conn:
    with conn.cursor() as cur:
        video_db_id = insert_video(cur, video_id, url, title, transcript)

        if video_db_id is None:
            conn.commit()
            print("Skipped duplicate video")
            exit()


        for noun in translated:
            noun_id = insert_noun(cur, video_db_id, noun)
            q = generate_mcq(noun, translated)
            insert_question(cur, video_db_id, noun_id, q)

    conn.commit()

print(f"Video processed: {title}")