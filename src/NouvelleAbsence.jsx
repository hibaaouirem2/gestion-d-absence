import { useState, useEffect } from "react";

function NouvelleAbsence() {
  const [etudiants, setetudiants] = useState([]);
  const [form, setForm] = useState({
    etudiant_id: "", date: "", matiere: "", justifiee: true
  });
  const [message, setMessage] = useState("");

  // ── Ajouter un élève ──
  const [nometudiant, setNometudiant] = useState("");
  const [messageetudiant, setMessageetudiant] = useState("");

  const chargeretudiants = () => {
    fetch("http://localhost:5000/etudiants")
      .then((r) => r.json())
      .then(setetudiants);
  };

  useEffect(() => {
    chargeretudiants();
  }, []);

  const handleAjouteretudiant = async (e) => {
    handleAnnuler();
    e.preventDefault();
    const res = await fetch("http://localhost:5000/etudiants", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nom: nometudiant }),
    });
    const data = await res.json();
    setMessageetudiant("✅ " + data.message);
    setNometudiant("");
    chargeretudiants();
  };

const handleSupprimeretudiant = async (id) => {
  handleAnnuler()
  const res=  await fetch(`http://localhost:5000/etudiants/${id}`, {
    method: "DELETE",
  });
  const data = await res.json();

  setMessageetudiant("✅ "+ data.message)

  chargeretudiants(); // recharge la liste
};

  const handleAnnuler = () => {
    setForm({ etudiant_id: "", date: "", matiere: "", justifiee: true });
    setMessage("");
  };

  const handleSubmit = async (e) => {
    setMessageetudiant("")
    e.preventDefault();
    const res = await fetch("http://localhost:5000/absences", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    setMessage(data.message);
  };

  return (
    <div style={styles.container}>

      {/* ── Section Ajouter un Étudiant ── */}
      <div style={styles.section}>
        <h3 style={styles.sousTitre}>Ajouter un Étudiant </h3>
        <form onSubmit={handleAjouteretudiant} style={styles.ligneForm}>
          <input
            required
            placeholder="Nom complet de l'élève"
            value={nometudiant}
            onChange={(e) => setNometudiant(e.target.value)}
            style={styles.inputLigne}
          />
          <button type="submit" style={styles.btnViolet}>Ajouter</button>
        </form>
        {messageetudiant && <p style={styles.succes}>{messageetudiant}</p>}
              {/* ── Liste des élèves avec bouton supprimer ── */}
      {etudiants.length > 0 && (
        <ul style={styles.liste}>
          {etudiants.map((el) => (
            <li key={el.id} style={styles.listeItem}>
              <span>{el.nom}</span>
              <button
                onClick={() => handleSupprimeretudiant(el.id)}
                style={styles.btnSupprimer}>
                🗑 Supprimer
              </button>
            </li>
          ))}
        </ul>
      )}
              
      </div>

      <hr style={{ margin: "24px 0", borderColor: "#e2e8f0" }} />

      {/* ── Section Nouvelle absence ── */}
      <h2 style={styles.titre}>Nouvelle absence</h2>
      <p style={styles.sous}>Ici vous pouvez ajouter une absences des élèves avec 4 champs</p>

      {message && <div style={styles.succes}>✅ {message}</div>}

      <form onSubmit={handleSubmit} style={styles.form}>
        <label style={styles.label}>Étudiant</label>
        <select required style={styles.input}
          value={form.etudiant_id}
          onChange={(e) => setForm({ ...form, etudiant_id: e.target.value })}>
          <option value="">Selectionner un Étudiant</option>
          {etudiants.map((el) => (
            <option key={el.id} value={el.id}>{el.nom}</option>
          ))}
        </select>

        <label style={styles.label}>Date</label>
        <input required type="date" style={styles.input}
          value={form.date}
          onChange={(e) => setForm({ ...form, date: e.target.value })} />

        <label style={styles.label}>Matière</label>
        <select required style={styles.input}
          value={form.matiere}
          onChange={(e) => setForm({ ...form, matiere: e.target.value })}>
          <option value="">Selectionner une matière</option>
          <option value="Reseaux locaux d'entreprise">Réseaux Locaux d'Entreprise</option>
          <option value="Introduction a l'informatique et au numerique">Introduction à l'Informatique et au Numérique</option>
          <option value="Academic English">Academic English</option>
          <option value="Architecture des ordinateurs">Architecture des Ordinateurs</option>
          <option value="Initiation aux Atelier dissertatifs">Initiation aux Ateliers dissertatifs</option>
          <option value="Structures de donnees">Structures de Donéees</option>
          <option value="Fondements Mathematiques">Fondements Mathématiques</option>
          <option value="Systeme d'information">Système d'Information</option>
          <option value="Systeme d'exploitations">Système d'Exploitations</option>
        </select>

        <label style={styles.label}>Absence justifiée ?</label>
        <div style={styles.radioGroup}>
          <label style={styles.radio}>
            <input type="radio" name="justifiee" checked={form.justifiee === true}
              onChange={() => setForm({ ...form, justifiee: true })} />
            Oui
          </label>
          <label style={styles.radio}>
            <input type="radio" name="justifiee" checked={form.justifiee === false}
              onChange={() => setForm({ ...form, justifiee: false })} />
            Non
          </label>
        </div>

        <div style={styles.boutons}>
          <button type="button" onClick={handleAnnuler} style={styles.btnAnnuler}>
            Annuler
          </button>
          <button type="submit" style={styles.btnEnregistrer}>
            Enregistrer
          </button>
        </div>
      </form>
    </div>
  );
}

