from . import db
from .models import User, Movie


def db_drop():
    db.drop_all()


def db_create():
    db.create_all()


def db_seed():
    user = User(email='hoge@hoge.com', password='p@ssword')
    db.session.add(user)

    db.session.add(Movie(
        name="The Untouchables",
        casts="Kevin Costner, Robert De Niro, Sean Connery, Andy García",
        genres="Crime",
        user=user
    ))
    db.session.add(Movie(
        name="Die Hard",
        casts="Bruce Willis, Alan Rickman",
        genres="Action",
        user=user
    ))

    db.session.commit()


def db_init():
    db_drop()
    db_create()
    db_seed()


def register_commands(app):
    app.cli.command('db_drop')(db_drop)
    app.cli.command('db_create')(db_create)
    app.cli.command('db_seed')(db_seed)
    app.cli.command('db_init')(db_init)
