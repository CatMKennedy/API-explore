# Defines object relational mappings using SQLAlchemy
# This code is based on the tutorial at: https://courses.miguelgrinberg.com/p/flask-mega-tutorial 
# - chapter on API development

from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Country(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    capital: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    area: so.Mapped[Optional[str]] = so.mapped_column(sa.Integer)
    population: so.Mapped[Optional[str]] = so.mapped_column(sa.Integer)

    def __repr__(self):
        return '<Country {}>'.format(self.name)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'capital': self.capital,
            'area': self.area, 
            'population': self.population  
        }
        return data
    
    def from_dict(self, data):
        for field in ['name', 'capital', 'area', 'population']:
            if field in data:
                setattr(self, field, data[field])


def init_db():
    db.create_all()

    # Create test entries in table
    #new_user = Country('a@a.com', 'aaaaaaaa')
    #new_user.display_name = 'Nathan'
    #db.session.add(new_user)
    #db.session.commit()

    #new_user.datetime_subscription_valid_until = datetime.datetime(2019, 1, 1)
    #db.session.commit()