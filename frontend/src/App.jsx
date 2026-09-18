import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const suggestedQuestions = [
    "How does deforestation affect biodiversity and climate change?",
    "How does soil biodiversity affect ecosystem functioning?",
    "How does climate change affect forests?",
  ];

  const askQuestion = async (questionText = question) => {
    const trimmedQuestion = questionText.trim();

    if (!trimmedQuestion || loading) return;

    setLoading(true);
    setError("");
    setAnswer(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();

      setAnswer(data);
      setQuestion(trimmedQuestion);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to connect to Daaruka.Earth. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    askQuestion();
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">🌍</div>

          <div>
            <h1>Daaruka.Earth</h1>
            <span>Environmental Intelligence</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Scientific RAG
        </div>
      </header>

      <main className="main-content">
        <section className="hero">
          <div className="hero-badge">🌱 AI + Environmental Science</div>

          <h2>
            Understand Earth's
            <br />
            <span>connected systems.</span>
          </h2>

          <p>
            Ask questions about biodiversity, soil, forests, water, climate,
            and human impact using a scientific knowledge base.
          </p>
        </section>

        <section className="question-section">
          <form onSubmit={handleSubmit} className="question-box">
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask Daaruka.Earth a scientific question..."
              rows="3"
              disabled={loading}
            />

            <div className="question-footer">
              <span>Powered by scientific sources</span>

              <button type="submit" disabled={loading || !question.trim()}>
                {loading ? "Thinking..." : "Ask Daaruka →"}
              </button>
            </div>
          </form>

          <div className="suggestions">
            <span>Try asking:</span>

            <div className="suggestion-list">
              {suggestedQuestions.map((item) => (
                <button
                  key={item}
                  onClick={() => {
                    setQuestion(item);
                    askQuestion(item);
                  }}
                  disabled={loading}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </section>

        {loading && (
          <section className="answer-card loading-card">
            <div className="loading-spinner"></div>

            <div>
              <h3>Analyzing scientific knowledge...</h3>
              <p>
                Searching the Daaruka.Earth knowledge base and generating an
                evidence-grounded answer.
              </p>
            </div>
          </section>
        )}

        {error && <div className="error-message">⚠️ {error}</div>}

        {answer && !loading && (
          <section className="answer-card">
            <div className="answer-header">
              <div className="answer-icon">🧠</div>

              <div>
                <span>DAARUKA.EARTH</span>
                <h3>Scientific Analysis</h3>
              </div>
            </div>

            <div className="answer-text">
              {answer.answer}
            </div>

            {answer.sources && answer.sources.length > 0 && (
              <div className="sources">
                <h4>📚 Sources</h4>

                <div className="source-list">
                  {answer.sources.map((source, index) => (
                    <div
                      className="source-item"
                      key={`${source.source}-${source.chunk_id}-${index}`}
                    >
                      <span>{index + 1}</span>

                      <div>
                        <strong>{source.source}</strong>
                        <small>Page {source.page} · Chunk {source.chunk_id}</small>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {!answer && !loading && !error && (
          <section className="knowledge-preview">
            <div>🌱</div>
            <h3>Scientific environmental intelligence</h3>
            <p>
              Daaruka.Earth retrieves relevant evidence from its environmental
              knowledge base before generating an answer.
            </p>

            <div className="knowledge-grid">
              <div>🌳 Forests</div>
              <div>🐝 Biodiversity</div>
              <div>🌱 Soil</div>
              <div>💧 Water</div>
              <div>🌡️ Climate</div>
              <div>🏭 Human Impact</div>
            </div>
          </section>
        )}
      </main>

      <footer>
        Daaruka.Earth · Environmental Intelligence System
      </footer>
    </div>
  );
}

export default App;