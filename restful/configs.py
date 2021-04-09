import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_string'

    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MY_MAIL_SENDER = 'support@movie-bag.com'
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class DevConfig(Config):
    """Development configuration"""
    ENV = 'development'
    DEBUG = True


class TestConfig(Config):
    """Test configuration"""
    ENV = 'test'
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # in-memory


class ProdConfig(Config):
    """Production configuration"""
    ENV = 'production'
    DEBUG = False
