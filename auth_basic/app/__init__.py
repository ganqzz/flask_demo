import os

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # このファイルからみて、1階上

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY') or 'hard_to_guess_string',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'db.sqlite3'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True,
        SEND_MAIL_BY_CELERY=False,
        MAIL_SERVER='smtp.mailtrap.io',
        MAIL_PORT=2525,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    )

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from .main import main
    from .auth import auth
    from .account.views import account
    from .gig.views import gig
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(account, url_prefix='/user')
    app.register_blueprint(gig, url_prefix='/gig')
    app.register_blueprint(admin, url_prefix='/admin')

    return app
