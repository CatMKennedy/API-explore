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


class CountryModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
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
        return [c1, c2]

    # test API 

    def test_get_country_by_id(self):
        init_state = self.populate_db() 
        response = self.test_client.get('/countries/1') 
        data = json.loads(response.get_data())
        print(f'data = {data}')
        self.assertEqual(response.status_code, 200)

    #TO DO - this is redundant - covered by country/?query string
    def test_get_country_by_capital(self):
        init_state = self.populate_db() 
        response = self.test_client.get('/country/capital/?capital=Ottowa') 
        data = json.loads(response.get_data())
        print(f'data = {data}')
        self.assertEqual(response.status_code, 200)

    def test_get_countries(self):
        init_state = self.populate_db() 
        response = self.test_client.get('/countries/all')
        data = json.loads(response.get_data())
        print(f'data = {data}')
        self.assertEqual(response.status_code, 200)

    def test_get_query_string(self):
        init_state = self.populate_db() 
        response = self.test_client.get('/country/?area=70000') 
        data = json.loads(response.get_data())
        print(f'data = {data}')
        self.assertEqual(response.status_code, 200)

    
    # URLs and status codes should be constants
    def test_create_country(self):
        response = self.test_client.post('/countries/', 
            json={'name':'France', 
                'capital':'Paris',
                'area': 20000}, content_type='application/json')
        self.assertEqual(response.status_code, 201)

 
    def test_update_country(self):
        pass




    # test database + models
    def test_query_items(self):
        init_state = self.populate_db()
   
        query = sa.select(Country)
        data = db.session.scalars(query).all()
        self.assertEqual(data, init_state)
   
        query_attr = "name"
        query_value = "Canada"
        data = db.session.scalar(sa.select(Country).where(
            getattr(Country, query_attr) == query_value))  
        self.assertEqual(data.capital, "Ottowa")

    
    def test_update_item(self):
        init_state = self.populate_db()
        
        id = 1
        c = db.get_or_404(Country, id)  # retrieve country with <id>
        self.assertEqual(c.area, 70000)

        c.area = 150000
        db.session.commit()
        c_updated = db.get_or_404(Country, id)
        self.assertEqual(c_updated.area, 150000)


    def test_delete_item(self):
        init_state = self.populate_db()
        
        id = 2
        c = db.get_or_404(Country, id)  # retrieve country with <id>
        self.assertEqual(c.name, "Canada")
        db.session.delete(c)
        db.session.commit()

        data = db.session.scalar(sa.select(Country).where(
            getattr(Country, "name") == "Canada"))
        self.assertEqual(data, None)

        


if __name__ == '__main__':
    unittest.main(verbosity=2)