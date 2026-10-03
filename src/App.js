import { useState } from "react";
import Sidebar from "./Sidebar";
import NouvelleAbsence from "./NouvelleAbsence";

function App() {
  const [page, setPage] = useState("saisie");

  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "sans-serif" }}>
      <Sidebar page={page} setPage={setPage} />
      <main style={{ flex: 1, padding: "32px", background: "#f8fafc" }}>
        {page === "saisie" && <NouvelleAbsence />}
        {page === "dashboard" && <p>Tableau de bord (Personne 3)</p>}
        {page === "consulter" && <p>Consulter (Personne 2)</p>}
      </main>
    </div>
  );
}

export default App;