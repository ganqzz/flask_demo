from functools import wraps

from flask import render_template, flash, redirect, url_for, abort, request

from app import db
from app.auth import current_user, login_required
from app.models import User, Gig
from . import admin


def admin_required(f):
    @wraps(f)
    def _admin_required(*args, **kwargs):
        if not current_user.is_admin():
            flash('You need to be an administrator to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return _admin_required


@admin.before_request
@login_required
@admin_required
def check_admin_each_request():
    # some logging stuff
    print(f'Admin "{current_user.username}" accessed: {request.url}')


@admin.route('/')
@login_required
@admin_required
def home():
    return render_template('admin/home.html')


@admin.route('/users')
@login_required
@admin_required
def all_users():
    users = User.query.all()
    return render_template('admin/all_users.html', users=users)


@admin.route('/gigs')
@login_required
@admin_required
def all_gigs():
    gigs = Gig.query.all()
    return render_template('admin/all_gigs.html', gigs=gigs)


@admin.route('/gigs/<id>/delete', methods=["POST"])
@login_required
@admin_required
def delete_gig(id):
    gig = Gig.query.get(id)
    if not gig:
        abort(404)

    db.session.delete(gig)
    db.session.commit()
    flash('The gig has been deleted.', 'success')
    return redirect(url_for('admin.all_gigs'))


@admin.route('/users/<id>/delete', methods=["POST"])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    flash('The user has been deleted.', 'success')
    return redirect(url_for('admin.all_users'))
