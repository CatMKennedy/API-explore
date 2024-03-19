# __init__.py  
from flask import Flask, render_template, request, json, jsonify, url_for

from werkzeug.http import HTTP_STATUS_CODES  #to be moved to error module

import sqlalchemy as sa

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# TO DO - refactor - use blueprints, add tests and error handling

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

@app.get('/countries/<int:id>')   # Retrieve a country using id (primary key)
def get_country_by_id(id):  
    data = db.get_or_404(Country, id)  
    results = data.to_dict()
    return jsonify(results)
    

@app.get('/countries/all')   # get all countries
def get_countries():
    query = sa.select(Country)
    countries = db.session.scalars(query).all()
    results = []
    for c in countries:  # change each item to dict
        results.append(c.to_dict())

    return jsonify(results)


# Handle queries: get a country where an attribute has a particular value.
# Currently only handles one attribute - for complex queries, needs to build a dynamic query
@app.get('/country/')   # /country/?<key>=<value>
def get_country():
    # Get country attributes (from model)
    c = Country()
    c_dict = c.to_dict()
    
    # Get query params
    arg_dict = request.args.to_dict()
    arg_key = list(arg_dict.keys())[0]  # Assume only one arg in query
    if not arg_key in c_dict.keys():
        return error_response(400, f"Attribute {arg_key} not in database")

    # get the value
    query_value = request.args.get(arg_key)
    if not query_value: 
       return error_response(400,f"Attribute {arg_key} must have a value") 

    data = db.session.scalar(sa.select(Country).where(
            getattr(Country, arg_key) == query_value))  
    if data != None:
        results = data.to_dict()
        return jsonify(results)
    else:
        return error_response(400, f"Country with {arg_key} of {query_value} not found in database")


''' Old - too much repeated code
@app.get('/country/')   # /countries/?name=<country name>
def get_country():
    country = request.args.get('name') 
    data = db.session.scalar(sa.select(Country).where(
            #Country.name == country))
            getattr(Country, "name") == country))  
    if data != None:
        results = data.to_dict()
        return jsonify(results)
    else:
        return error_response(400, f"Country {country} not found in database")


@app.get('/country/capital/')   # /capital/?capital=<capital name>
def get_country_with_capital():
    capital = request.args.get('capital') 
    data = db.session.scalar(sa.select(Country).where(
            Country.capital == capital))
    if data != None:
        results = data.to_dict()
        return jsonify(results)
    else:
        return error_response(400, f"Country with capital {capital} not found in database")


'''

@app.post('/countries/')
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


# Retrieve a country by <id> and update its details
@app.put('/countries/<int:id>')
def update_country(id):  
    print(f"id = {id}") 
    c = db.get_or_404(Country, id)  # retrieve country with <id>
    data = request.get_json()
    print(f"Data is {data}")

    # TO DO - check json data - e.g. if a capital city already exists

    # Make the update
    c.from_dict(data)
    print(f"c is {c}")
    db.session.commit()
    return c.to_dict()
    
    

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
