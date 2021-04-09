import json

from restful import crud
from .base import BaseCase, app


class TestAuthEndpoint(BaseCase):

    # --- Sign-up Tests

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email": "fuga@fuga.com",
            "password": "mycoolpassword"
        })

        # When
        response = self.client.post(self.SIGN_UP,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(201, response.status_code)
        self.assertTrue(response.is_json)
        res_data = response.get_json()
        self.assertTrue(isinstance(res_data.get("id"), int))
        self.assertEqual("fuga@fuga.com", res_data['email'])
        self.assertEqual(str, type(res_data['password']))

    def test_signup_with_non_existing_field(self):
        # Given
        payload = json.dumps({
            "xxxxx": "hoge123",
            "email": "fuga@fuga.com",
            "password": "mycoolpassword"
        })

        # When
        response = self.client.post(self.SIGN_UP,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(400, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual('bad request', response.json['error'])
        self.assertIsNotNone(response.json['message'].get('xxxxx'))

    def test_signup_without_email(self):
        # Given
        payload = json.dumps({
            "password": "mycoolpassword",
        })

        # When
        response = self.client.post(self.SIGN_UP,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(400, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual('bad request', response.json['error'])
        self.assertIsNotNone(response.json['message'].get('email'))

    def test_signup_without_password(self):
        # Given
        payload = json.dumps({
            "email": "fuga@fuga.com",
        })

        # When
        response = self.client.post(self.SIGN_UP,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(400, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual('bad request', response.json['error'])
        self.assertIsNotNone(response.json['message'].get('password'))

    def test_signup_already_existing_user(self):
        # Given
        with app.app_context():
            user = crud.get_user_by_id(1)

        payload = json.dumps({
            "email": user.email,  #
            "password": "mycoolpassword"
        })

        # When
        response = self.client.post(self.SIGN_UP,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(400, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual('bad request', response.json['error'])
        self.assertTrue(response.json['message'].strip())

    # --- Login Tests

    def test_successful_login(self):
        # Given
        payload = json.dumps({
            "email": "hoge@hoge.com",
            "password": "p@ssword"
        })

        # When
        response = self.client.post(self.LOGIN,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual(str, type(response.json['token']))

    # TODO: Test for format check

    def test_login_with_invalid_email(self):
        # Given
        no_registered_email = "fuga@fuga.com"
        payload = json.dumps({
            "email": no_registered_email,  #
            "password": "p@ssword"
        })

        # When
        response = self.client.post(self.LOGIN,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(401, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual('unauthorized', response.json['error'])
        self.assertEqual(f'user({no_registered_email}) not found', response.json['message'])

    def test_login_with_invalid_password(self):
        # Given
        payload = json.dumps({
            "email": "hoge@hoge.com",
            "password": "mycoolpassword"  #
        })

        # When
        response = self.client.post(self.LOGIN,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(401, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual('unauthorized', response.json['error'])
        self.assertEqual('password not match', response.json['message'])
