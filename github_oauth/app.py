import os

import requests
from flask import Flask, request, jsonify

# from .env
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_API_URL = 'https://api.github.com'

app = Flask(__name__)


@app.route('/')
def index():
    return f'<a href="https://github.com/login/oauth/authorize?client_id={CLIENT_ID}">Login with Github</a>'


@app.route('/authorize')
def authorize():
    code = request.args.get('code')
    data = {'code': code, 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    headers = {'Accept': 'application/json'}
    r = requests.post(GITHUB_TOKEN_URL, data=data, headers=headers)
    json = r.json()
    print(json)

    # TODO: error

    token = json['access_token']
    print(token)
    headers['Authorization'] = f'Token {token}'
    r2 = requests.get(GITHUB_API_URL + '/user/repos', headers=headers)

    return jsonify(r2.json())


if __name__ == '__main__':
    app.run(debug=True)
