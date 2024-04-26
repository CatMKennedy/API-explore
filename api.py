'''
Top level initialisation - calls the create_app() application factory in the "app"
subdirectory. The project structure follows approximately the guidelines in 
Miguel Grinberg's mega-tutorial at https://blog.miguelgrinberg.com/, and also the
DigitalOcean tutorial on structuring a large Flask application.
'''
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import Country

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Country': Country}


