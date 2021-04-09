from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
api_bp = Blueprint('api', __name__)


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    api_bp.add_url_rule(url, defaults={pk: None},
                        view_func=view_func, methods=['GET'])
    api_bp.add_url_rule(url, view_func=view_func, methods=['POST'])
    api_bp.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func,
                        methods=['GET', 'PUT', 'DELETE'])


from . import main, auth, movie
