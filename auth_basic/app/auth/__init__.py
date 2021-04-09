from functools import wraps

from flask import Blueprint, g, session, request, flash, redirect, url_for, \
    current_app, has_request_context
from itsdangerous import URLSafeSerializer
from werkzeug.local import LocalProxy

from app.models import User, Role

auth = Blueprint('auth', __name__, template_folder='templates')

current_user = LocalProxy(lambda: get_current_user())  # request local


def get_current_user():
    _current_user = getattr(g, '_current_user', None)
    if _current_user is None:
        if cuid := session.get('user_id'):
            if user := User.query.get(cuid):
                _current_user = g._current_user = user  # memoization
        elif cuid := request.cookies.get('user_id'):  # remember me
            user = User.query.get(int(decrypt_cookie(cuid)))
            if user and user.check_remember_token(
                    decrypt_cookie(request.cookies.get('remember_token'))):
                login_user(user)
                _current_user = g._current_user = user  # memoization

    if _current_user is None:
        _current_user = User()  # anonymous user

    return _current_user


def login_required(f):
    @wraps(f)
    def _login_required(*args, **kwargs):
        if current_user.is_anonymous():
            flash('You need to be logged in to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return _login_required


def activation_required(f):
    @wraps(f)
    def _activation_required(*args, **kwargs):
        if not current_user.is_active():
            flash('Only activated users have access to that page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)

    return _activation_required


def role_required(role):
    def _role_required(f):
        @wraps(f)
        def __role_required(*args, **kwargs):
            if not current_user.is_role(role):
                flash('You are not authorized to access this page.', 'danger')
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)

        return __role_required

    return _role_required


def encrypt_cookie(content):
    s = URLSafeSerializer(current_app.secret_key, salt='cookie')
    return s.dumps(content)


def decrypt_cookie(encrypted_content):
    s = URLSafeSerializer(current_app.secret_key, salt='cookie')
    try:
        content = s.loads(encrypted_content)
    except:
        content = '-1'
    return content


def login_user(user):
    session['user_id'] = user.id


def logout_user():
    session.pop('user_id', None)


@auth.app_context_processor
def inject_app_context_globals():
    if has_request_context():
        return dict(Role=Role, current_user=get_current_user())
    return dict(Role=Role)  # at sending emails


# import views here
from . import views
