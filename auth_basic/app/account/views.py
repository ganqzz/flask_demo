from flask import Blueprint, render_template, flash, redirect, url_for, abort
from werkzeug.utils import escape, unescape

from app import db
from app.auth import current_user, login_required, activation_required, logout_user
from app.models import User, Role
from .forms import UpdateAccountForm, DeleteAccountForm

account = Blueprint('account', __name__)


@account.route('/profile/<username>')
@login_required
@activation_required
def show(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    gigs = None
    if user.is_role(Role.EMPLOYER):
        gigs = user.gigs.all()
    elif user.is_role(Role.MUSICIAN):
        gigs = user.applied_gigs.all()

    delete_form = DeleteAccountForm()
    return render_template('account/show_account.html',
                           user=user, gigs=gigs, delete_form=delete_form)


@account.route('/edit', methods=["GET", "POST"])
@login_required
@activation_required
def edit():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.location = escape(form.location.data)
        current_user.description = escape(form.description.data)
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account.show', username=current_user.username))

    form.location.data = unescape(current_user.location)
    form.description.data = unescape(current_user.description)
    return render_template('account/edit_account.html', form=form)


@account.route('/delete', methods=["POST"])
@login_required
@activation_required
def delete():
    """ resign """
    db.session.delete(current_user._get_current_object())
    db.session.commit()
    logout_user()
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('main.home'))
