from flask import request

from cleana.usecase.auth.auth_usecase import AuthUseCase

auth_use_case: AuthUseCase


def login():
    auth_use_case.login(request.get_json())
    # 400
    return '', 200


def logout():
    auth_use_case.logout()
    return '', 200


def signup():
    auth_use_case.sign_up(request.get_json())
    # 400
    return '', 201


def update():
    auth_use_case.update(request.get_json())
    # 401, 400
    return '', 200


def register_routes(app):
    app.add_url_rule('/auth/login', view_func=login, methods=['POST'])
    app.add_url_rule('/auth/logout', view_func=logout, methods=['GET'])
    app.add_url_rule('/auth/signup', view_func=signup, methods=['POST'])
    app.add_url_rule('/auth/update', view_func=update, methods=['POST'])
