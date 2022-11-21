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
login.login_view='index.login'
login.login_message='Por favor inicie sesión para acceder a esta página.'
from .routes import post_scope,error_scope,index_scope,user_scope
from app.models import User,Posts,Role

app.register_blueprint(error_scope,url_prefix="/")
app.register_blueprint(index_scope,url_prefix="/")
app.register_blueprint(user_scope,url_prefix="/user")
app.register_blueprint(post_scope,url_prefix="/post")
#IMPORTA A LA SHEL AUTOMATICAMENTE LOS MODELOS
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Posts}