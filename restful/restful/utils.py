from functools import wraps
from threading import Thread

from flask import current_app, render_template
from flask import request
from flask_mail import Message

from . import mail
from .errors import ValidationError


def json_input_required(view_func):
    """ decorator to verify the input body is json """

    @wraps(view_func)
    def _(*args, **kwargs):
        if request.is_json:
            return view_func(*args, **kwargs)
        raise ValidationError('body must be json')

    return _


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, sender=None, **kwargs):
    app = current_app._get_current_object()  # 別スレッドで動かすためには実オブジェクトが必要
    sender = sender or app.config['MY_MAIL_SENDER']
    msg = Message(subject, sender=sender, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
