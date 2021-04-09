from datetime import timedelta

from flask import request, jsonify
from flask_jwt_extended import create_access_token, decode_token
from marshmallow import ValidationError as MaValidationError

from restful import crud
from restful.errors import ValidationError, DoesNotExist, \
    response_unauthorized, response_bad_request
from restful.schemas import user_schema
from restful.utils import send_email
from . import auth_bp


def _load_body():
    body = request.get_json() if request.is_json else request.form
    if not body:
        raise ValidationError('body must be json or form')
    return body  # dict


def _validate(body):
    try:
        return user_schema.load(body)
    except MaValidationError as e:
        raise ValidationError(e.normalized_messages())  # dict


@auth_bp.route('/signup', methods=['POST'])
def signup():
    # TODO: confirmation
    user = crud.create_user(_validate(_load_body()))
    payload = user_schema.dump(user)
    return jsonify(payload), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    body = _load_body()
    email = body.get('email')
    password = body.get('password')
    if not email or not password:
        return response_bad_request('email and password both required')

    try:
        user = crud.get_user_by_email(email)
    except DoesNotExist:  # 404 -> 401
        return response_unauthorized(f'user({email}) not found')

    if not user.check_password(password):
        return response_unauthorized('password not match')

    expires = timedelta(days=7)
    access_token = create_access_token(identity=user.id, expires_delta=expires)
    return {'token': access_token}, 200


@auth_bp.route('/forget_password', methods=['POST'])
def forget_password():
    body = _load_body()
    email = body.get('email')  # not found => None
    if not email:
        return response_bad_request('email required')

    user = crud.get_user_by_email(email)
    expires = timedelta(minutes=30)
    reset_token = create_access_token(str(user.id), expires_delta=expires)  # *
    url = request.host_url + 'reset/' + reset_token

    send_email(
        [user.email],
        '[Movie-bag] Reset Your Password',
        'email/reset_password',
        url=url
    )


@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    body = _load_body()
    reset_token = body.get('reset_token')
    password = body.get('password')
    if not reset_token or not password:
        return response_bad_request('both reset_token and password required')

    # TODO: validation
    user_id = decode_token(reset_token)['identity']  # *
    user = crud.update_user_password(user_id, password)

    send_email(
        [user.email],
        '[Movie-bag] Password reset successful',
        'email/reset_password_done',
    )
