from sqlalchemy.exc import DatabaseError

from . import db
from .errors import DoesNotExist, ValidationError
from .models import Movie, User


def get_movies():
    movies = Movie.query.all()  # Djangoのobjects.all()とは違い、クエリが実行されてオブジェクトのリストが返る
    return movies


def get_movie_by_id(id, user_id=None):
    if user_id:
        movie = Movie.query.filter_by(id=id, user_id=user_id).first()
    else:
        movie = Movie.query.get(id)

    if movie is None:
        raise DoesNotExist
    return movie


def create_movie(user_id, data):
    user = get_user_by_id(user_id)  # DoesNotExistは発生しない前提
    movie = Movie(**data, user=user)
    try:
        db.session.add(movie)
        db.session.commit()
        return movie
    except DatabaseError as e:
        raise ValidationError(str(e))  # TODO: user friendly message


def update_movie(id, user_id, data):
    movie = get_movie_by_id(id, user_id)
    movie.update(**data)
    try:
        db.session.commit()
        return movie
    except DatabaseError as e:
        raise ValidationError(str(e))


def delete_movie(id, user_id):
    movie = get_movie_by_id(id, user_id)
    db.session.delete(movie)
    db.session.commit()


def get_user_by_id(id):
    user = User.query.get(id)
    if user is None:
        raise DoesNotExist
    return user


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise DoesNotExist
    return user


def create_user(data):
    try:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user
    except DatabaseError as e:
        raise ValidationError(str(e))


def update_user_password(id, password):
    user = get_user_by_id(id)
    # TODO: validation
    user.hash_password(password)
    db.session.commit()
    return user
