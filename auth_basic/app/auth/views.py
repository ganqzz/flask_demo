from flask import render_template, redirect, flash, url_for, make_response

from app import db
from app.email_utils import send_activation_mail, send_password_reset_mail
from app.models import User
from . import auth, current_user, login_required, encrypt_cookie, \
    login_user, logout_user
from .forms import LoginForm, RegistrationForm, PasswordResetForm, UpdatePasswordForm


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # POST
        user = User(
            form.username.data,
            form.email.data,
            form.password.data,
            form.location.data,
            form.description.data,
            form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('You are registered.', 'success')
        login_user(user)
        user.create_token_for('activation')
        send_activation_mail(user)
        return redirect(url_for('main.home'))

    # GET
    return render_template("auth/register.html", form=form)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        flash('Your are already logged in.', 'warning')
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # userが存在するかどうかの確認は、formの方で行っている
        if user.check_password(form.password.data):
            login_user(user)
            flash('You successfully logged in.', 'success')
            if user.is_admin():
                # adminはremember_meを無視する
                return redirect(url_for('admin.home'))

            resp = make_response(redirect(url_for('main.home')))
            if form.remember_me.data:
                remember_token = user.get_remember_token()
                resp.set_cookie('remember_token', encrypt_cookie(remember_token),
                                max_age=8640000)  # 100days
                resp.set_cookie('user_id', encrypt_cookie(user.id), max_age=8640000)
            return resp
        else:
            form.password.errors.append('The password is not correct.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    current_user.forget()
    resp = make_response(redirect(url_for('main.home')))
    resp.set_cookie('remember_token', '', max_age=0)
    resp.set_cookie('user_id', '', max_age=0)
    logout_user()
    flash('You are logged out.', 'success')
    return resp


@auth.route('/activate/<token>')
@login_required
def activate_account(token):
    if current_user.is_active():
        flash('Your account is already active.', 'warning')
    elif current_user.activate(token):
        flash(f'Your account is confirmed. Welcome {current_user.username}!', 'success')
    else:
        flash('The confirmation link is not valid or it has expired.', 'danger')
    return redirect(url_for('main.home'))


@auth.route('/send_activation')
@login_required
def send_activation():
    if current_user.is_active():
        flash('Your account is already active.', 'warning')
    else:
        current_user.create_token_for('activation')
        send_activation_mail(current_user)
        flash('New email has been sent. Please use it to confirm your account.', 'success')
    return redirect(url_for('main.home'))


@auth.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    """パスワードリセットリンク用メール送信フォーム"""
    if current_user.is_authenticated():
        flash('Your are already logged in.', 'warning')
        return redirect(url_for('main.home'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # userが存在するかどうかの確認は、formの方で行っている
        user.create_token_for('reset')
        send_password_reset_mail(user)
        flash('The password reset instructions are sent to your email.', 'success')
        return redirect(url_for('main.home'))

    return render_template('auth/reset_password.html', form=form)


@auth.route('/update_password/<token>/<email>', methods=["GET", "POST"])
def update_password(token, email):
    """パスワード更新フォーム"""
    if current_user.is_authenticated():
        flash('Your are already logged in.', 'warning')
        return redirect(url_for('main.home'))

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_reset_token(token):
        flash('The password reset link is not valid or it has expired.', 'danger')
        return redirect(url_for('main.home'))

    form = UpdatePasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        user.reset_hash = None
        db.session.add(user)
        db.session.commit()
        flash('New password is set! You can now login to the account.', 'success')
        return redirect(url_for('auth.login'))

    flash(f'Hi {user.username}! You can now set a new password for the account.', 'success')
    return render_template('auth/update_password.html', form=form, )
