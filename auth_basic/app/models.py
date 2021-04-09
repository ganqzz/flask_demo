from datetime import datetime
from secrets import token_urlsafe

from slugify import slugify
from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class ModelUpdateMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, **kwargs):
        for name, value in kwargs.items():
            if name in self.__dict__:
                setattr(self, name, value)


def generate_token():
    return token_urlsafe(20)


def generate_hash(token):
    return generate_password_hash(token)


def _check_token(hash, token):
    return check_password_hash(hash, token)


class Remember(db.Model):
    __tablename__ = 'remembers'

    id = db.Column(db.Integer, primary_key=True)
    remember_hash = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    def __init__(self, user_id):
        self.token = generate_token()  # transient attr: not saved in DB
        self.remember_hash = generate_hash(self.token)
        self.user_id = user_id

    def check_token(self, token):
        return _check_token(self.remember_hash, token)


class Gig(ModelUpdateMixin, db.Model):
    __tablename__ = 'gigs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    payment = db.Column(db.Numeric)
    location = db.Column(db.String(100), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)  # update_slug

    def __init__(self, title, description, payment, location, employer_id):
        super().__init__(
            title=title,
            description=description,
            payment=payment,
            location=location,
            employer_id=employer_id
        )


@event.listens_for(Gig.title, 'set')  # AttributeEvents.set()
def update_slug(target, value, old_value, initiator):
    target.slug = slugify(value) + '-' + token_urlsafe(3)


# junction table
applications = db.Table(
    'applications',
    db.Column('gig_id', db.Integer, db.ForeignKey('gigs.id')),
    db.Column('musician_id', db.Integer, db.ForeignKey('users.id'))
)


class Role:
    ANONYMOUS = 0
    ADMIN = 1
    MUSICIAN = 2
    EMPLOYER = 3


class User(ModelUpdateMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.Integer, nullable=False, default=0)
    activated = db.Column(db.Boolean, default=False)
    activation_hash = db.Column(db.String(255))
    activation_sent_at = db.Column(db.DateTime)
    reset_hash = db.Column(db.String(255))
    reset_sent_at = db.Column(db.DateTime)

    remember_hashes = db.relationship(Remember, backref='user',
                                      lazy='dynamic',  # returns Query object
                                      cascade='all, delete-orphan')
    gigs = db.relationship(Gig, backref='employer', lazy='dynamic',
                           cascade='all, delete-orphan')
    applied_gigs = db.relationship(Gig, secondary=applications,
                                   backref=db.backref('musicians', lazy='dynamic'),
                                   lazy='dynamic', cascade='all')

    def __init__(self, username='', email='', password='', location='', description='',
                 role_id=Role.ANONYMOUS):
        super().__init__(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            location=location,
            description=description,
            role_id=role_id,
            activated=(role_id == Role.ADMIN)
        )

    def __str__(self):
        return '<User: username={}, email={}>'.format(self.username, self.email)

    @property
    def password(self):
        raise AttributeError('Password should not be read like this')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_remember_token(self):
        remember_instance = Remember(self.id)
        db.session.add(remember_instance)
        db.session.commit()
        return remember_instance.token

    def check_remember_token(self, token):
        if token:
            for remember_hash in self.remember_hashes:
                if remember_hash.check_token(token):
                    return True
        return False

    def forget(self):
        self.remember_hashes.delete()  # delete all
        db.session.commit()

    def is_authenticated(self):
        return '' != self.username

    def is_anonymous(self):
        return '' == self.username

    def is_admin(self):
        return self.role_id == Role.ADMIN

    def is_role(self, role):
        return self.role_id == role

    def is_gig_owner(self, gig):
        return self.id == gig.employer_id

    def is_applied_to(self, gig):
        if gig is None:
            return False
        return self.applied_gigs.filter_by(id=gig.id).first() is not None

    def apply(self, gig):
        if not self.is_applied_to(gig):
            self.applied_gigs.append(gig)
            db.session.add(self)
            db.session.commit()

    def remove_application(self, gig):  # not used
        if self.is_applied_to(gig):
            self.applied_gigs.remove(gig)
            db.session.add(self)
            db.session.commit()

    def is_active(self):
        return self.activated

    def create_token_for(self, token_type):
        setattr(self, token_type + "_token", generate_token())  # transient attr
        setattr(self, token_type + "_hash",
                generate_hash(getattr(self, token_type + "_token")))
        setattr(self, token_type + "_sent_at", datetime.utcnow())
        db.session.add(self)
        db.session.commit()

    def activate(self, token):
        days_from_sending_activation = (datetime.utcnow() - self.activation_sent_at) \
                                           .total_seconds() / 86400
        if (days_from_sending_activation < 2
                and _check_token(self.activation_hash, token)):
            self.activated = True
            self.activation_hash = None
            db.session.add(self)
            db.session.commit()
            return True
        return False

    def check_reset_token(self, token):
        minutes_from_sending_reset = (datetime.utcnow() - self.reset_sent_at) \
                                         .total_seconds() / 60
        return (minutes_from_sending_reset < 30
                and _check_token(self.reset_hash, token))
