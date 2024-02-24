# __init__.py  - based on various tutorials 
from flask import Flask, render_template, request, json, jsonify, url_for

from werkzeug.http import HTTP_STATUS_CODES  #to be moved to error module

import sqlalchemy as sa

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# TO DO - add error handling
# from a app.api.errors import bad_request

app = Flask(__name__)   # create a Flask object


# Configure database using SQLAlchemy
app.config.from_object(Config)  # configure app (Flask object)
db = SQLAlchemy(app)            # Create db 
migrate = Migrate(app, db)

# Createflask db upgrade the database using cli with migrate:
# flask db init - create new migrations directory
# flask db migrate - create/update script to adapt any existing db to model 
# flask db upgrade - apply any changes to db (apply script)


from app import models
from app.models import Country


# Initial DB contents for testing
countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]


# Needs refactoring



# TO DO: change the route functions so that they use the database instead


# API Helper functions - currently doesn't use database
def _find_next_id():
    return max(country["id"] for country in countries) + 1

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code



# View functions

@app.route("/")
def home():
    return render_template("home.html")


# API functions

@app.get('/countries')
def get_countries():
    pass

@app.get('/countries/<int:id>')
def get_country(id):
    pass

@app.post('/countries')
def create_country():
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


'''
@app.post('/countries')
def add_country():
    if request.is_json:
        country_name = request.json['name']
        country_capital = request.json['capital']
        country_area = request.json['area']
        c = Country(name=country_name, capital=country_capital, area=country_area)
        #dict = json.loads(country)
        #c = Country(name=dict["name"], capital=dict["capital"], area=dict["area"])
        db.session.add(c)
        db.session.commit()
    return {"error": "Request must be JSON"}, 415
'''
    


'''
@app.get("/countries")
def get_countries():
    return jsonify(countries)
'''
    
'''
@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415
'''

# For newer Mac OS versions, port 5000 is already used - change to port 8000
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=8000, debug=True)
