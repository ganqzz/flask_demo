import secrets

from flask import Blueprint, render_template, redirect, url_for, \
    request, abort, jsonify, session

people_bp = Blueprint("people", __name__)


class Person:
    def __init__(self, first_name="", last_name=""):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return self.first_name + " " + self.last_name


# shared across the requests and clients
# 簡易的にlistのindexを"id"として利用しているので、並行してアクセスするときは注意
people = [
    Person('<em>Hoge</em>', 'Hoge'),
    Person('Fuga', 'Fuga'),
    Person('FeFe', 'FeFe'),
    Person('Piyo', 'Awawa'),
]


def create_csrf_token():
    csrf_token = session["csrf_token"] = secrets.token_urlsafe(32)
    return csrf_token


def check_csrf_token():
    saved_token = session.get("csrf_token", None)
    given_token = request.form.get("csrf_token", None)
    if (not saved_token
            or not given_token
            or not secrets.compare_digest(saved_token, given_token)):  # != による比較はタイミング攻撃に脆弱
        abort(403, f"expected='{saved_token}', actual='{given_token}'")


@people_bp.route("/", methods=["GET", "POST"])
def top():
    if request.method == "POST":
        check_csrf_token()
        first_name = request.form.get("first-name", "")
        last_name = request.form.get("last-name", "")

        person = Person(first_name, last_name)
        people.append(person)

        return redirect(url_for("people.top"))  # method name

    # GET
    return render_template("people/people.html", people=people,
                           csrf_token=create_csrf_token())


@people_bp.route("/<int:id>", methods=["GET", "POST"])
def update(id):
    try:
        person = people[id]
    except IndexError:
        abort(404)
    else:
        if request.method == "GET":
            create_csrf_token()
            return render_template("people/form_update.html", person=person,
                                   csrf_token=create_csrf_token())

        # POST
        person.first_name = request.form.get("first-name", "")
        person.last_name = request.form.get("last-name", "")
        return redirect(url_for("people.top"))


@people_bp.route("/<int:id>/delete", methods=["POST"])  # POSTだけに限定すること
def delete(id):
    check_csrf_token()
    try:
        del people[id]
        return redirect(url_for("people.top"))
    except IndexError:
        abort(404)


@people_bp.route("/api/")
def api_card_list():
    return jsonify([vars(p) for p in people])


@people_bp.route("/api/<int:index>")
def api_card_detail(index):
    try:
        return vars(people[index])
    except IndexError:
        abort(404)


@people_bp.errorhandler(403)
def page_not_found(e):
    # abort(403)
    return e, 403  # for the demo purpose only
