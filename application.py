from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route("/")
def index():
    return "Hello!"


@app.route("/drinks")
def get_drinks():
    drinks = Drink.query.all()

    output = [
        {"name": drink.name, "description": drink.description} for drink in drinks
    ]
    return {"drinks": output}


@app.route("/drinks/<id>")
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}


@app.route("/drinks", methods=["POST"])
def add_drink():
    drink = Drink(name=request.json["name"], description=request.json["description"])
    db.session.add(drink)
    db.session.commit()
    return {"id": drink.id}


@app.route("/drinks/<id>", methods=["DELETE"])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "drink not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "the drink was successfully deleted."}


@app.route("/drinks/<id>", methods=["PUT"])
def edit_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "No drink found"}, 404

    # Check if the new name already exists and is not the current drink
    new_name = request.json["name"]
    existing_drink = Drink.query.filter_by(name=new_name).first()
    if existing_drink and existing_drink.id != drink.id:
        return {"error": f"Drink with name '{new_name}' already exists."}, 400

    drink.name = new_name
    drink.description = request.json["description"]

    db.session.commit()
    return {"message": "Drink updated successfully", "id": drink.id}
