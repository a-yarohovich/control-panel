from flask_wtf import FlaskForm
from wtforms import *


class CountryForm(FlaskForm):
    submit = SubmitField("Display country's")
