import os
basedir = os.path.abspath(os.path.dirname(__file__))

# The config class is selected by "api.py" when it calls "create_app()"

class Config(object):
    # Default
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
class InMemoryConfig(Config):
    #For in-memory database - may be test or dev
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    
# TO DO - add other options - such as test and prod
