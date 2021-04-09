from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from configs import DevConfig

db = SQLAlchemy()
ma = Marshmallow()  # after db
mail = Mail()
jwt = JWTManager()


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    from .views import main_bp, auth_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    from .errors import register_error_handlers
    register_error_handlers(app)

    from .commands import register_commands
    register_commands(app)

    return app
