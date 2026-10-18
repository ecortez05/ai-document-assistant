import { useEffect, useRef, useState } from "react";
import { api } from "../api.js";

export default function Chat({ documentId, hasDocs }) {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const bottom = useRef();

  useEffect(() => {
    bottom.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send(e) {
    e.preventDefault();
    const q = question.trim();
    if (!q || loading) return;
    setQuestion("");
    setMessages((m) => [...m, { role: "user", text: q }]);
    setLoading(true);
    try {
      const res = await api.ask(q, documentId);
      setMessages((m) => [...m, { role: "assistant", text: res.answer, sources: res.sources }]);
    } catch (err) {
      setMessages((m) => [...m, { role: "assistant", text: err.message, failed: true }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card chat">
      <div className="messages">
        {messages.length === 0 && (
          <p className="muted">{hasDocs ? "Ask something about your documents." : "Upload a PDF to get started."}</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role} ${m.failed ? "failed" : ""}`}>
            <p>{m.text}</p>
            {m.sources?.length > 0 && (
              <details>
                <summary>{m.sources.length} sources</summary>
                <ol>
                  {m.sources.map((s, j) => (
                    <li key={j}>
                      <strong>{s.filename}</strong>, page {s.page}
                      <blockquote>{s.snippet}…</blockquote>
                    </li>
                  ))}
                </ol>
              </details>
            )}
          </div>
        ))}
        {loading && <div className="msg assistant muted">Thinking…</div>}
        <div ref={bottom} />
      </div>
      <form onSubmit={send} className="ask">
        <input value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ask a question…" />
        <button disabled={loading || !hasDocs}>Send</button>
      </form>
    </section>
  );
}
