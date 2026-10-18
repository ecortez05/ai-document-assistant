const BASE = "/api";

let token = localStorage.getItem("token");

export function setToken(t) {
  token = t;
  if (t) localStorage.setItem("token", t);
  else localStorage.removeItem("token");
}

export const hasToken = () => !!token;

async function request(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(BASE + path, { ...options, headers });

  if (res.status === 401 && token) {
    setToken(null);
    window.location.reload();
  }
  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") message = body.detail;
      else if (Array.isArray(body.detail)) message = body.detail[0]?.msg || message;
    } catch {}
    throw new Error(message);
  }
  return res.status === 204 ? null : res.json();
}

const json = (body) => ({
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

export const api = {
  login: (email, password) => request("/auth/login", json({ email, password })),
  register: (email, password) => request("/auth/register", json({ email, password })),
  documents: () => request("/documents"),
  upload: (file) => {
    const form = new FormData();
    form.append("file", file);
    return request("/documents", { method: "POST", body: form });
  },
  remove: (id) => request(`/documents/${id}`, { method: "DELETE" }),
  ask: (question, documentId) =>
    request("/chat", json({ question, document_id: documentId || null })),
};
