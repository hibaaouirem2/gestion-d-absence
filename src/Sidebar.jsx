function Sidebar({ page, setPage }) {
  return (
    <aside style={styles.sidebar}>
      <div style={styles.logo}>Suivi d'absence</div>
      <p style={styles.label}>Espace enseignant</p>
      <nav>
        <button style={page === "dashboard" ? styles.actif : styles.lien}
          onClick={() => setPage("dashboard")}>
          📊 Tableau de bord
        </button>
        <button style={page === "saisie" ? styles.actif : styles.lien}
          onClick={() => setPage("saisie")}>
          ➕ Nouvelle absence
        </button>
        <button style={page === "consulter" ? styles.actif : styles.lien}
          onClick={() => setPage("consulter")}>
          🔍 Consulter
        </button>
      </nav>
    </aside>
  );
}

const styles = {
  sidebar: { width: "200px", background: "#5e326d", color: "white",
    padding: "24px 16px", minHeight: "100vh", display: "flex",
    flexDirection: "column", gap: "8px" },
  logo: { fontSize: "20px", fontWeight: "bold", marginBottom: "4px" },
  label: { fontSize: "12px", color: "#b294be", marginBottom: "16px" },
  lien: { display: "block", width: "100%", background: "none", border: "none",
    color: "#dbc4e2", padding: "10px 12px", borderRadius: "6px",
    cursor: "pointer", textAlign: "left", fontSize: "14px" },
  actif: { display: "block", width: "100%", background: "#35053f", border: "none",
    color: "white", padding: "10px 12px", borderRadius: "6px",
    cursor: "pointer", textAlign: "left", fontSize: "14px" },
};

export default Sidebar;