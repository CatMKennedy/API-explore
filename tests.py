import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
import json
import sqlalchemy as sa
from app import create_app, db
from app.models import Country
from app.main import bp
from config import Config

# Use in-memory test db 
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class CountryAPICase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.populate_db() 
        self.test_client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def populate_db(self):
        c1 = Country(name='USA', capital='Washington', area=70000)
        c2 = Country(name='Canada', capital='Ottowa', area=60000)
        db.session.add_all([c1, c2])
        db.session.commit()
        #return [c1, c2]

    # test API 
    # TO DO - refactoring - repeated code and string constants currently
    # - also need more error handling tests

    def test_get_country_by_id(self):
        response = self.test_client.get('/countries/1') 
        data = json.loads(response.get_data())
        print(f'data = {data}')
        self.assertEqual(response.status_code, 200)
        # test error-hanlding - non-existent id
        response = self.test_client.get('/countries/20') 
        self.assertEqual(response.status_code, 404)

    def test_get_country_by_capital(self): 
        response = self.test_client.get('/countries/Washington/') 
        data = json.loads(response.get_data())
        print(f'data = {data}')
        self.assertEqual(response.status_code, 200)
        # test error-handling - non-existent capital
        response = self.test_client.get('/countries/Athens/')
        self.assertEqual(response.status_code, 404)

    def test_get_all_countries(self): 
        response = self.test_client.get('/countries/all')
        data = json.loads(response.get_data())
        print(f'data = {data}')
        self.assertEqual(response.status_code, 200)

    def test_get_query_string(self):
        response = self.test_client.get('/countries/?area=70000') 
        data = json.loads(response.get_data())
        print(f'data = {data}')
        self.assertEqual(response.status_code, 200)
        #TO DO - need to test badly formed query string

    def test_create_country(self):
        response = self.test_client.post('/countries/', 
            json={'name':'France', 
                'capital':'Paris',
                'area': 20000}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        #test error handling - repeat post of same item, which already exists
        response = self.test_client.post('/countries/', 
            json={'name':'France', 
                'capital':'Paris',
                'area': 20000}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
    def test_update_country(self):
        response = self.test_client.put('/countries/2', 
            json = {'area': 85000}, content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        #test error handling - item to be updated not found
        response = self.test_client.put('/countries/20', 
            json = {'area': 85000}, content_type='application/json') 
        self.assertEqual(response.status_code, 404)
        
    def test_delete_country(self):
        response = self.test_client.delete('/countries/1', 
            content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        #test error handling - item to be deleted not found
        response = self.test_client.delete('/countries/20', 
            content_type='application/json') 
        self.assertEqual(response.status_code, 404)
        

if __name__ == '__main__':
    unittest.main(verbosity=2)