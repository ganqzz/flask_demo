from app import create_app, db
from app.models import User, Role

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.cli.command('db_init')
def db_init():
    db.drop_all()
    db.create_all()

    db.session.add(
        User(
            username='Hoge',
            email='hoge@hoge.com',
            password='p@ssword',
            location='Tokyo',
            description='Administrator',
            role_id=Role.ADMIN
        )
    )
    db.session.add(
        User(
            username='Fuga',
            email='fuga@fuga.com',
            password='password',
            location='Nagoya',
            description='Nagoya Symphonic Orchestra',
            role_id=Role.EMPLOYER
        )
    )
    db.session.add(
        User(
            username='Fefe',
            email='fefe@fefe.com',
            password='password',
            location='Osaka',
            description='I am an oboe player.',
            role_id=Role.MUSICIAN
        )
    )

    db.session.commit()
