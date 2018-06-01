from flask_wtf import FlaskForm
from wtforms import *


class LangHandleForm(FlaskForm):
    submit_delete = SubmitField("Delete")
    submit_add = SubmitField("Create")
    submit_edit = SubmitField("Edit")


class LangWizard(FlaskForm):
    desc = StringField("Description")
    lang_iso639_1 = StringField(
        "ISO 639.1",
        validators=[validators.DataRequired("Field is required"), validators.Length(2, 2)]
    )
    submit = SubmitField("Save")
