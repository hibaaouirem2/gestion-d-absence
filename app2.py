
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. STOCKAGE DES DONNEES EN MEMOIRE
# Chaque élève est représenté par un dictionnaire.
eleves = []

# Chaque absence est représentée par un dictionnaire.
absences = []

# Compteurs utilisés pour attribuer des identifiants uniques.
prochain_id_eleve = 1
prochain_id_absence = 1

# 2. FONCTIONS POUR LES ELEVES

def rechercher_eleve(nom_recherche):
    #Recherche les élèves dont le nom contient le texte saisi.

    resultats = []

    for eleve in eleves:
        if nom_recherche.lower() in eleve["nom"].lower():
            resultats.append(eleve)

    return resultats


def trouver_eleve(eleve_id):
    #Retourne un élève à partir de son identifiant.

    for eleve in eleves:
        if eleve["id"] == eleve_id:
            return eleve

    return None


# 3. FONCTIONS POUR LES ABSENCES


def obtenir_absences_eleve(eleve_id):
    #Retourne toutes les absences d'un élève.

    resultats = []

    for absence in absences:
        if absence["eleve_id"] == eleve_id:
            resultats.append(absence)

    return resultats


def filtrer_absences(absences_eleve, filtre):
    #Filtre les absences selon leur justification.

    if filtre == "toutes":
        return absences_eleve

    resultats = []

    for absence in absences_eleve:
        if filtre == "justifiees" and absence["justifiee"] is True:
            resultats.append(absence)

        elif filtre == "non_justifiees" and absence["justifiee"] is False:
            resultats.append(absence)

    return resultats



# 4. CONSULTER ET RECHERCHER LES ELEVES


@app.route("/eleves", methods=["GET"])
def liste_eleves():
    #Retourne la liste de tous les élèves.
    return jsonify(eleves), 200


@app.route("/eleves/recherche", methods=["GET"])
def recherche_eleve():
    """Recherche un élève à partir de son nom."""

    nom = request.args.get("nom", "")
    resultats = rechercher_eleve(nom)

    return jsonify(resultats), 200



# 5. AJOUTER UN ELEVE


@app.route("/eleves", methods=["POST"])
def ajouter_eleve():
    global prochain_id_eleve

    data = request.get_json(silent=True) or {}
    nom = data.get("nom", "").strip()

    if not nom:
        return jsonify({
            "message": "Le nom de l'élève est obligatoire."
        }), 400

    eleve = {
        "id": prochain_id_eleve,
        "nom": nom
    }

    eleves.append(eleve)
    prochain_id_eleve += 1

    return jsonify({
        "message": "Élève ajouté avec succès.",
        "eleve": eleve
    }), 201


# 6. CONSULTER LES ABSENCES D'UN ELEVE


@app.route("/eleves/<int:eleve_id>/absences", methods=["GET"])
def consulter_absences(eleve_id):
    """Retourne les absences d'un élève, avec un filtre facultatif."""

    eleve = trouver_eleve(eleve_id)

    if eleve is None:
        return jsonify({
            "message": "Élève non trouvé."
        }), 404

    absences_eleve = obtenir_absences_eleve(eleve_id)

    filtre = request.args.get("filtre", "toutes")

    if filtre not in ["toutes", "justifiees", "non_justifiees"]:
        return jsonify({
            "message": "Filtre invalide."
        }), 400

    resultats = filtrer_absences(absences_eleve, filtre)

    return jsonify(resultats), 200


# ==================================================
# 7. AJOUTER UNE ABSENCE
# ==================================================

@app.route("/absences", methods=["POST"])
def ajouter_absence():
    global prochain_id_absence

    data = request.get_json(silent=True) or {}

    # Vérifier la présence des informations nécessaires.
    if not all(cle in data for cle in
               ["eleve_id", "date", "matiere", "justifiee"]):
        return jsonify({
            "message": "Informations d'absence incomplètes."
        }), 400

    try:
        eleve_id = int(data["eleve_id"])
    except (ValueError, TypeError):
        return jsonify({
            "message": "Identifiant d'élève invalide."
        }), 400

    eleve = trouver_eleve(eleve_id)

    if eleve is None:
        return jsonify({
            "message": "Élève non trouvé."
        }), 404

    date = data["date"]
    matiere = data["matiere"]
    justifiee = data["justifiee"]

    if not isinstance(date, str) or not date.strip():
        return jsonify({"message": "Date obligatoire."}), 400

    if not isinstance(matiere, str) or not matiere.strip():
        return jsonify({"message": "Matière obligatoire."}), 400

    # Refuser les valeurs autres que True ou False.
    if not isinstance(justifiee, bool):
        return jsonify({
            "message": "La justification doit être vraie ou fausse."
        }), 400

    absence = {
        "id": prochain_id_absence,
        "eleve_id": eleve_id,
        "date": date,
        "matiere": matiere.strip(),
        "justifiee": justifiee
    }

    absences.append(absence)
    prochain_id_absence += 1

    return jsonify({
        "message": "Absence enregistrée avec succès.",
        "absence": absence
    }), 201



# 8. SUPPRIMER UNE ABSENCE


@app.route("/absences/<int:absence_id>", methods=["DELETE"])
def supprimer_absence(absence_id):
    """Supprime une absence à partir de son identifiant."""

    for absence in absences:
        if absence["id"] == absence_id:
            absences.remove(absence)

            return jsonify({
                "message": "Absence supprimée avec succès."
            }), 200

    return jsonify({
        "message": "Absence non trouvée."
    }), 404



# 9. LANCEMENT DU SERVEUR


if __name__ == "__main__":
    app.run(debug=True, port=5001)
```
