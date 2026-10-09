from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# ==========================
# CLASSES
# ==========================

class Etudiant:
    def __init__(self, id, nom,):
        self.id = id
        self.nom = nom
       


    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom, 
      
        }


class Absence:
    def __init__(self, id, etudiant_id, date, matiere, justifiee):
        self.id = id
        self.etudiant_id = etudiant_id
        self.date = date
        self.matiere = matiere
        self.justifiee = justifiee

    def to_dict(self):
        return {
            "id": self.id,
            "etudiant_id": self.etudiant_id,
            "date": self.date,
            "matiere": self.matiere,
            "justifiee": self.justifiee
        }


# ==========================
# LISTES D'OBJETS 
# Initilisation des données 
# ==========================

etudiants = [
    Etudiant(1, "Hiba Aouirem"),
    Etudiant(2, "Sara toto"),
    Etudiant(3, "Yassine toto"),
    Etudiant(4, "Yassine 2"),

]

absences = [
    Absence(1, 1, "2026-10-01", "Structures de Donéees", False),
    Absence(2, 3, "2026-10-02", "Academic English", True),
    Absence(3, 3, "2026-10-02", "Academic English", True)

]


# ==========================
#  Nouvelle Absence
# ==========================

@app.route("/etudiants", methods=["GET"])
def liste_etudiants():
    liste_etudiants = []
    for etudiant in etudiants:
        liste_etudiants.append(etudiant.to_dict())

    return jsonify(liste_etudiants)


@app.route("/etudiants", methods=["POST"])
def ajouter_etudiant():

    data = request.json

    nouvel_id = 1

    if etudiants:
        ids = []
    
        for etudiant in etudiants:
            ids.append(etudiant.id)
        
        nouvel_id = max(ids) + 1

    etudiant = Etudiant(
        nouvel_id,
        data["nom"]
    )

    etudiants.append(etudiant)

    return jsonify({
        "message": "Etudiant ajoute",
        "etudiant": etudiant.to_dict()
    }), 201


@app.route("/etudiants/<int:id>", methods=["DELETE"])
def supprimer_etudiant(id):

    for etudiant in etudiants:

        if etudiant.id == id:

            etudiants.remove(etudiant)

            return jsonify({
                "message": "Etudiant supprimé"
            })

    return jsonify({
        "message": "Etudiant non trouve"
    }), 404


@app.route("/absences", methods=["POST"])
def ajouter_absence():

    data = request.json

    nouvel_id = 1

    if absences:
        ids = []
    
        for absence in absences:
            ids.append(absence.id)
        
        nouvel_id = max(ids) + 1

    absence = Absence(
        nouvel_id,
        data["etudiant_id"],
        data["date"],
        data["matiere"],
        data["justifiee"]
    )

    absences.append(absence)

    return jsonify({
        "message": "Absence enregistree",
        "absence": absence.to_dict()
    }), 201


@app.route("/absences", methods=["GET"])
def liste_absences():
    liste_absences = []
    for absence in absences:
        liste_absences.append(absence.to_dict())

    return jsonify(liste_absences)

# ============================================================
# CONSULTER LES ABSENCES D'UN ÉLÈVE
# ============================================================

def obtenir_absences_etudiant(etudiant_id):
    resultat = []

    for absence in absences:
        if absence.etudiant_id == etudiant_id:
            resultat.append(absence.to_dict())

    return resultat
def filtrer_absences(absences_etudiant, filtre):

    if filtre == "toutes":
        return absences_etudiant

    resultat = []

    for absence in absences_etudiant:

        if filtre == "justifiees":
            if absence["justifiee"] == True:
                resultat.append(absence)

        elif filtre == "non_justifiees":
            if absence["justifiee"] == False:
                resultat.append(absence)

    return resultat

@app.route(
    '/etudiants/<int:etudiant_id>/absences',
    methods=['GET']
)
def consulter_absences(etudiant_id):

    etudiant = None

    for e in etudiants:
        if e.id == etudiant_id:
            etudiant = e

    if etudiant is None:
        return jsonify({
            "message": "Etudiant non trouve"
        }), 404

    filtre = request.args.get(
        'filtre',
        'toutes'
    )

    resultat = []

    for absence in absences:

        if absence.etudiant_id == etudiant_id:

            if filtre == "toutes":
                resultat.append(absence.to_dict())

            elif filtre == "justifiees" and absence.justifiee:
                resultat.append(absence.to_dict())

            elif filtre == "non_justifiees" and not absence.justifiee:
                resultat.append(absence.to_dict())

    return jsonify(resultat), 200

@app.route(
    '/absences/<int:absence_id>',
    methods=['DELETE']
)
def supprimer_absence(absence_id):

    absence_a_supprimer = None

    for absence in absences:
        if absence.id == absence_id:
            absence_a_supprimer = absence

    if absence_a_supprimer is None:
        return jsonify({
            "message": "Absence non trouvee"
        }), 404

    absences.remove(absence_a_supprimer)

    return jsonify({
        "message": "Absence supprimee"
    }), 200

    
# ==========================
#  Tableau de Bord 
# ==========================
def absences_par_matiere(absences):
    resultat = {}

    for absence in absences:
        matiere = absence.matiere

        if matiere not in resultat:
            resultat[matiere] = 0

        resultat[matiere] += 1
    print(resultat)
    return resultat

def total_absences(absences):
    """Nombre total d'absences."""
    return len(absences)

def etudiant_plus_absent(etudiants, absences):
    if len(absences) == 0:
        return None

    list1 = []

    for absence in absences:
        list1.append(absence.etudiant_id)

    maxi1 = 0  # nb d'absences max
    maxi2 = 0  # id de l'étudiant

    for id_etudiant in list1:
        nb = list1.count(id_etudiant)

        if nb > maxi1:
            maxi1 = nb
            maxi2 = id_etudiant

    for etudiant in etudiants:
        if etudiant.id == maxi2:
            return {
                "nom": etudiant.nom,
                "nb_absences": maxi1
            }

    return None

def taux_par_matiere(absences, nb_etudiants, seances_par_matiere):
    """Renvoie [{"matiere": ..., "taux": ...}, ...] en pourcentage."""
    resultat = []
    for matiere, nb_seances in seances_par_matiere.items():
        nb_abs = 0
        for a in absences:
            if a.matiere== matiere:
                nb_abs += 1
        possible = nb_etudiants * nb_seances
        if possible == 0:
            taux = 0
        else:
            taux = round(nb_abs / possible * 100, 1)
        resultat.append({"matiere": matiere, "taux": taux})
    return resultat

def taux_global(absences, nb_etudiants, seances_par_matiere):
    """Taux d'absence global en pourcentage."""
    possible = nb_etudiants * sum(seances_par_matiere.values())
    if possible == 0:
        return 0
    return round(len(absences) / possible * 100, 1)

def calculer_stats(etudiants, absences, seances_par_matiere):
    """Regroupe tous les calculs dans un seul dictionnaire."""
    nb_etudiants = len(etudiants)
    return {
        "etudiant_plus_absent": etudiant_plus_absent(etudiants, absences),
        "taux_global": taux_global(absences, nb_etudiants, seances_par_matiere),
        "total_absences": total_absences(absences),
        "par_matiere": taux_par_matiere(absences, nb_etudiants, seances_par_matiere),
    }

@app.route("/stats", methods=["GET"])
def stats():
        seances_par_matiere= absences_par_matiere(absences)
        return jsonify(calculer_stats(etudiants, absences, seances_par_matiere))

if __name__ == "__main__":
    app.run(debug=True)