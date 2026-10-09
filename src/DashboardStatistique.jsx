import { useEffect, useState } from "react";


const API_URL = "http://localhost:5000/stats";
const SEUIL_ROUGE = 60;   // à ajuster avec le groupe
const SEUIL_ORANGE = 40;


function couleur(taux) {
  if (taux >= SEUIL_ROUGE) return "#e02424";
  if (taux >= SEUIL_ORANGE) return "#f59e0b";
  return "#15803d";
}

function CarteChiffre({ titre, valeur }) {
  return (
    <div style={styles.carte}>
      <div style={styles.carteTitre}>{titre}</div>
      <div style={styles.carteValeur}>{valeur}</div>
    </div>
  );
}
function BarreMatiere({ matiere, taux }) {
  return (
    <div style={styles.ligneMatiere}>
      <span style={styles.nomMatiere}>{matiere}</span>
      <div style={styles.piste}>
        <div

          style={{
            height: "100%",
            borderRadius: "6px", width: `${Math.min(taux, 100)}%`, background: couleur(taux)
          }}
        />
      </div>
      <span style={styles.pourcent}>{taux} %</span>
    </div>
  );
}

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [erreur, setErreur] = useState(false);

  useEffect(() => {
    fetch(API_URL)
      .then((reponse) => {
        if (!reponse.ok) throw new Error("Erreur serveur");
        return reponse.json();
      })
      .then((donnees) => setStats(donnees))
      .catch(() => setErreur(true));
  }, []);

  if (erreur) return <p>Impossible de joindre le serveur. Vérifie que le backend est lancé.</p>;
  if (stats === null) return <p>Chargement...</p>;


  return (
    <div>
      <h1>Tableau de bord</h1>

      <div style={styles.cartes}>
        <CarteChiffre
          titre="Élève le plus absent"
          valeur={stats.etudiant_plus_absent?.nom || "Aucun"}
        />
        <CarteChiffre titre="Taux global" valeur={`${stats.taux_global} %`} />
        <CarteChiffre titre="Total d'absences" valeur={stats.total_absences} />
      </div>

      <h3>Absences par matière</h3>
      {stats.par_matiere.map((m) => (
        <BarreMatiere key={m.matiere} matiere={m.matiere} taux={m.taux} />
      ))}


    </div>
  );
}
const styles = {
  cartes: {
    display: "flex",
    gap: "16px",
    margin: "24px 0 32px",
  },
  carte: {
    flex: 1,
    background: "#f3f4f6",
    border: "1px solid #d1d5db",
    borderRadius: "10px",
    padding: "16px",
  },
  carteTitre: {
    fontSize: "13px",
    color: "#6b7280",
  },
  carteValeur: {
    fontSize: "22px",
    fontWeight: "700",
    color: "#0b5348",
    marginTop: "8px",
  },
  ligneMatiere: {
    display: "flex",
    alignItems: "center",
    gap: "16px",
    margin: "16px 0",
  },
  nomMatiere: {
    width: "140px",
    fontWeight: "500",
  },
  piste: {
    flex: 1,
    height: "12px",
    background: "#e5e7eb",
    borderRadius: "6px",
    overflow: "hidden",
  },
  barre: {
    height: "100%",
    borderRadius: "6px",
  },
  pourcent: {
    width: "55px",
    textAlign: "right",
    fontWeight: "600",
  },
};

export default Dashboard;
