from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///absences.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Eleve(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nom": self.nom}

class Absence(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    eleve_id  = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    date      = db.Column(db.String(20), nullable=False)
    matiere   = db.Column(db.String(100), nullable=False)
    justifiee = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id":        self.id,
            "eleve_id":  self.eleve_id,
            "date":      self.date,
            "matiere":   self.matiere,
            "justifiee": self.justifiee
        }

@app.route('/eleves', methods=['GET'])
def liste_eleves():
    eleves = Eleve.query.all()
    return jsonify([e.to_dict() for e in eleves])

@app.route('/eleves/<int:id>', methods=['DELETE'])
def supprimer_eleve(id):
    eleve = Eleve.query.get(id)
    if eleve is None:
        return jsonify({"message": "Eleve non trouve"}), 404
    db.session.delete(eleve)
    db.session.commit()
    return jsonify({"message": "Eleve supprime"}), 200

@app.route('/eleves', methods=['POST'])
def ajouter_eleve():
    data  = request.json
    eleve = Eleve(nom=data["nom"])
    db.session.add(eleve)
    db.session.commit()
    return jsonify({"message": "Eleve ajoute", "eleve": eleve.to_dict()}), 201

@app.route('/absences', methods=['POST'])
def ajouter_absence():
    data    = request.json
    absence = Absence(
        eleve_id  = data["eleve_id"],
        date      = data["date"],
        matiere   = data["matiere"],
        justifiee = data["justifiee"]
    )
    db.session.add(absence)
    db.session.commit()
    return jsonify({"message": "Absence enregistree", "absence": absence.to_dict()}), 201


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)