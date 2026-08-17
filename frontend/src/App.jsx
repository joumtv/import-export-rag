import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Load history
  const loadHistory = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/history`
      );

      setHistory(response.data);

    } catch (err) {
      console.error("Could not load history:", err);
    }
  };

  // Load history when page starts
  useEffect(() => {
    axios
      .get(`${API_URL}/history`)
      .then((response) => {
        setHistory(response.data);
      })
      .catch((err) => {
        console.error("Could not load history:", err);
      });
  }, []);


  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await axios.get(
        `${API_URL}/ask`,
        {
          params: {
            question: question
          }
        }
      );

      console.log("Backend response:", response.data);

      setResult(response.data);

      // Reload history after asking a new question
      await loadHistory();

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

                  <strong>
                    {source.document_name}
                  </strong>

                  <span>
                    Page {source.page}
                  </span>

                </div>
              ))}
            </>
          )}

        </div>
      )}


      {/* HISTORY */}

      <div className="history-section">

        <h2>Question History</h2>

        {history.length === 0 ? (

          <p className="no-history">
            No question history yet.
          </p>

        ) : (

          history.map((item) => (

            <div
              className="history-card"
              key={item.id}
            >

              <div className="history-header">

                <span className="history-number">
                  #{item.id}
                </span>

                <span
                  className={`confidence ${item.confidence_level?.toLowerCase()}`}
                >
                  {item.confidence_level} CONFIDENCE
                </span>

              </div>


              <h3>Question</h3>

              <p>
                {item.question}
              </p>


              <h3>Answer</h3>

              <p>
                {item.answer || "No answer generated."}
              </p>


              <p className="history-status">
                <strong>Status:</strong>{" "}
                {item.status}
              </p>


              {item.created_at && (
                <p className="history-date">
                  {new Date(item.created_at).toLocaleString()}
                </p>
              )}

            </div>

          ))
        )}

      </div>

    </div>
  );
}

export default App;