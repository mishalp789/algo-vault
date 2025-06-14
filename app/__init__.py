from flask import Flask
from .models import db
from .auth import auth as auth_blueprint
from .routes import main as main_blueprint
from flask_login import LoginManager
from .models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'algo-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///algovault.db'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
