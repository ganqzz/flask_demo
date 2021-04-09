from flask import jsonify

from werkzeug.exceptions import InternalServerError


# application exceptions

class ValidationError(ValueError):
    pass


class DoesNotExist(ValueError):
    pass


# error responses
# messageはjson変換可能であればよい

def response_bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def response_unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def response_forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


# error handlers

def validation_error(e):
    return response_bad_request(e.args[0])


def unauthorized(e):
    return response_unauthorized(e.args[0])


def forbidden(e):
    return response_forbidden(e.args[0])


def not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response


def method_not_allowed(e):
    response = jsonify({'error': 'method not allowed'})
    response.status_code = 405
    return response


def internal_server_error(e):
    response = jsonify({'error': 'internal server error'})
    response.status_code = 500
    return response


def register_error_handlers(app):
    app.register_error_handler(401, unauthorized)  # Flask-JWT-Extendedはこれを使わない
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(DoesNotExist, not_found)
    app.register_error_handler(ValidationError, validation_error)
    app.register_error_handler(InternalServerError, internal_server_error)
