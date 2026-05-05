import "./App.css";
import { useEffect, useState } from "react";


function App() {
  
  const [latestVideo, setVideo] = useState<any>(null);
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
      body: JSON.stringify({
        question_id: questionId,
        selected_answer: selected,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setFeedback(data);
    });
  }

  function getScore() {
  fetch("http://localhost:8000/score")
    .then((res) => res.json())
    .then((data) => setScore(data));
}

  if (!latestVideo) return <div>Loading...</div>;

  const currentQuestion = latestVideo.questions[currentQuestionIndex];

  return (
  <main className="app">
    <section className="hero">
      <nav className="topbar">
        <div className="logo">LinguaLift</div>
        <button className="library-button">Library</button>
      </nav>

      <div className="video-card">
        <img
          src={latestVideo.thumbnail_url || "/src/assets/hero.png"}
          alt=""
          className="thumbnail"
        />

        <div className="video-content">
          <p className="eyebrow">Latest practice set</p>
          <h1>{latestVideo.title}</h1>
          <p className="channel">{latestVideo.channel_name || "YouTube video"}</p>
          <div className="stats">
            <span>{latestVideo.questions.length} questions</span>
            <span>Vocabulary practice</span>
          </div>
        </div>
      </div>
    </section>

    <section className="quiz-card">
      <div className="progress-track">
        <div
          className="progress-fill"
          style={{
            width: `${((currentQuestionIndex + 1) / latestVideo.questions.length) * 100}%`,
          }}
        />
      </div>

      <p className="question-count">
        Question {currentQuestionIndex + 1} of {latestVideo.questions.length}
      </p>

      <h2>{currentQuestion.question_text}</h2>

      <div className="answer-grid">
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
        <div className={feedback.is_correct ? "feedback correct-feedback" : "feedback"}>
          {feedback.is_correct ? "Correct" : `Incorrect — correct answer: ${feedback.correct_answer}`}
        </div>
      )}

      <button
        className="secondary-button"
        onClick={() => {
          setFeedback(null);
          setCurrentQuestionIndex((prev) => prev + 1);
        }}
      >
        Next question
      </button>

      <button className="secondary-button" onClick={getScore}>
        Get score
      </button>

      {score && (
        <div className="feedback correct-feedback">
          Score: {score.total_correct}/{score.total_answered} ({score.percentage}%)
        </div>
)}
    </section>



  </main>
);
}
   
  


export default App;