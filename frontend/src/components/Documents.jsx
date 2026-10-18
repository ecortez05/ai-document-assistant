import { useRef, useState } from "react";
import { api } from "../api.js";

export default function Documents({ docs, selected, onSelect, onChange }) {
  const input = useRef();
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  async function handleFile(e) {
    const file = e.target.files[0];
    if (!file) return;
    setError("");
    setUploading(true);
    try {
      await api.upload(file);
      await onChange();
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
      input.current.value = "";
    }
  }

  async function remove(id) {
    if (!confirm("Delete this document?")) return;
    await api.remove(id);
    if (String(id) === String(selected)) onSelect("");
    onChange();
  }

  return (
    <aside className="card">
      <h2>Documents</h2>
      <input ref={input} type="file" accept="application/pdf" onChange={handleFile} hidden />
      <button onClick={() => input.current.click()} disabled={uploading}>
        {uploading ? "Processing…" : "Upload PDF"}
      </button>
      {error && <p className="error">{error}</p>}

      <ul className="docs">
        <li className={selected === "" ? "active" : ""} onClick={() => onSelect("")}>
          All documents
        </li>
        {docs.map((d) => (
          <li key={d.id} className={String(d.id) === String(selected) ? "active" : ""} onClick={() => onSelect(d.id)}>
            <span>
              {d.filename} <small>{d.page_count} pg</small>
            </span>
            <button
              className="link"
              onClick={(e) => {
                e.stopPropagation();
                remove(d.id);
              }}
            >
              ✕
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
