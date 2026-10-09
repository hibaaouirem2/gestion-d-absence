from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///absences.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Etudiant(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nom": self.nom}

class Absence(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    etudiant_id  = db.Column(db.Integer, db.ForeignKey('etudiant.id'), nullable=False)
    date      = db.Column(db.String(20), nullable=False)
    matiere   = db.Column(db.String(100), nullable=False)
    justifiee = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id":        self.id,
            "etudiant_id":  self.etudiant_id,
            "date":      self.date,
            "matiere":   self.matiere,
            "justifiee": self.justifiee
        }
# ==========================
#  Nouvelle Absence
# ==========================
@app.route('/etudiants', methods=['GET'])
def liste_etudiants():
    etudiants = Etudiant.query.all()
    return jsonify([e.to_dict() for e in etudiants])

@app.route('/etudiants/<int:id>', methods=['DELETE'])
def supprimer_etudiant(id):
    etudiant = Etudiant.query.get(id)
    if etudiant is None:
        return jsonify({"message": "Etudiant non trouve"}), 404
    db.session.delete(etudiant)
    db.session.commit()
    return jsonify({"message": "Etudiant supprimé"}), 200

@app.route('/etudiants', methods=['POST'])
def ajouter_etudiant():
    data  = request.json
    etudiant = Etudiant(nom=data["nom"])
    db.session.add(etudiant)
    db.session.commit()
    return jsonify({"message": "Etudiant ajoute", "etudiant": etudiant.to_dict()}), 201

@app.route('/absences', methods=['POST'])
def ajouter_absence():
    data    = request.json
    absence = Absence(
        etudiant_id  = data["etudiant_id"],
        date      = data["date"],
        matiere   = data["matiere"],
        justifiee = data["justifiee"]
    )
    db.session.add(absence)
    db.session.commit()
    return jsonify({"message": "Absence enregistree", "absence": absence.to_dict()}), 201



# ============================================================
# CONSULTER LES ABSENCES D'UN ÉLÈVE
# ============================================================
def obtenir_absences_etudiant(etudiant_id):
    toutes_les_absences = Absence.query.all()
    absences_etudiant = []
    # Parcourir toutes les absences
    for absence in toutes_les_absences:
        # Vérifier si l'absence appartient à l'élève recherché
        if absence.etudiant_id == etudiant_id:
            # Transformer l'absence en dictionnaire
            dictionnaire = absence.to_dict()
            # Ajouter l'absence à notre liste
            absences_etudiant.append(dictionnaire)
    # Retourner les absences de l'élève
    return absences_etudiant

def filtrer_absences(absences, filtre):
    # CAS 1 : L'utilisateur veut toutes les absences
    if filtre == "toutes":
        # On retourne directement la liste
        return absences
    # CAS 2 ET 3 : L'utilisateur veut un filtre
    resultats = []
    # Parcourir toutes les absences
    for absence in absences:
        # Absence justifiée
        if (
            filtre == "justifiees"
            and absence["justifiee"] is True
        ):
            # Ajouter l'absence à la liste
            resultats.append(absence)
        # Absence non justifiée
        elif (
            filtre == "non_justifiees"
            and absence["justifiee"] is False
        ):
            # Ajouter l'absence à la liste
            resultats.append(absence)
    # Retourner les résultats filtrés
    return resultats



@app.route(
    '/etudiants/<int:etudiant_id>/absences',
    methods=['GET']
)
def consulter_absences(etudiant_id):
    # Vérifier que l'élève existe
    etudiant = Etudiant.query.get(etudiant_id)
    # Si l'élève n'existe pas
    if etudiant is None:
        return jsonify({
            "message": "Etudiant non trouve"
        }), 404
    # Récupérer les absences de l'élève
    absences = obtenir_absences_etudiant(
        etudiant_id
    )
    # Récupérer le filtre envoyé par React
    # Si aucun filtre n'est fourni, on utilise "toutes".
    filtre = request.args.get(
        'filtre',
        'toutes'
    )
    # Appliquer le filtre
    absences_filtrees = filtrer_absences(
        absences,
        filtre
    )
    # Envoyer les résultats à React
    return jsonify(
        absences_filtrees
    ), 200
# ============================================================
# ROUTE 4 : SUPPRIMER UNE ABSENCE
# ============================================================

@app.route(
    '/absences/<int:absence_id>',
    methods=['DELETE']
)
def supprimer_absence(absence_id):
    # Chercher l'absence grâce à son identifiant
    absence = Absence.query.get(absence_id)
    # Vérifier que l'absence existe
    if absence is None:
        return jsonify({
            "message": "Absence non trouvee"
        }), 404
    # Supprimer l'absence
    db.session.delete(absence)
    # Enregistrer la suppression dans la base
    db.session.commit()
    # Envoyer une confirmation à React
    return jsonify({
        "message": "Absence supprimée"
    }), 200

# ============================================================
# Tableau de bord 
# ============================================================

def absences_par_matiere():
    resultat = {}
    donnees = db.session.query(
        Absence.matiere,
        func.count(Absence.id)
    ).group_by(Absence.matiere).all()

    for matiere, nb_absences in donnees:
        resultat[matiere] = nb_absences

    return resultat

def total_absences():
    return Absence.query.count()

def etudiant_plus_absent():
    resultat = (
        db.session.query(
            Etudiant.nom,
            func.count(Absence.id).label("nb_absences")
        )
        .join(Absence, Etudiant.id == Absence.etudiant_id)
        .group_by(Etudiant.id)
        .order_by(func.count(Absence.id).desc())
        .first()
    )

    if resultat is None:
        return None

    return {
        "nom": resultat.nom,
        "nb_absences": resultat.nb_absences
    }
def taux_par_matiere(nb_etudiants, seances_par_matiere):
    resultat = []

    absences_matiere = absences_par_matiere()

    for matiere, nb_seances in seances_par_matiere.items():

        nb_abs = absences_matiere.get(matiere, 0)

        possible = nb_etudiants * nb_seances

        if possible == 0:
            taux = 0
        else:
            taux = round((nb_abs / possible) * 100, 1)

        resultat.append({
            "matiere": matiere,
            "taux": taux
        })

    return resultat

def taux_global(nb_etudiants, seances_par_matiere):

    total = total_absences()

    possible = nb_etudiants * sum(seances_par_matiere.values())

    if possible == 0:
        return 0

    return round((total / possible) * 100, 1)

def calculer_stats():
    nb_etudiants = Etudiant.query.count()

    seances_par_matiere = absences_par_matiere()

    return {
        "etudiant_plus_absent": etudiant_plus_absent(),
        "taux_global": taux_global(nb_etudiants, seances_par_matiere),
        "total_absences": total_absences(),
        "par_matiere": taux_par_matiere(nb_etudiants, seances_par_matiere)
    }

@app.route("/stats", methods=["GET"])
def stats():
    return jsonify(calculer_stats())

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)