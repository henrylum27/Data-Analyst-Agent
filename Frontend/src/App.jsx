import { useRef, useState } from "react";
import axios from "axios";
import html2pdf from "html2pdf.js";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [summary, setSummary] = useState("");
  const [question, setQuestion] = useState("");
  const [sqlResult, setSqlResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const reportRef = useRef(null);
  const API_BASE = "http://127.0.0.1:8000";

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadResult(null);
    setSummary("");
    setSqlResult(null);
  };

  const uploadCsv = async () => {
    if (!file) {
      alert("Please upload a CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/upload`, formData);
      setUploadResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Upload failed. Make sure your backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const generateSummary = async () => {
    if (!file) {
      alert("Please upload a CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/summary`, formData);
      setSummary(response.data.summary);
    } catch (error) {
      console.error(error);
      alert("Summary failed. Make sure Ollama and backend are running.");
    } finally {
      setLoading(false);
    }
  };

  const runSql = async () => {
    if (!file) {
      alert("Please upload a CSV file first.");
      return;
    }

    if (!question.trim()) {
      alert("Please enter a question.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/run-sql`, formData);
      setSqlResult(response.data);
    } catch (error) {
      console.error(error);
      alert("SQL query failed.");
    } finally {
      setLoading(false);
    }
  };

  const downloadSummaryPdf = () => {
    if (!reportRef.current) return;

    const options = {
      margin: 0.5,
      filename: "data-analysis-executive-summary.pdf",
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
    };

    html2pdf().set(options).from(reportRef.current).save();
  };

  const formatSummaryLines = (text) => {
    return text
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      .map((line) => line.replace(/\*\*/g, "").replace(/^#+\s?/g, ""));
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="navbar-content">
          <div className="logo-block">
            <h1>Data Analyst Agent</h1>
            <p>AI-powered CSV profiling, SQL analysis, and executive reporting</p>
          </div>
          <div className="status-pill">Local AI • Free • Private</div>
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div className="hero-card">
            <h2>Analyze datasets faster with a local AI assistant.</h2>
            <p>
              Upload a CSV file, detect data quality issues, generate professional
              summaries, and ask natural-language questions that are converted into
              safe SQL.
            </p>
          </div>

          <div className="upload-card">
            <h3>Upload Dataset</h3>

            <input
              className="file-input"
              type="file"
              accept=".csv"
              onChange={handleFileChange}
            />

            <div className="button-row">
              <button onClick={uploadCsv} disabled={loading}>
                Analyze CSV
              </button>

              {uploadResult && (
                <button
                  className="secondary-button"
                  onClick={generateSummary}
                  disabled={loading}
                >
                  Generate AI Summary
                </button>
              )}
            </div>

            {file && <p className="selected-file">Selected file: {file.name}</p>}
          </div>
        </section>

        {loading && <div className="loading">Processing request...</div>}

        {uploadResult && (
          <section className="section">
            <div className="card">
              <div className="card-header">
                <h2 className="section-title">Dataset Overview</h2>
                <div className="status-pill">{uploadResult.filename}</div>
              </div>

              <div className="metrics">
                <div className="metric-card">
                  <span>Rows</span>
                  <strong>{uploadResult.profile.rows}</strong>
                </div>

                <div className="metric-card">
                  <span>Columns</span>
                  <strong>{uploadResult.profile.columns}</strong>
                </div>

                <div className="metric-card">
                  <span>Missing Values</span>
                  <strong>{uploadResult.profile.total_missing}</strong>
                </div>
              </div>

              <h3>Data Preview</h3>
              <Table data={uploadResult.preview} />

              <h3>Column Summary</h3>
              <Table data={uploadResult.profile.columns_summary} />

              <h3>Anomaly Detection</h3>
              {uploadResult.anomalies.length > 0 ? (
                <Table data={uploadResult.anomalies} />
              ) : (
                <p className="empty-state">No numeric anomalies detected.</p>
              )}
            </div>
          </section>
        )}

        {summary && (
          <section className="section">
            <div className="card">
              <div className="card-header">
                <div>
                  <h2 className="section-title">Executive Summary</h2>
                  <p className="section-description">
                    A professional report generated from the uploaded dataset.
                  </p>
                </div>

                <button onClick={downloadSummaryPdf}>Download PDF</button>
              </div>

              <div className="report-document" ref={reportRef}>
                <div className="report-header">
                  <h1>Data Analysis Executive Summary</h1>
                  <p>Generated by Data Analyst Agent</p>
                </div>

                <div className="report-meta">
                  <div>
                    <strong>Dataset</strong>
                    <span>{uploadResult?.filename}</span>
                  </div>

                  <div>
                    <strong>Rows</strong>
                    <span>{uploadResult?.profile.rows}</span>
                  </div>

                  <div>
                    <strong>Columns</strong>
                    <span>{uploadResult?.profile.columns}</span>
                  </div>

                  <div>
                    <strong>Missing Values</strong>
                    <span>{uploadResult?.profile.total_missing}</span>
                  </div>
                </div>

                <div className="report-section">
                  <h2>Executive Summary</h2>

                  {formatSummaryLines(summary).map((line, index) => {
                    const isHeading =
                      line.toLowerCase().includes("dataset overview") ||
                      line.toLowerCase().includes("data quality") ||
                      line.toLowerCase().includes("notable") ||
                      line.toLowerCase().includes("recommended") ||
                      line.toLowerCase().includes("next steps") ||
                      line.match(/^\d+\./);

                    if (isHeading) {
                      return <h3 key={index}>{line}</h3>;
                    }

                    return <p key={index}>{line}</p>;
                  })}
                </div>

                <div className="report-footer">
                  <p>
                    This report was generated locally using an AI model through
                    Ollama. Results should be reviewed before business use.
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}

        {uploadResult && (
          <section className="section">
            <div className="card">
              <div className="card-header">
                <h2 className="section-title">Ask a Data Question</h2>
                <div className="status-pill">DuckDB SQL</div>
              </div>

              <input
                className="question-input"
                type="text"
                placeholder="Example: Show total sales by region"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />

              <button onClick={runSql} disabled={loading}>
                Generate and Run SQL
              </button>

              {sqlResult && (
                <div>
                  <h3>Generated SQL</h3>
                  <pre className="sql">{sqlResult.sql}</pre>

                  {sqlResult.error && <p className="error">{sqlResult.error}</p>}

                  {sqlResult.results && (
                    <>
                      <h3>Query Results</h3>
                      <Table data={sqlResult.results} />
                    </>
                  )}
                </div>
              )}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

function Table({ data }) {
  if (!data || data.length === 0) {
    return <p className="empty-state">No data available.</p>;
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {columns.map((col) => (
                <td key={col}>{String(row[col])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;