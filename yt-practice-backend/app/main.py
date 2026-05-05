from fastapi import FastAPI, HTTPException
from app.db import get_connection
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="YouTube Language Practice API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnswerSubmission(BaseModel):
    question_id: int
    selected_answer: str



@app.get("/")
def root():
    return {"status": "ok", "app": "YouTube Language Practice API"}


@app.get("/health/db")
def db_health():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()

    return {"database": "ok", "result": result[0]}


@app.get("/latest-video")
def get_latest_video():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, youtube_video_id, youtube_url, title, channel_name, thumbnail_url
                FROM videos
                ORDER BY created_at DESC
                LIMIT 1;
            """)
            video = cur.fetchone()

            if not video:
                raise HTTPException(status_code=404, detail="No videos found")

            video_id = video[0]

            cur.execute("""
                SELECT id, question_text, option_a, option_b, option_c, option_d
                FROM questions
                WHERE video_id = %s
                ORDER BY id;
            """, (video_id,))
            
            questions = cur.fetchall()

    return {
        "id": video[0],
        "youtube_video_id": video[1],
        "youtube_url": video[2],
        "title": video[3],
        "channel_name": video[4],
        "thumbnail_url": video[5],
        "questions": [
            {
                "id": q[0],
                "question_text": q[1],
                "options": [q[2], q[3], q[4], q[5]],
            }
            for q in questions
        ],
    }


@app.post("/answers")
def submit_answer(answer: AnswerSubmission):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT correct_answer
                FROM questions
                WHERE id = %s;
            """, (answer.question_id,))
            row = cur.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Question not found")

            correct_answer = row[0]
            is_correct = answer.selected_answer == correct_answer

            cur.execute("""
                INSERT INTO user_answers (question_id, selected_answer, is_correct)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (answer.question_id, answer.selected_answer, is_correct))

            answer_id = cur.fetchone()[0]
            conn.commit()

    return {
        "answer_id": answer_id,
        "question_id": answer.question_id,
        "selected_answer": answer.selected_answer,
        "is_correct": is_correct,
        "correct_answer": correct_answer,
    }


@app.get("/score")
def get_score():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) AS total_answered,
                    COUNT(*) FILTER (WHERE is_correct = TRUE) AS total_correct
                FROM user_answers;
            """)
            total_answered, total_correct = cur.fetchone()

    percentage = 0 if total_answered == 0 else round((total_correct / total_answered) * 100)

    return {
        "total_answered": total_answered,
        "total_correct": total_correct,
        "percentage": percentage,
    }


