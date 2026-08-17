import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  const handleAsk = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/ask",
        {
          params: {
            question: question
          }
        }
      );

      setResult(response.data);

    } catch (err) {
      console.error(err);
      setError(
        "Could not connect to the AI backend. Make sure the FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">

        <header className="header">
          <h1>Import-Export Regulation AI</h1>
          <p>
            Ask questions about import-export regulations and receive
            answers based on the available documents.
          </p>
        </header>

        <main>
          <div className="question-card">
            <label htmlFor="question">
              Ask a question
            </label>

            <textarea
              id="question"
              placeholder="Example: What documents are required for customs clearance?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              rows="4"
            />

            <button
              onClick={handleAsk}
              disabled={loading}
            >
              {loading ? "Thinking..." : "Ask AI"}
            </button>
          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          {result && (
            <div className="result-card">

              <div className="result-header">
                <h2>AI Response</h2>

                <span
                  className={`confidence ${result.confidence.level.toLowerCase()}`}
                >
                  {result.confidence.level} CONFIDENCE
                </span>
              </div>

              {result.answer ? (
                <div className="answer">
                  {result.answer}
                </div>
              ) : (
                <div className="human-review">
                  <h3>Human Review Required</h3>
                  <p>
                    {result.confidence.message}
                  </p>
                  <p>
                    The available documents do not contain enough reliable
                    information to answer this question.
                  </p>
                </div>
              )}

              <div className="status">
                <strong>Status:</strong> {result.status}
              </div>

              {result.sources.length > 0 && (
                <div className="sources">
                  <h3>Sources</h3>

                  {result.sources.map((source, index) => (
                    <div className="source" key={index}>
                      <strong>{source.document_name}</strong>
                      <span>Page {source.page}</span>
                    </div>
                  ))}
                </div>
              )}

            </div>
          )}

        </main>

      </div>
    </div>
  );
}

export default App;