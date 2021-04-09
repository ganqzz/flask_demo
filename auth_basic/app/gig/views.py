from functools import wraps

from flask import Blueprint, render_template, flash, redirect, url_for, \
    abort, request
from werkzeug.utils import escape, unescape

from app import db
from app.auth import current_user, login_required, activation_required, role_required
from app.models import Role, Gig
from .forms import CreateGigForm, UpdateGigForm

gig = Blueprint('gig', __name__)


def gig_owner_required(f):
    @wraps(f)
    def _gig_owner_required(*args, **kwargs):
        gig = Gig.query.filter_by(slug=request.view_args.get('slug')).first()
        if not gig or not current_user.is_gig_owner(gig):
            flash('You are not the owner of that gig.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)

    return _gig_owner_required


@gig.route('/info/<slug>')
@login_required
@activation_required
def show(slug):
    gig = Gig.query.filter_by(slug=slug).first()
    if not gig:
        abort(404)

    musicians = gig.musicians.all()
    return render_template('gig/show_gig.html', gig=gig, musicians=musicians)


@gig.route('/my_gigs')
@login_required
@activation_required
def my_gigs():
    gigs = None
    if current_user.is_role(Role.EMPLOYER):
        gigs = current_user.gigs.all()
    elif current_user.is_role(Role.MUSICIAN):
        gigs = current_user.applied_gigs.all()

    return render_template('gig/my_gigs.html', gigs=gigs)


@gig.route('/create', methods=["GET", "POST"])
@login_required
@activation_required
@role_required(Role.EMPLOYER)
def create():
    form = CreateGigForm()
    if form.validate_on_submit():
        gig = Gig(
            title=escape(form.title.data),
            description=escape(form.description.data),
            payment=form.payment.data,
            location=escape(form.location.data),
            employer_id=current_user.id
        )
        db.session.add(gig)
        db.session.commit()
        flash(f'The new gig has been added. "{gig.title}"', 'success')
        return redirect(url_for('gig.show', slug=gig.slug))

    return render_template('gig/create_gig.html', form=form)


@gig.route('/edit/<slug>', methods=["GET", "POST"])
@login_required
@activation_required
@role_required(Role.EMPLOYER)
@gig_owner_required
def edit(slug):
    form = UpdateGigForm()
    gig = Gig.query.filter_by(slug=slug).first()
    if not gig:
        abort(404)

    if form.validate_on_submit():
        gig.update(
            title=escape(form.title.data),
            description=escape(form.description.data),
            payment=form.payment.data,
            location=escape(form.location.data)
        )
        db.session.add(gig)
        db.session.commit()
        flash('The gig has been updated.', 'success')
        return redirect(url_for('gig.show', slug=gig.slug))

    form.title.data = unescape(gig.title)
    form.description.data = unescape(gig.description)
    form.payment.data = gig.payment
    form.location.data = unescape(gig.location)
    return render_template('gig/edit_gig.html', gig=gig, form=form)


@gig.route('/delete/<slug>', methods=["POST"])
@login_required
@activation_required
@role_required(Role.EMPLOYER)
@gig_owner_required
def delete(slug):
    gig = Gig.query.filter_by(slug=slug).first()
    if not gig:
        abort(404)

    db.session.delete(gig)
    db.session.commit()
    flash('The gig has been deleted.', 'success')
    return redirect(url_for('gig.my_gigs'))


@gig.route('/apply/<slug>', methods=["POST"])
@login_required
@activation_required
@role_required(Role.MUSICIAN)
def apply_to_gig(slug):
    gig = Gig.query.filter_by(slug=slug).first()
    if not gig:
        abort(404)

    current_user.apply(gig)
    flash(f'You just applied to the gig: "{gig.title}".', 'success')
    return redirect(request.referrer)  # back
