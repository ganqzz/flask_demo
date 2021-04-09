from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, TextAreaField, SubmitField, DecimalField
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms.widgets import Input


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
    # NumberRangeからmin/maxへの反映については調査中。v3待ち？
    widget = PriceInput()


class GigForm(FlaskForm):
    title = StringField(
        "Title *",
        validators=[
            InputRequired("Input is required!"),
            Length(min=5, max=100,
                   message="Input must be between 5 and 100 characters long"),
        ])
    description = TextAreaField(
        "Description *",
        validators=[
            InputRequired("Input is required!"),
            Length(max=1000,
                   message="Input must be less equal to 1000 characters long"),
        ])
    payment = PriceField(
        'Payment',
        validators=[
            InputRequired("Input is required!"),
            NumberRange(min=0),
        ])
    location = StringField(
        "Location *",
        validators=[
            InputRequired("Input is required!"),
            Length(min=3, max=100,
                   message="Input must be between 3 and 100 characters long"),
        ])


class CreateGigForm(GigForm):
    submit = SubmitField("Create")


class UpdateGigForm(GigForm):
    submit = SubmitField("Update")
