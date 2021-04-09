from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, \
    ValidationError, PasswordField, BooleanField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username *",
        validators=[
            InputRequired("Input is required!"),
            Length(min=4, max=20,
                   message="Input must be between 4 and 20 characters long"),
        ])
    email = EmailField(
        "Email *",
        validators=[
            InputRequired("Input is required!"),
            Length(max=255,
                   message="Input must be less equal to 255 characters long"),
            Email("Invalid Email format!"),
        ])
    password = PasswordField(
        "Password *",
        validators=[
            InputRequired("Input is required!"),
            Length(min=6, max=40,
                   message="Input must be between 6 and 40 characters long"),
            EqualTo("password_confirm", message="Passwords must match"),
        ])
    password_confirm = PasswordField(
        "Confirm Password *",
        validators=[InputRequired("Input is required!"), ])
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
    role = RadioField("I am *", coerce=int,
                      choices=((2, "Musician"), (3, "Employer")),
                      validators=[InputRequired("Input is required!")])
    submit = SubmitField("Register")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Username already exitsts")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email already exitsts")


def user_exists_with_email(form, field):
    """Custom validator"""
    user = User.query.filter_by(email=field.data).first()
    if not user:
        raise ValidationError("There is not registered account with that email")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email *",
        validators=[
            InputRequired("Input is required!"),
            Length(max=255,
                   message="Input must be less equal to 255 characters long"),
            Email("Invalid Email format!"),
            user_exists_with_email,
        ])
    password = PasswordField(
        "Password *",
        validators=[
            InputRequired("Input is required!"),
            Length(min=6, max=40,
                   message="Input must be between 6 and 40 characters long"),
        ])
    remember_me = BooleanField('Remember me')
    submit = SubmitField("Login")


class PasswordResetForm(FlaskForm):
    email = EmailField(
        "Your Email",
        validators=[
            InputRequired("Input is required!"),
            Length(max=255,
                   message="Input must be less equal to 255 characters long"),
            Email("Invalid Email format!"),
            user_exists_with_email,
        ])
    submit = SubmitField("Submit")


class UpdatePasswordForm(FlaskForm):
    password = PasswordField(
        "New password",
        validators=[
            InputRequired("Input is required!"),
            Length(min=6, max=40,
                   message="Input must be between 6 and 40 characters long"),
            EqualTo("password_confirm", message="Passwords must match"),
        ])
    password_confirm = PasswordField(
        "Confirm new Password",
        validators=[InputRequired("Input is required!"), ])
    submit = SubmitField("Update")
