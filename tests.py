import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
import sqlalchemy as sa
from app import create_app, db
from app.models import Country
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class CountryModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_query_items(self):
        c1 = Country(name='USA', capital='Washington', area=70000)
        c2 = Country(name='Canada', capital='Ottowa', area=60000)
        db.session.add_all([c1, c2])
        db.session.commit()
   
        query = sa.select(Country)
        data = db.session.scalars(query).all()
        self.assertEqual(data, [c1, c2])
   
        query_attr = "name"
        query_value = "Canada"
        data = db.session.scalar(sa.select(Country).where(
            getattr(Country, query_attr) == query_value))  
        self.assertEqual(data.capital, "Ottowa")

    
    def test_update_item(self):
        c1 = Country(name='USA', capital='Washington', area=70000)
        c2 = Country(name='Canada', capital='Ottowa', area=60000)
        db.session.add_all([c1, c2])
        db.session.commit()
        
        id = 1
        c = db.get_or_404(Country, id)  # retrieve country with <id>
        self.assertEqual(c.area, 70000)

        c.area = 150000
        db.session.commit()
        c_updated = db.get_or_404(Country, id)
        self.assertEqual(c_updated.area, 150000)


    def test_delete_item(self):
        c1 = Country(name='USA', capital='Washington', area=70000)
        c2 = Country(name='Canada', capital='Ottowa', area=60000)
        db.session.add_all([c1, c2])
        db.session.commit()
        
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