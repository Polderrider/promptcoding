from app.db import get_connection
from pprint import pprint
import json



def insert_video(cur, video_id, url, title, transcript):
    print(f"transcript: {type(transcript)}")
    pprint(transcript)


    cur.execute("""
        INSERT INTO videos (youtube_video_id, youtube_url, title, transcript_text, transcript_segments)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (youtube_video_id) DO NOTHING
        RETURNING id
    """, (
        video_id, 
        url, 
        title, 
        transcript["text"], 
        json.dumps(transcript["segments"])          # SNIPPETS postgres-doesn’t-auto-convert-list/dicts-to-JSON
    ))

    result = cur.fetchone()
    if result is None:
        print("Video already exists, skipping")
        return
    video_db_id = result[0]

    return video_db_id


def insert_noun(cur, video_db_id, noun):
    cur.execute("""
        INSERT INTO nouns (video_id, source_word, english_translation, frequency)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (video_db_id, noun["source"], noun["translation"], noun["frequency"]))

    return cur.fetchone()[0]


def insert_question(cur, video_id, noun_id, q):
    cur.execute("""
        INSERT INTO questions (video_id, noun_id, question_text,
        correct_answer, option_a, option_b, option_c, option_d)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        video_id,
        noun_id,
        q["question_text"],
        q["correct_answer"],
        q["options"][0],
        q["options"][1],
        q["options"][2],
        q["options"][3],
    ))