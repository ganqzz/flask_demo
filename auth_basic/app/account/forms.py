from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length


class UpdateAccountForm(FlaskForm):
    location = StringField(
        "Location *",
        validators=[
            InputRequired("Input is required!"),
            Length(min=3, max=100,
                   message="Input must be between 3 and 100 characters long"),
        ])
    description = TextAreaField(
        "Description *",
        validators=[
            InputRequired("Input is required!"),
            Length(max=1000,
                   message="Input must be less equal to 1000 characters long"),
        ])
    submit = SubmitField("Update")


class DeleteAccountForm(FlaskForm):
    submit = SubmitField("Delete")
