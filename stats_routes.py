from flask import jsonify

# À valider avec le groupe : noms EXACTS des matières (accents, majuscules)
SEANCES_PAR_MATIERE = {"Mathématiques": 20, "Physique": 20, "Anglais": 10}


def total_absences(absences):
    """Nombre total d'absences."""
    return len(absences)


def eleve_plus_absent(eleves, absences):
    """Renvoie l'élève le plus absent (ou None s'il n'y a aucune absence)."""
    if len(absences) == 0:
        return None

    list1 = []
    for i in absences:
        list1.append(i["eleve_id"])
    maxi1 = 0
    maxi2 = 0
    for i in list1:
        if list1.count(i) > maxi1:
            maxi1 = list1.count(i)
            maxi2 = i

    for i in eleves:
        if i["id"] == maxi2:
            return {"nom": i["nom"], "nb_absences": maxi1}
    return None


def taux_par_matiere(absences, nb_eleves, seances_par_matiere):
    """Renvoie [{"matiere": ..., "taux": ...}, ...] en pourcentage."""
    resultat = []
    for matiere, nb_seances in seances_par_matiere.items():
        nb_abs = 0
        for a in absences:
            if a["matiere"] == matiere:
                nb_abs += 1
        possible = nb_eleves * nb_seances
        if possible == 0:
            taux = 0
        else:
            taux = round(nb_abs / possible * 100, 1)
        resultat.append({"matiere": matiere, "taux": taux})
    return resultat


def taux_global(absences, nb_eleves, seances_par_matiere):
    """Taux d'absence global en pourcentage."""
    possible = nb_eleves * sum(seances_par_matiere.values())
    if possible == 0:
        return 0
    return round(len(absences) / possible * 100, 1)


def calculer_stats(eleves, absences, seances_par_matiere):
    """Regroupe tous les calculs dans un seul dictionnaire."""
    nb_eleves = len(eleves)
    return {
        "eleve_plus_absent": eleve_plus_absent(eleves, absences),
        "taux_global": taux_global(absences, nb_eleves, seances_par_matiere),
        "total_absences": total_absences(absences),
        "par_matiere": taux_par_matiere(absences, nb_eleves, seances_par_matiere),
    }


def register_stats_routes(app, db, Eleve, Absence):
    """Ajoute la route GET /stats à l'application de la collègue."""

    @app.route("/stats", methods=["GET"])
    def stats():
        eleves = [e.to_dict() for e in Eleve.query.all()]
        absences = [a.to_dict() for a in Absence.query.all()]
        return jsonify(calculer_stats(eleves, absences, SEANCES_PAR_MATIERE))