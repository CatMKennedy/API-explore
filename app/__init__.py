'''
Uses application factory pattern. Follows approximately the guidelines in 
Miguel Grinberg's mega-tutorial at https://blog.miguelgrinberg.com/, and also the
DigitalOcean tutorial on structuring a large Flask application.

'''
from flask import Flask

from config import Config, InMemoryConfig   

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Called by api.py in the top level directory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    #app.config.from_object(InMemoryConfig)
    
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app