Flask
=====

ENVs
---

- FLASK_APP=app.py  # default
- FLASK_ENV=development


Commands
---

- Run local server (127.0.0.1:5000)
```
flask run  # app.py

export FLASK_APP=hoge.py
flask run
```

- Routes (Flask.url_map)
```
flask routes
```


Tips
---

- Context "globals"
    Can access across the threads
    * current_app
        Active application instance
    * g
        Temporary storage during the request lifetime
    * request
        Holds the contents of a HTTP request
    * session
        Dictionary for remembering values across the requests

- Context "locals"
    Thread local
    can access from another views or templates by using a LocalProxy
