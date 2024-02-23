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

    def __repr__(self):
        return '<Country {}>'.format(self.name)