const styles = {
  container: { maxWidth: "520px", padding: "32px" },
  section: { background: "#f1f5f9", padding: "16px", borderRadius: "8px" },
  sousTitre: { fontSize: "16px", fontWeight: "bold", marginBottom: "12px", marginTop: 0 },
  ligneForm: { display: "flex", gap: "8px" },
  inputLigne: { flex: 1, padding: "10px", borderRadius: "6px",
    border: "1px solid #cbd5e1", fontSize: "14px" },
  btnViolet: { padding: "10px 16px", borderRadius: "6px", border: "none",
    background: "#9235c8", color: "white", cursor: "pointer", fontWeight: "bold" },
  titre: { fontSize: "22px", fontWeight: "bold", marginBottom: "4px" },
  sous: { color: "#64748b", marginBottom: "24px", fontSize: "14px" },
  succes: { background: "#dcfce7", color: "#16a34a", padding: "12px",
    borderRadius: "8px", marginBottom: "16px" },
  form: { display: "flex", flexDirection: "column", gap: "8px" },
  label: { fontWeight: "600", fontSize: "14px" },
  input: { padding: "10px", borderRadius: "6px", border: "1px solid #cbd5e1",
    fontSize: "14px", marginBottom: "8px" },
  radioGroup: { display: "flex", gap: "16px", marginBottom: "8px" },
  radio: { display: "flex", alignItems: "center", gap: "6px", cursor: "pointer" },
  boutons: { display: "flex", gap: "12px", marginTop: "16px" },
  btnAnnuler: { flex: 1, padding: "10px", borderRadius: "6px",
    border: "1px solid #cbd5e1", background: "white", cursor: "pointer" },
  btnEnregistrer: { flex: 1, padding: "10px", borderRadius: "6px",
    border: "none", background: "#9235c8", color: "white",
    cursor: "pointer", fontWeight: "bold" },
    liste: { listStyle: "none", padding: 0, marginTop: "12px" },
    liste: { listStyle: "none", padding: 0, marginTop: "12px" },
  listeItem: { display: "flex", justifyContent: "space-between",
    alignItems: "center", padding: "8px 0",
    borderBottom: "1px solid #e2e8f0" },
  btnSupprimer: { background: "none", border: "none", color: "#ef4444",
    cursor: "pointer", fontSize: "13px" },
  };

export default NouvelleAbsence;