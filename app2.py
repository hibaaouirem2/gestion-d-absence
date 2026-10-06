# Partie 2 : CONSULTATION ET RECHERCHE

# 1. IMPORTATION DES BIBLIOTHÈQUES
# Flask permet de créer notre serveur web
from flask import Flask, request, jsonify
# CORS permet à React de communiquer avec Flask
from flask_cors import CORS
# SQLAlchemy permet de travailler avec la base de données
from flask_sqlalchemy import SQLAlchemy

# ============================================================
# 2. CRÉATION DE L'APPLICATION FLASK
# ============================================================

app = Flask(__name__)

# Autoriser les requêtes provenant de React
CORS(app)
# ============================================================
# 3. CONFIGURATION DE LA BASE DE DONNÉES
# ============================================================

# On utilise la base de données du projet
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///absences.db'

# Désactiver le suivi inutile des modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Créer l'objet permettant de communiquer avec SQLite
db = SQLAlchemy(app)


# ============================================================
# 4. MODÈLE ELEVE
# ============================================================

# Cette classe représente la table "eleve"
class Eleve(db.Model):

    # Identifiant unique de l'élève
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Nom de l'élève
    nom = db.Column(
        db.String(100),
        nullable=False
    )


    # --------------------------------------------------------
    # Transformer un élève en dictionnaire
    # --------------------------------------------------------

    def to_dict(self):

        return {
            "id": self.id,
            "nom": self.nom
        }


# ============================================================
# 5. MODÈLE ABSENCE
# ============================================================

# Cette classe représente la table "absence"
class Absence(db.Model):

    # Identifiant unique de l'absence
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Identifiant de l'élève concerné
    eleve_id = db.Column(
        db.Integer,
        db.ForeignKey('eleve.id'),
        nullable=False
    )

    # Date de l'absence
    date = db.Column(
        db.String(20),
        nullable=False
    )

    # Matière dans laquelle l'élève était absent
    matiere = db.Column(
        db.String(100),
        nullable=False
    )

    # True  → absence justifiée
    # False → absence non justifiée
    justifiee = db.Column(
        db.Boolean,
        nullable=False
    )


    # --------------------------------------------------------
    # Transformer une absence en dictionnaire
    # --------------------------------------------------------

    def to_dict(self):

        return {
            "id": self.id,
            "eleve_id": self.eleve_id,
            "date": self.date,
            "matiere": self.matiere,
            "justifiee": self.justifiee
        }


# ============================================================
# PARTIE PERSONNE 2
# ============================================================
#
# Notre travail consiste à :
#
# 1. Récupérer la liste des élèves
# 2. Rechercher un élève
# 3. Consulter les absences d'un élève
# 4. Filtrer les absences
# 5. Supprimer une absence
#
# ============================================================


# ============================================================
# ROUTE 1 : RÉCUPÉRER TOUS LES ÉLÈVES
# ============================================================

@app.route('/eleves', methods=['GET'])
def liste_eleves():

    # Récupérer tous les élèves présents
    # dans la base de données
    eleves = Eleve.query.all()


    # Liste vide qui va contenir les résultats
    resultats = []


    # Parcourir tous les élèves
    for eleve in eleves:

        # Transformer l'élève en dictionnaire
        dictionnaire = eleve.to_dict()

        # Ajouter le dictionnaire à notre liste
        resultats.append(dictionnaire)


    # Envoyer la liste au format JSON
    # vers React
    return jsonify(resultats), 200


# ============================================================
# FONCTION : RECHERCHER UN ÉLÈVE
# ============================================================

def rechercher_eleve(nom_recherche):

    # Récupérer tous les élèves
    eleves = Eleve.query.all()


    # Liste vide pour stocker les résultats
    resultats = []


    # Parcourir tous les élèves
    for eleve in eleves:

        # lower() transforme le texte en minuscules
        #
        # Exemple :
        # "Ahmed" devient "ahmed"
        #
        # Cela permet d'effectuer une recherche
        # sans tenir compte des majuscules/minuscules.
        nom_eleve = eleve.nom.lower()
        recherche = nom_recherche.lower()


        # Vérifier si le texte recherché
        # se trouve dans le nom de l'élève
        #
        # Exemple :
        # recherche = "ahm"
        # nom = "Ahmed"
        #
        # "ahm" est bien présent dans "ahmed"
        if recherche in nom_eleve:

            # Ajouter l'élève trouvé
            resultats.append(eleve.to_dict())


    # Retourner la liste des résultats
    return resultats


# ============================================================
# ROUTE 2 : RECHERCHER UN ÉLÈVE
# ============================================================

