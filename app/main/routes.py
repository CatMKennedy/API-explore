from flask import Flask, render_template, request, json, jsonify, url_for

from werkzeug.http import HTTP_STATUS_CODES  #to be moved to error module

import sqlalchemy as sa

from app.main import bp

from app import db, models
from app.models import Country

# Helper functions

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code


# View functions - for testing

@bp.route("/")
def home():
    return render_template("home.html", name=request.args.get('name'))


# API functions 

@bp.get('/countries/<int:id>')   # Retrieve a country using id (primary key)
def get_country_by_id(id):  
    data = db.get_or_404(Country, id)  
    results = data.to_dict()
    return jsonify(results)

@bp.get('/countries/all')   # get all countries
def get_countries():
    query = sa.select(Country)
    countries = db.session.scalars(query).all()
    results = []
    for c in countries:  # change each item to dict
        results.append(c.to_dict())

    return jsonify(results)

# Handle queries: get a country where an attribute has a particular value.
# Currently only handles one attribute - for complex queries, needs to build a dynamic query
@bp.get('/country/')   # /country/?<key>=<value>
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


@bp.get('/country/capital/')   # /capital/?capital=<capital name>
def get_country_with_capital():
    capital = request.args.get('capital') 
    data = db.session.scalar(sa.select(Country).where(
            Country.capital == capital))
    if data != None:
        results = data.to_dict()
        return jsonify(results)
    else:
        return error_response(400, f"Country with capital {capital} not found in database")


@bp.post('/countries/')
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


# Retrieve a country by <id> and update its details
@bp.put('/countries/<int:id>')
def update_country(id):  
    c = db.get_or_404(Country, id)  # retrieve country with <id>
    data = request.get_json()

    # TO DO - check json data - e.g. if a capital city already exists

    # Make the update
    c.from_dict(data)
    db.session.commit()
    return c.to_dict()
 
    
# Delete country with <id> 
@bp.delete('/countries/<int:id>')
def delete_country(id):  
    c = db.get_or_404(Country, id)  # retrieve country with <id>
    
    db.session.delete(c)
    db.session.commit()
    return c.to_dict()

