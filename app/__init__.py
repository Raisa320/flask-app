from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
#CONFIGURACION DE LA CARPETAS DE TEMPLATES
#app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)


app = Flask(__name__)

app.config.from_object(Config)
db=SQLAlchemy(app)
migrate=Migrate(app,db)
moment = Moment(app)
login=LoginManager(app)
login.login_view='login'
login.login_message='Por favor inicie sesión para acceder a esta página.'
from app import routes
from app.models import User,Posts,Role

#IMPORTA A LA SHEL AUTOMATICAMENTE LOS MODELOS
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Posts}