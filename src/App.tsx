import "./App.css";

const latestVideo = {
  title: "Dutch Listening Practice: Daily Life in Amsterdam",
  thumbnail:
    "https://images.unsplash.com/photo-1512470876302-972faa2aa9a4?q=80&w=1200&auto=format&fit=crop",
  channel: "External YouTube Channel",
  questionCount: 10,
};

const question = {
  word: "fiets",
  prompt: 'What does "fiets" mean?',
  options: ["car", "bicycle", "train", "street"],
  correctAnswer: "bicycle",
};

function App() {
  return (
    <main className="app">
      <section className="hero">
        <nav className="topbar">
          <div className="logo">LinguaLift</div>
          <button className="library-button">Library</button>
        </nav>

        <div className="video-card">
          <img src={latestVideo.thumbnail} alt="" className="thumbnail" />

          <div className="video-content">
            <p className="eyebrow">Latest practice set</p>
            <h1>{latestVideo.title}</h1>
            <p className="channel">{latestVideo.channel}</p>

            <div className="stats">
              <span>{latestVideo.questionCount} questions</span>
              <span>Vocabulary practice</span>
            </div>

            <button className="primary-button">Start practice</button>
          </div>
        </div>
      </section>

      <section className="quiz-card">
        <div className="progress-track">
          <div className="progress-fill" />
        </div>

        <p className="question-count">Question 1 of 10</p>

        <h2>{question.prompt}</h2>

        <div className="answer-grid">
          {question.options.map((option) => (
            <button
              key={option}
              className={option === question.correctAnswer ? "answer correct" : "answer"}
            >
              {option}
            </button>
          ))}
        </div>

        <div className="feedback correct-feedback">
          Correct — “fiets” means bicycle.
        </div>

        <button className="secondary-button">Next question</button>

        <button className="rewatch-placeholder">
          Rewatch word in video · coming later
        </button>
      </section>
    </main>
  );
}

export default App;