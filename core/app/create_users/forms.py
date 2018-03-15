from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms import ValidationError


class MyEmailValidation(object):
    def __init__(self, message=None):
        if not message:
            message = "Email isn't valid."
        self.message = message

    def __call__(self, form, field):
        if "@" not in field.data:
            raise ValidationError(self.message)


class CreateUsersForm(FlaskForm):
    email = StringField("Destination email", validators=[DataRequired(), MyEmailValidation()])
    role_selector = SelectField(
        "Select role for new user",
        choices=[("admin", 3), ("moderator", 4), ("operator", 5)]
    )
    submit = SubmitField("Create user")
