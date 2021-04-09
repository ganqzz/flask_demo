from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError as MaValidationError

from restful import crud
from restful.errors import ValidationError
from restful.schemas import movie_schema
from restful.utils import json_input_required
from . import register_api


class MovieApi(MethodView):
    """ api/movies/ """

    def get(self, id):
        if id:
            payload = movie_schema.dump(crud.get_movie_by_id(id))
        else:
            payload = movie_schema.dump(crud.get_movies(), many=True)
        return jsonify(payload), 200

    @jwt_required
    @json_input_required
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        data = _validate(body)
        movie = crud.create_movie(user_id, data)
        payload = movie_schema.dump(movie)
        return jsonify(payload), 201

    @jwt_required
    @json_input_required
    def put(self, id):
        user_id = get_jwt_identity()
        body = request.get_json()
        data = _validate(body)
        movie = crud.update_movie(id, user_id, data)
        payload = movie_schema.dump(movie)
        return jsonify(payload), 200

    @jwt_required
    def delete(self, id):
        user_id = get_jwt_identity()
        crud.delete_movie(id, user_id)
        return '', 204


def _validate(body):
    try:
        return movie_schema.load(body)
    except MaValidationError as e:
        raise ValidationError(e.normalized_messages())  # dict


# Register routes to the Blueprint
register_api(MovieApi, 'movies', '/movies/')
