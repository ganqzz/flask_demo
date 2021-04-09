from threading import Thread

from flask import render_template, url_for, current_app
from flask_mail import Message

from app import mail


def create_message(content):
    msg = Message(
        content["subject"],
        sender=content["sender"],
        recipients=content["recipients"],
    )
    msg.body = render_template(content["template"] + ".txt", **content["kwargs"])
    msg.html = render_template(content["template"] + ".html", **content["kwargs"])
    return msg


def _send_mail(app, content):
    with app.app_context():
        msg = create_message(content)
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    content = {
        "subject": subject,
        "sender": "Globomantics Team <noreply@example.com>",
        "recipients": [to],
        "template": template,
        "kwargs": kwargs,
    }

    if current_app.config.get("SEND_MAIL_BY_CELERY"):
        # TODO: Celery
        pass
    else:
        # fire and forget by using Thread
        thr = Thread(target=_send_mail,
                     args=[current_app._get_current_object(), content])
        thr.start()


def send_activation_mail(user):
    send_mail(
        user.email,
        "Confirm Your Account",
        "auth/email/confirm",
        username=user.username,
        role=user.role_id,
        activation_link=url_for("auth.activate_account",
                                token=user.activation_token,
                                _external=True)  # _external=True: absolute path
    )


def send_password_reset_mail(user):
    send_mail(
        user.email,
        "Reset Password",
        "auth/email/password_reset",
        username=user.username,
        role=user.role_id,
        password_reset_link=url_for("auth.update_password",
                                    token=user.reset_token,
                                    email=user.email,  # for security reason
                                    _external=True)
    )
