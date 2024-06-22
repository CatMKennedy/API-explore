Example REST API using Python Flask, SQLite and SQLAlchemy.

The data model is for demonstration only and contains a list of countries, with country name, capital and area. The example is based on the tutorial at: https://realpython.com/api-integration-in-python/#flask. In the repo, the database is already initialised and contains 10 example countries.

USER GUIDE

After creating a virtual environment, and installing the packages in "requirements.txt", it should be easy to try out the API manually on localhost. First, start the application on the Flask development server:

(venv) flask run

To retrieve data, point the browser to: http://127.0.0.1:5000/ This may initially produce "Hello world" (as part of a test). Here are some example queries:

http://127.0.0.1:5000/countries/all

- should give a json list of countries in the initial database

http://127.0.0.1:5000/countries/2

- return the country with id=2 (return the second country ).

http://127.0.0.1:5000/countries/?capital=Berlin

- return the country whose capital is Berlin

http://127.0.0.1:5000/countries/?name=UK

- return the country with name UK

If an error happens (e.g. country does not exist), the correct HTTP error should be returned. Error handling is still being improved.

To add, modify or delete a country - use command line with cURL.

Example: create a new entry:

curl -i http://127.0.0.1:5000/countries/ -X POST -H 'Content-Type: application/json' -d '{"name":"Norway", "capital": "Oslo", "area":30000}' -w '\n

Check it:
http://127.0.0.1:5000/countries/?name=Norway

- should return the json entry for the newly added country

Modify the new entry by changing the area (assume id = 11):

curl -i -H "Content-Type: application/json" -X PUT -d '{"area":15000}' http://localhost:5000/countries/11

Delete it:

curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/countries/11
