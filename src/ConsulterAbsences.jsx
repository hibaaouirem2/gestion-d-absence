import { useEffect, useState } from "react";

function ConsulterAbsences() {
  const [eleves, setEleves] = useState([]);
  const [eleveSelectionne, setEleveSelectionne] = useState(null);
  const [recherche, setRecherche] = useState("");
  const [absences, setAbsences] = useState([]);
  const [filtre, setFiltre] = useState("toutes");
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://localhost:5001/eleves")
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
      .includes(recherche.toLowerCase());
  });

  const choisirEleve = (eleve) => {
    setEleveSelectionne(eleve);
    setFiltre("toutes");
    setMessage("");
    chargerAbsences(eleve.id, "toutes");
  };

  const chargerAbsences = (eleveId, filtreChoisi) => {
    const url = `http://localhost:5001/eleves/${eleveId}/absences?filtre=${filtreChoisi}`;

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

    fetch(`http://localhost:5001/absences/${absenceId}`, {
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
    <div>
      <h1>Consulter les absences</h1>

      <input
        type="text"
        placeholder="Rechercher un élève..."
        value={recherche}
        onChange={(e) => setRecherche(e.target.value)}
      />

      {recherche !== "" && (
        <div>
          {elevesFiltres.length === 0 ? (
            <p>Aucun élève trouvé.</p>
          ) : (
            elevesFiltres.map((eleve) => (
              <button
                key={eleve.id}
                onClick={() => choisirEleve(eleve)}
              >
                {eleve.nom}
              </button>
            ))
          )}
        </div>
      )}

      {eleveSelectionne !== null && (
        <div>
          <h2>
            Absences de {eleveSelectionne.nom}
          </h2>

          <button onClick={() => changerFiltre("toutes")}>
            Toutes
          </button>

          <button onClick={() => changerFiltre("justifiees")}>
            Justifiées
          </button>

          <button onClick={() => changerFiltre("non_justifiees")}>
            Non justifiées
          </button>

          <p>
            Nombre d'absences : {absences.length}
          </p>

          {message !== "" && (
            <p>{message}</p>
          )}

          {absences.length === 0 ? (
            <p>Aucune absence pour ce filtre.</p>
          ) : (
            <table>
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
                        ? "Justifiée"
                        : "Non justifiée"}
                    </td>
                    <td>
                      <button
                        onClick={() =>
                          supprimerAbsence(absence.id)
                        }
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
export default ConsulterAbsences;
