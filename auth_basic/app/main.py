from flask import render_template, Blueprint

from app.auth import current_user
from app.models import User, Role, Gig

main = Blueprint('main', __name__)


@main.route('/')
def home():
    gigs = musicians = None
    if current_user.is_role(Role.MUSICIAN):
        gigs = Gig.query.all()
    elif current_user.is_role(Role.EMPLOYER):
        musicians = User.query.filter_by(role_id=Role.MUSICIAN).all()
    return render_template('main/home.html', gigs=gigs, musicians=musicians)
