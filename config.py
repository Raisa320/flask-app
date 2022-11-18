import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'estaesmiclavesecreta'
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    #TEMPLATE_FOLDER = "views/templates/"
    #STATIC_FOLDER = "views/static/"