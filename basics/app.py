from flask import Flask, render_template, redirect, url_for, \
    request, abort, jsonify, Response, make_response

app = Flask(__name__)
app.secret_key = 'Nanika'  # config['SECRET_KEY']: needed by sessions or cookies


@app.route('/')  # GET, OPTIONS, HEAD
def index():
    return render_template("index.html")


@app.route('/hello')
def hello():
    name = request.args.get('name', 'Nanashi')  # args: query params (dict-like object)
    return "Hello, {}!".format(name)


@app.route('/res')
def response_demo():
    # (response, status code, headers)
    # (response, status code)
    # (response, headers)
    # response
    return 'Hoge', 200, {'Hoge': 'Hoge Hoge'}


@app.route('/json1')
def json_demo1():
    return Response('{"message": "Hello, World!"}',
                    mimetype="application/json",
                    status=200)


@app.route('/json2')
def json_demo2():
    return jsonify(message='Hello, World!')


@app.route('/json3')
def json_demo3():
    return {'message': 'Hello, World!'}  # dict only


@app.route('/image')
def get_image():
    return send_file('static/python.png', mimetype='image/png')


@app.route('/not_found')
def not_found():
    return 'That resource was not found', 404


@app.route('/abort')
def abort_demo():
    abort(404)


@app.route('/add/<int:num1>/<int:num2>')
@app.route('/add/<float:num1>/<float:num2>')
@app.route('/add/<int:num1>/<float:num2>')
@app.route('/add/<float:num1>/<int:num2>')
def add(num1, num2):
    print(request.view_args)
    context = {'num1': num1, 'num2': num2}
    return render_template("add.html", **context)


@app.route('/cookie', methods=["GET", "POST"])
def cookie():
    # !!!No CSRF protection!!!
    # Poor Cookie security!
    if request.method == "POST":
        resp = make_response(redirect(url_for('cookie')))
        resp.set_cookie('text', request.form.get('text', 'No Data'))
        return resp

    text = request.cookies.get('text', 'No Data')
    return render_template("cookie.html", text=text)


@app.errorhandler(404)
def page_not_found(e):
    # abort(404)
    return render_template('404.html'), 404


from people import people_bp

app.register_blueprint(people_bp, url_prefix="/people")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
