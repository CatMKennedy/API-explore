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


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_countries(self):
        c1 = Country(name='USA', capital='Washington', area=70000)
        c2 = Country(name='Canada', capital='Ottowa', area=60000)
        db.session.add_all([c1, c2])
        db.session.commit()
   
        query = sa.select(Country)
        data = db.session.scalars(query).all()
        print(f'retrieved = {data}')
        countries = [c1, c2]
        print(f'countries = {countries}')
        self.assertEqual(data, [c1, c2])


if __name__ == '__main__':
    unittest.main(verbosity=2)