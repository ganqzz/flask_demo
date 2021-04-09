import unittest

from restful import create_app
from restful.commands import db_init, db_drop
from configs import TestConfig

app = create_app(TestConfig)


class BaseCase(unittest.TestCase):
    MOVIES = '/api/movies'
    AUTH = '/auth'
    SIGN_UP = AUTH + '/signup'
    LOGIN = AUTH + '/login'

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self):
        self.client = app.test_client()
        with app.app_context() as c:
            db_init()

    def tearDown(self):
        with app.app_context() as c:
            db_drop()
