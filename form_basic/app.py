import datetime
import os
import sqlite3
from secrets import token_hex

from flask import Flask, jsonify, send_from_directory, render_template, \
    request, redirect, url_for, g, flash
from flask_wtf import CSRFProtect
from flask_wtf.file import FileRequired
from werkzeug.utils import escape, unescape, secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secretkey"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["jpeg", "jpg", "png", "gif"]
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["IMAGE_UPLOADS"] = os.path.join(basedir, "uploads")

csrf = CSRFProtect(app)  # サイト全体で自動CSRFチェックを有効にする（Formを経由しないAJAXやDELETEの場合など）


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("db/globomantics.db")  # memoization
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


import crud
from forms import NewItemForm, EditItemForm, DeleteItemForm, \
    FilterForm, NewCommentForm


@app.route("/")
def home():
    form = FilterForm(request.args, meta={"csrf": False})  # データ変更なしのためCSRF対策不要

    categories = crud.get_categories()
    categories.insert(0, (0, "---"))
    form.category.choices = categories

    subcategories = crud.get_subcategories()
    subcategories.insert(0, (0, "---"))
    form.subcategory.choices = subcategories

    if form.validate():
        items = crud.get_items(title=escape(form.title.data.strip()),
                               category_id=form.category.data,
                               subcategory_id=form.subcategory.data,
                               order=form.price.data)
    else:
        items = crud.get_items()

    # jQueryの場合は、"X-Requested-With: XMLHttpRequest"ヘッダーで判別する方法もある
    if request.args.get("ajax", type=int):  # MultiDict(TypeConversionDict)
        return render_template("_items.html", items=items)

    return render_template("home.html", items=items, form=form)


@app.route("/category/<int:category_id>")
def category(category_id):
    subcategories = crud.get_subcategories(category_id)
    return jsonify(subcategories=subcategories)


@app.route("/item/<int:item_id>")
def item_detail(item_id):
    item = crud.get_item(item_id)
    if item:
        comments = crud.get_comments(item_id)
        commentForm = NewCommentForm()
        commentForm.item_id.data = item_id
        deleteItemForm = DeleteItemForm()
        return render_template("item.html", item=item, comments=comments,
                               commentForm=commentForm, deleteItemForm=deleteItemForm)
    return redirect(url_for("home"))


def save_image_upload(image):
    format = "%Y%m%dT%H%M%S"
    now = datetime.datetime.utcnow().strftime(format)
    random_string = token_hex(2)
    filename = random_string + "_" + now + "_" + image.data.filename
    filename = secure_filename(filename)
    image.data.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
    return filename


@app.route("/item/new", methods=["GET", "POST"])
def new_item():
    form = NewItemForm()
    form.category.choices = crud.get_categories()
    form.subcategory.choices = crud.get_subcategories()

    # POST
    if form.validate_on_submit() and \
            form.image.validate(form, extra_validators=(FileRequired(),)):
        filename = save_image_upload(form.image)

        # create data
        # escape()したデータはテンプレートでsafeフィルターを併用すること
        crud.create_item(title=escape(form.title.data),
                         description=escape(form.description.data),
                         price=float(form.price.data),
                         image=filename,
                         category_id=form.category.data,
                         subcategory_id=form.subcategory.data, )

        # Redirect to some page
        flash("Item {} has been successfully submitted"
              .format(request.form.get("title")), "success")
        return redirect(url_for("home"))

    # GET
    return render_template("new_item.html", form=form)


@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)


@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
    item = crud.get_item_no_categories(item_id)
    if item:
        form = EditItemForm()
        if form.validate_on_submit():
            filename = save_image_upload(form.image) if form.image.data \
                else item["image"]

            # update data
            # escape()したデータはテンプレートでsafeフィルターを併用すること
            crud.update_item(item_id,
                             title=escape(form.title.data),
                             description=escape(form.description.data),
                             price=float(form.price.data),
                             image=filename)

            flash("Item {} has been successfully updated".format(form.title.data), "success")
            return redirect(url_for("item", item_id=item_id))

        form.title.data = unescape(item["title"])
        form.description.data = unescape(item["description"])
        form.price.data = item["price"]
        return render_template("edit_item.html", item=item, form=form)

    return redirect(url_for("home"))


@app.route("/item/<int:item_id>/delete", methods=["POST"])  # GETは許可しないようにする
def delete_item(item_id):
    item = crud.get_item_no_categories(item_id)
    if item:
        crud.delete_item(item_id)
        flash("Item {} has been successfully deleted.".format(item["title"]), "success")
    else:
        flash("This item does not exist.", "danger")

    return redirect(url_for("home"))


@app.route("/comment/new", methods=["POST"])
def new_comment():
    is_ajax = request.form.get("ajax", type=int)  # MultiDict(TypeConversionDict)

    form = NewCommentForm()

    if form.validate_on_submit():
        crud.create_comment(item_id=form.item_id.data,
                            content=escape(form.content.data))

        if is_ajax:
            return render_template("_comment.html", content=form.content.data)

    if is_ajax:
        return "Content is required.", 400

    return redirect(url_for("item_detail", item_id=form.item_id.data))
