import json
import unittest

from .base import BaseCase


class TestMovieApiEndpoint(BaseCase):

    def test_get_movies(self):
        response = self.client.get(self.MOVIES + '/')  # 308を避けるため"/"を付加
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual(2, len(response.json))

    @unittest.skip('SUT is not implemented')
    def test_get_movies_filtered(self):
        response = self.client.get(self.MOVIES + '/?q={}'.format('hoge'))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual(2, len(response.json))

    def test_get_movie_by_id(self):
        response = self.client.get(self.MOVIES + '/2')
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.is_json)
        self.assertEqual('Die Hard', response.json['name'])

    def _login(self):
        payload = json.dumps({
            "email": "hoge@hoge.com",
            "password": "p@ssword"
        })
        response = self.client.post(self.LOGIN,
                                    headers={"Content-Type": "application/json"},
                                    data=payload)
        return response.json['token']

    def test_create_movie(self):
        # Given
        login_token = self._login()

        movie_payload = json.dumps({
            "name": "Star Wars: The Rise of Skywalker",
            "casts": "Daisy Ridley, Adam Driver",
            "genres": "Fantasy, Sci-fi"
        })

        # When
        response = self.client.post(
            self.MOVIES + '/',
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {login_token}"},
            data=movie_payload
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertTrue(response.is_json)
        res_data = response.get_json()
        self.assertTrue(isinstance(res_data.get("id"), int))
        self.assertEqual(1, res_data.get("user"))
        self.assertEqual('Star Wars: The Rise of Skywalker', res_data['name'])

    def test_update_movie(self):
        # Given
        login_token = self._login()

        movie_payload = json.dumps({
            "name": "Star Wars: The Rise of Skywalker",
            "casts": "Daisy Ridley, Adam Driver",
            "genres": "Fantasy, Sci-fi"
        })

        # When
        response = self.client.put(
            self.MOVIES + '/1',
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {login_token}"},
            data=movie_payload
        )

        # Then
        self.assertEqual(200, response.status_code)
        res_data = response.get_json()
        self.assertEqual(1, res_data.get("id"))
        self.assertEqual(1, res_data.get("user"))
        self.assertEqual('Star Wars: The Rise of Skywalker', res_data['name'])
