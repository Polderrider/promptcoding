import "./App.css";
import { useEffect, useState } from "react";

type Page = "landing" | "quiz" | "score";

function App() {
  const [latestVideo, setVideo] = useState<any>(null);
  const [page, setPage] = useState<Page>("landing");
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [feedback, setFeedback] = useState<any>(null);
  const [score, setScore] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/latest-video")
      .then((res) => res.json())
      .then((data) => setVideo(data));
  }, []);

  function submitAnswer(questionId: number, selected: string) {
    fetch("http://localhost:8000/answers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question_id: questionId, selected_answer: selected }),
    })
      .then((res) => res.json())
      .then((data) => setFeedback(data));
  }

  function finishQuiz() {
    fetch("http://localhost:8000/score")
      .then((res) => res.json())
      .then((data) => {
        setScore(data);
        setPage("score");
      });
  }

  function nextQuestion() {
    setFeedback(null);

    if (currentQuestionIndex + 1 >= latestVideo.questions.length) {
      finishQuiz();
      return;
    }

    setCurrentQuestionIndex((prev) => prev + 1);
  }

  if (!latestVideo) return <div className="loading">Loading...</div>;

  const currentQuestion = latestVideo.questions[currentQuestionIndex];

  return (
    <main className="app">
      <nav className="topbar">
        <div className="brand">study app</div>
        <button>Video Library</button>
        <button>Reviews</button>
        <button>Visitor Count</button>
      </nav>

      {page === "landing" && (
        <section className="landing">
          <h1>Welcome to NOS Study</h1>
          <p className="intro">
            Your partner to test knowledge on today&apos;s NOS video in easy Dutch.
          </p>
          <p className="visitor">You are today&apos;s 42nd visitor.</p>

          <div className="latest-panel">
            <img
              src={latestVideo.thumbnail_url || "/src/assets/hero.png"}
              alt=""
              className="video-thumb"
            />

            <div className="latest-content">
              <h2>{latestVideo.title}</h2>

              <div className="level-row">
                <button onClick={() => setPage("quiz")}>Novice</button>
                <button onClick={() => setPage("quiz")}>Beginner</button>
                <button onClick={() => setPage("quiz")}>Intermediate</button>
                <button onClick={() => setPage("quiz")}>Advanced</button>
              </div>

              <p className="score-note">
                Your score on Easy: — That&apos;s the 3rd highest score today.
              </p>
            </div>
          </div>
        </section>
      )}

      {page === "quiz" && (
        <section className="quiz-page">
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{
                width: `${((currentQuestionIndex + 1) / latestVideo.questions.length) * 100}%`,
              }}
            />
          </div>

          <h2 className="question-title">{currentQuestion.question_text}</h2>

          <div className="answer-row">
            {currentQuestion.options.map((opt: string) => (
              <button
                key={opt}
                className="answer"
                onClick={() => submitAnswer(currentQuestion.id, opt)}
              >
                {opt}
              </button>
            ))}
          </div>

          {feedback && (
            <div className={feedback.is_correct ? "feedback correct" : "feedback incorrect"}>
              {feedback.is_correct
                ? "Correct"
                : `Incorrect — correct answer: ${feedback.correct_answer}`}
              <button onClick={nextQuestion}>Next</button>
            </div>
          )}
        </section>
      )}

      {page === "score" && score && (
        <section className="score-page">
          <h1>Your result</h1>
          <p>
            Score: {score.total_correct}/{score.total_answered} ({score.percentage}%)
          </p>
          <button onClick={() => window.location.reload()}>Replay quiz</button>
        </section>
      )}
    </main>
  );
}

export default App;