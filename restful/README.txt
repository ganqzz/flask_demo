# REST API by Flask

- SQLAlchemy
- marshmallow
- JWT
- Mail

```
flask run
```

- Authentication (Json Web Token)
    * set the Authorization http-header: ``Authorization: Bearer <token string>``
    * client flow
        - expired => re-get an access token by accessing to /login

# ToDo

- filtering