@app.route('/eleves/recherche', methods=['GET'])
def recherche_eleve():

    # Récupérer le paramètre "nom" envoyé par React
    # request.args permet de récupérer
    # les paramètres présents dans l'URL.
    nom = request.args.get(
        'nom',
        ''
    )

    # Appeler notre fonction de recherche
    resultats = rechercher_eleve(nom)


    # Retourner les résultats à React
    return jsonify(resultats), 200


# ============================================================
# FONCTION : RÉCUPÉRER LES ABSENCES D'UN ÉLÈVE
# ============================================================

def obtenir_absences_eleve(eleve_id):

    # Récupérer toutes les absences
    toutes_les_absences = Absence.query.all()


    # Liste vide pour stocker
    # uniquement les absences de l'élève
    absences_eleve = []


    # Parcourir toutes les absences
    for absence in toutes_les_absences:

        # Vérifier si l'absence appartient à l'élève recherché
        if absence.eleve_id == eleve_id:

            # Transformer l'absence en dictionnaire
            dictionnaire = absence.to_dict()

            # Ajouter l'absence à notre liste
            absences_eleve.append(dictionnaire)


    # Retourner les absences de l'élève
    return absences_eleve


# ============================================================
# FONCTION : FILTRER LES ABSENCES
# ============================================================

def filtrer_absences(absences, filtre):

    # --------------------------------------------------------
    # CAS 1 : L'utilisateur veut toutes les absences
    # --------------------------------------------------------

    if filtre == "toutes":

        # On retourne directement la liste
        return absences


    # --------------------------------------------------------
    # CAS 2 ET 3 : L'utilisateur veut un filtre
    # --------------------------------------------------------

    # Liste vide pour les résultats
    resultats = []


    # Parcourir toutes les absences
    for absence in absences:

        # ----------------------------------------------------
        # Absence justifiée
        # ----------------------------------------------------

        if (
            filtre == "justifiees"
            and absence["justifiee"] is True
        ):

            # Ajouter l'absence à la liste
            resultats.append(absence)


        # ----------------------------------------------------
        # Absence non justifiée
        # ----------------------------------------------------

        elif (
            filtre == "non_justifiees"
            and absence["justifiee"] is False
        ):

            # Ajouter l'absence à la liste
            resultats.append(absence)


    # Retourner les résultats filtrés
    return resultats


# ============================================================
# ROUTE 3 : CONSULTER LES ABSENCES D'UN ÉLÈVE
# ============================================================

@app.route(
    '/eleves/<int:eleve_id>/absences',
    methods=['GET']
)
def consulter_absences(eleve_id):

    # --------------------------------------------------------
    # Vérifier que l'élève existe
    # --------------------------------------------------------

    eleve = Eleve.query.get(eleve_id)


    # Si l'élève n'existe pas
    if eleve is None:

        return jsonify({
            "message": "Eleve non trouve"
        }), 404


    # --------------------------------------------------------
    # Récupérer les absences de l'élève
    # --------------------------------------------------------

    absences = obtenir_absences_eleve(
        eleve_id
    )


    # --------------------------------------------------------
    # Récupérer le filtre envoyé par React
    # --------------------------------------------------------
    # Si aucun filtre n'est fourni, on utilise "toutes".
    filtre = request.args.get(
        'filtre',
        'toutes'
    )


    # --------------------------------------------------------
    # Appliquer le filtre
    # --------------------------------------------------------

    absences_filtrees = filtrer_absences(
        absences,
        filtre
    )


    # --------------------------------------------------------
    # Envoyer les résultats à React
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Vérifier que l'absence existe
    # --------------------------------------------------------

    if absence is None:

        return jsonify({
            "message": "Absence non trouvee"
        }), 404


    # --------------------------------------------------------
    # Supprimer l'absence
    # --------------------------------------------------------

    db.session.delete(absence)


    # Enregistrer la suppression dans la base
    db.session.commit()


    # --------------------------------------------------------
    # Envoyer une confirmation à React
    # --------------------------------------------------------

    return jsonify({
        "message": "Absence supprimee"
    }), 200


# ============================================================
# 6. CRÉATION DES TABLES
# ============================================================

# Ouvrir le contexte de l'application Flask
with app.app_context():

    # Créer les tables si elles n'existent pas.
    #
    # Si elles existent déjà,
    # elles ne sont pas supprimées.
    db.create_all()


# ============================================================
# 7. LANCEMENT DU SERVEUR
# ============================================================

if __name__ == '__main__':

    # Lancer Flask sur le port 5001
    #
    # Personne 1 peut utiliser le port 5000.
    # Toi, tu utilises le port 5001.
    app.run(
        debug=True,
        port=5001
    )
