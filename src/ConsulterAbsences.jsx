import { useEffect, useState } from "react";

function ConsulterAbsences() {
  const [eleves, setEleves] = useState([]);
  const [eleveSelectionne, setEleveSelectionne] = useState(null);
  const [recherche, setRecherche] = useState("");
  const [absences, setAbsences] = useState([]);
  const [filtre, setFiltre] = useState("toutes");
  const [message, setMessage] = useState("");
  const [rechercheActive, setRechercheActive] = useState("");

  useEffect(() => {
    fetch("http://localhost:5000/etudiants")
      .then((response) => response.json())
      .then((data) => {
        setEleves(data);
      })
      .catch((error) => {
        console.error("Erreur :", error);
      });
  }, []);
  const elevesFiltres = eleves.filter((eleve) => {
    return eleve.nom
      .toLowerCase()
      .includes(rechercheActive.toLowerCase());
  });
  const lancerRecherche = () => {
    setRechercheActive(recherche);
  };
  const choisirEleve = (eleve) => {
    setEleveSelectionne(eleve);
    setFiltre("toutes");
    setMessage("");
    chargerAbsences(eleve.id, "toutes");
  };

  const chargerAbsences = (eleveId, filtreChoisi) => {
    const url = `http://localhost:5000/etudiants/${eleveId}/absences?filtre=${filtreChoisi}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setAbsences(data);
      })
      .catch((error) => {
        console.error("Erreur :", error);
      });
  };

  const changerFiltre = (nouveauFiltre) => {
    setFiltre(nouveauFiltre);

    if (eleveSelectionne !== null) {
      chargerAbsences(eleveSelectionne.id, nouveauFiltre);
    }
  };

  const supprimerAbsence = (absenceId) => {
    const confirmation = window.confirm(
      "Voulez-vous vraiment supprimer cette absence ?"
    );

    if (!confirmation) {
      return;
    }

    fetch(`http://localhost:5000/absences/${absenceId}`, {
      method: "DELETE"
    })
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message);

        if (eleveSelectionne !== null) {
          chargerAbsences(eleveSelectionne.id, filtre);
        }
      })
      .catch((error) => {
        console.error("Erreur :", error);
      });
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.titre}>Consulter les absences</h2>

      <p style={styles.sous}>
        Recherchez un élève puis consultez ses absences.
      </p>

      <div
        style={{
          display: "flex",
          gap: "10px",
          alignItems: "center"
        }}
      >
        <input
          type="text"
          placeholder="Rechercher un élève..."
          value={recherche}
          onChange={(e) => setRecherche(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              lancerRecherche();
            }
          }}
          style={styles.input}
        />

        <button
          onClick={lancerRecherche}
          style={styles.btnViolet}
        >
          Rechercher
        </button>
      </div>

      {rechercheActive !== "" && (
        <div style={styles.section}>
          {elevesFiltres.length === 0 ? (
            <p>Aucun élève trouvé.</p>
          ) : (
            elevesFiltres.map((eleve) => (
              <button
                key={eleve.id}
                onClick={() => choisirEleve(eleve)}
                style={styles.btnViolet}
              >
                {eleve.nom}
              </button>
            ))
          )}
        </div>
      )}

      {eleveSelectionne && (
        <>
          <div style={styles.section}>
            <h3 style={styles.sousTitre}>
              Absences de {eleveSelectionne.nom}
            </h3>

            <div style={styles.boutons}>
              <button
                style={styles.btnViolet}
                onClick={() => changerFiltre("toutes")}
              >
                Toutes
              </button>

              <button
                style={styles.btnViolet}
                onClick={() => changerFiltre("justifiees")}
              >
                Justifiées
              </button>

              <button
                style={styles.btnViolet}
                onClick={() => changerFiltre("non_justifiees")}
              >
                Non justifiées
              </button>
            </div>

            <p>
              Nombre d'absences : <b>{absences.length}</b>
            </p>

            {message && (
              <div style={styles.succes}>
                ✅ {message}
              </div>
            )}
          </div>

          <div style={styles.section}>
            {absences.length === 0 ? (
              <p>Aucune absence trouvée.</p>
            ) : (
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Matière</th>
                    <th>Justification</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  {absences.map((absence) => (
                    <tr key={absence.id}>
                      <td>{absence.date}</td>
                      <td>{absence.matiere}</td>
                      <td>
                        {absence.justifiee
                          ? "✅ Justifiée"
                          : "❌ Non justifiée"}
                      </td>
                      <td>
                        <button
                          onClick={() =>
                            supprimerAbsence(absence.id)
                          }
                          style={styles.btnSupprimer}
                        >
                          🗑 Supprimer
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </div>
  );
}
const styles = {
  container: {
    maxWidth: "800px",
    padding: "32px",
  },

  titre: {
    fontSize: "22px",
    fontWeight: "bold",
    marginBottom: "4px",
  },

  sous: {
    color: "#64748b",
    marginBottom: "24px",
    fontSize: "14px",
  },

  section: {
    background: "#f1f5f9",
    padding: "16px",
    borderRadius: "8px",
    marginTop: "16px",
  },

  sousTitre: {
    fontSize: "16px",
    fontWeight: "bold",
    marginBottom: "12px",
    marginTop: 0,
  },

  input: {
    width: "100%",
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #cbd5e1",
    fontSize: "14px",
  },

  boutons: {
    display: "flex",
    gap: "10px",
    marginBottom: "16px",
    flexWrap: "wrap",
  },

  btnViolet: {
    padding: "10px 16px",
    borderRadius: "6px",
    border: "none",
    background: "#9235c8",
    color: "white",
    cursor: "pointer",
    fontWeight: "bold",
  },

  succes: {
    background: "#dcfce7",
    color: "#16a34a",
    padding: "12px",
    borderRadius: "8px",
    marginTop: "12px",
  },

  table: {
    width: "100%",
    borderCollapse: "collapse",
  },

  btnSupprimer: {
    background: "none",
    border: "none",
    color: "#ef4444",
    cursor: "pointer",
    fontWeight: "bold",
  },
};


export default ConsulterAbsences;