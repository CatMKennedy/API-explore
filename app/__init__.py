# __init__.py  - based on various tutorials 
from flask import Flask, render_template, request, json, jsonify, url_for

from werkzeug.http import HTTP_STATUS_CODES  #to be moved to error module

import sqlalchemy as sa

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# TO DO - refactor - use blueprints, add error handling

app = Flask(__name__)   # create a Flask object

# Configure database using SQLAlchemy
app.config.from_object(Config)  
db = SQLAlchemy(app)            # Create db 
migrate = Migrate(app, db)

from app import models
from app.models import Country


# Initial data for testing
countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]


# Helper functions
def _find_next_id():
    return max(country["id"] for country in countries) + 1

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code


# View functions - just for testing

@app.route("/")
def home():
    #name1=request.args.get('name')
    return render_template("home.html", name=request.args.get('name'))


# API functions - still very messy

@app.get('/countries/all')   # get all countries
def get_countries():
    query = sa.select(Country)
    countries = db.session.scalars(query).all()
    results = []
    for c in countries:  # change each item to dict
        results.append(c.to_dict())

    return jsonify(results)


@app.get('/countries/')   # /countries/?country=<name>
def get_country():
    print(f"Request.args = {request.args}")
    country = request.args.get('country') 
    print(f"country = {country}")
    data = db.session.scalar(sa.select(Country).where(
            Country.name == country))
    print(f"data = {data}")
    if data != None:
        results = data.to_dict()
        return jsonify(results)
    else:
        return error_response(400, f"Country {country} not found in database")



@app.post('/countries')
def create_country():   # TO DO - needs improving
    data = request.get_json()

    if 'name' not in data or 'capital' not in data or 'area' not in data:
        return error_response(400, 'must include name, capital and area fields')
    if db.session.scalar(sa.select(Country).where(
            Country.name == data['name'])):
        return error_response(400, 'Country already in database, please add a different one')
    if db.session.scalar(sa.select(Country).where(
            Country.capital == data['capital'])):
        return error_response(400, 'Capital already exists, please add a different one')

    c = Country()
    c.from_dict(data)
    db.session.add(c)
    db.session.commit()
    return c.to_dict(), 201
#{'Location': url_for('get_country', id=c.id)}


# Alternatives - using dictonary

'''
@app.get("/country")
def get_country():
    return countries[1]

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
'''

# If required:
# for newer Mac OS versions, port 5000 is already used - change to port 8000
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8000, debug=True)
