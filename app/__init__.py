# __init__.py  - based on various tutorials 
from flask import Flask, render_template, request, jsonify

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)   # create a Flask object


# Configure database using SQLAlchemy
app.config.from_object(Config)  # configure app (Flask object)
db = SQLAlchemy(app)            # Create db - an SQLAlchemy object
migrate = Migrate(app, db)

from app import models

# Test db - in-memory
countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

# Helper functions
def _find_next_id():
    return max(country["id"] for country in countries) + 1



# View functions

@app.route("/")
def home():
    return render_template("home.html")


@app.get("/countries")
def get_countries():
    return jsonify(countries)

@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

# For newer Mac OS versions, port 5000 is already used - change to port 8000
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8000, debug=True)
