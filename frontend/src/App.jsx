import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) {
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

      console.log("Backend response:", response.data);

      setResult(response.data);

    } catch (err) {
      console.error("Frontend error:", err);

      setError(
        err.response?.data?.detail ||
        err.message ||
        "Could not connect to the AI backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Import-Export Regulation AI</h1>

        <p>
          Ask questions about import-export regulations and receive answers
          based on the available documents.
        </p>
      </header>

      <div className="question-card">
        <h2>Ask a question</h2>

        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question here..."
        />

        <button
          onClick={askQuestion}
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
              className={`confidence ${result.confidence?.level?.toLowerCase()}`}
            >
              {result.confidence?.level} CONFIDENCE
            </span>
          </div>

          {result.answer ? (
            <p className="answer">
              {result.answer}
            </p>
          ) : (
            <p>
              No answer was generated. Human review may be required.
            </p>
          )}

          <hr />

          <p>
            <strong>Status:</strong> {result.status}
          </p>

          {result.sources && result.sources.length > 0 && (
            <>
              <h2>Sources</h2>

              {result.sources.map((source, index) => (
                <div className="source" key={index}>
                  <strong>{source.document_name}</strong>

                  <span>
                    Page {source.page}
                  </span>
                </div>
              ))}
            </>
          )}

        </div>
      )}
    </div>
  );
}

export default App;