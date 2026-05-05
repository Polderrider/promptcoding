from app.transcript import extract_video_id, fetch_transcript
from app.nlp import extract_nouns
from app.translate import translate_nouns
from app.questions import generate_mcq
from app.db import get_connection
from app.store_in_db import insert_video, insert_noun, insert_question


url = "https://www.youtube.com/watch?v=aZ8HgiV_4y8&t=247s"        # nos 


video_id = extract_video_id(url)
transcript = fetch_transcript(video_id)

nouns = extract_nouns(transcript["text"])
translated = translate_nouns(nouns)

with get_connection() as conn:
    with conn.cursor() as cur:
        video_db_id = insert_video(cur, video_id, url, "test title", transcript)

        for noun in translated:
            noun_id = insert_noun(cur, video_db_id, noun)
            q = generate_mcq(noun, translated)
            insert_question(cur, video_db_id, noun_id, q)

    conn.commit()