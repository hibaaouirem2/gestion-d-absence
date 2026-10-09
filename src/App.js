import { useState } from "react";
import Sidebar from "./Sidebar";
import NouvelleAbsence from "./NouvelleAbsence";
import ConsulterAbsences from "./ConsulterAbsences"
import Dashboard from "./DashboardStatistique";

function App() {
  const [page, setPage] = useState("saisie");

  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "sans-serif" }}>
      <Sidebar page={page} setPage={setPage} />
      <main style={{ flex: 1, padding: "32px", background: "#f8fafc" }}>
        {page === "saisie" && <NouvelleAbsence />}
            {page === "consulter" && <ConsulterAbsences />}
        {page === "dashboard" && <Dashboard/>}

      </main>
    </div>
  );
}

export default App;