from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class ModelUpdateMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, **kwargs):
        for name, value in kwargs.items():
            if name in self.__dict__:
                setattr(self, name, value)


class Movie(ModelUpdateMixin, db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    casts = db.Column(db.String(255), nullable=False)  # list of strings
    genres = db.Column(db.String(255), nullable=False)  # list of strings
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='movies', lazy='joined')  # eager loading


class User(ModelUpdateMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # hashed

    movies = db.relationship('Movie', back_populates='user', lazy='dynamic',
                             cascade='all')  # deleteはしない

    def __init__(self, email, password):
        super().__init__(email=email, password=generate_password_hash(password))

    def __str__(self):
        return '<User: email={}, password={}>'.format(self.email, self.password)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
