from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from markupsafe import Markup
from wtforms import DecimalField, StringField, TextAreaField, SelectField, \
    SubmitField, HiddenField, ValidationError
from wtforms.validators import InputRequired, DataRequired, Length
from wtforms.widgets import Input

from app import app, get_db


class PriceInput(Input):
    input_type = "number"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        kwargs.setdefault("step", "0.01")
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True

        return Markup("""<div class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text">$</span>
                    </div>
                    <input %s>
        </div>""" % self.html_params(name=field.name, **kwargs))


class PriceField(DecimalField):
    widget = PriceInput()


class ItemForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!"),
            Length(min=5, max=20,
                   message="Input must be between 5 and 20 characters long")
        ])
    price = PriceField("Price")
    description = TextAreaField(
        "Description",
        validators=[
            InputRequired("Input is required!"),
            DataRequired("Data is required!"),
            Length(min=5, max=40,
                   message="Input must be between 5 and 40 characters long")
        ])
    image = FileField(
        "Image",
        validators=[
            FileAllowed(app.config["ALLOWED_IMAGE_EXTENSIONS"], "Images only!")
        ])


# refer to WTForms source
# DB validationをFormでやるかどうかは考慮する点
class BelongsToOtherFieldOption:
    def __init__(self, table, belongs_to, foreign_key=None, message=None):
        if not table:
            raise AttributeError("""
            BelongsToOtherFieldOption validator needs the table parameter
            """)
        if not belongs_to:
            raise AttributeError("""
            BelongsToOtherFieldOption validator needs the belongs_to parameter
            """)

        self.table = table
        self.belongs_to = belongs_to

        if not foreign_key:
            foreign_key = belongs_to + "_id"
        if not message:
            message = "Chosen option is not valid."

        self.foreign_key = foreign_key
        self.message = message

    def __call__(self, form, field):
        c = get_db().cursor()
        try:
            c.execute("SELECT COUNT(*) FROM {} WHERE id = ? AND {} = ?".format(
                self.table, self.foreign_key
            ), (field.data, getattr(form, self.belongs_to).data))
        except Exception as e:
            raise AttributeError("Passed parameters are not correct. {}".format(e))
        exists = c.fetchone()[0]
        if not exists:
            raise ValidationError(self.message)


class NewItemForm(ItemForm):
    category = SelectField("Category", coerce=int)
    subcategory = SelectField(
        "Subcategory",
        coerce=int,
        validators=[
            BelongsToOtherFieldOption(
                table="subcategories",
                belongs_to="category",
                message="Subcategory does not belong to that category.")
        ])
    submit = SubmitField("Submit")


class EditItemForm(ItemForm):
    submit = SubmitField("Update item")


class DeleteItemForm(FlaskForm):
    submit = SubmitField("Delete item")


class FilterForm(FlaskForm):
    title = StringField("Title", validators=[Length(max=20)])
    price = SelectField("Price", coerce=int,
                        choices=[(0, "---"), (1, "Max to Min"), (2, "Min to Max")])
    category = SelectField("Category", coerce=int)
    subcategory = SelectField("Subcategory", coerce=int)
    submit = SubmitField("Filter")


class NewCommentForm(FlaskForm):
    content = TextAreaField("Comment",
                            validators=[
                                InputRequired("Input is required."),
                                DataRequired("Data is required.")
                            ])
    item_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Submit")
