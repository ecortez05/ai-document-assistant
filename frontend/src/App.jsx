import { useEffect, useState } from "react";
import { api, hasToken, setToken } from "./api.js";
import Login from "./components/Login.jsx";
import Documents from "./components/Documents.jsx";
import Chat from "./components/Chat.jsx";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(hasToken());
  const [docs, setDocs] = useState([]);
  const [selected, setSelected] = useState("");

  const refresh = () => api.documents().then(setDocs).catch(() => {});

  useEffect(() => {
    if (loggedIn) refresh();
  }, [loggedIn]);

  function logout() {
    setToken(null);
    setLoggedIn(false);
    setDocs([]);
  }

  if (!loggedIn) return <Login onDone={() => setLoggedIn(true)} />;

  return (
    <div className="layout">
      <header>
        <h1>Document Assistant</h1>
        <button className="link" onClick={logout}>Log out</button>
      </header>
      <main>
        <Documents docs={docs} selected={selected} onSelect={setSelected} onChange={refresh} />
        <Chat documentId={selected} hasDocs={docs.length > 0} />
      </main>
    </div>
  );
}
