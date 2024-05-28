from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__,instance_relative_config=True)
app.config.from_object(config("APP_SETTINGS"))

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt()
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from src.accounts.view import accounts_bp
from src.core.view import core_bp
from src.accounts.models import User

login_manager.login_view = "accounts.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(User.id == int(user_id)).first()


app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)
