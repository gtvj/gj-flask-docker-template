from flask_wtf import FlaskForm
from wtforms import SubmitField
from lib.content import load_content, get_field_content


class HomeForm(FlaskForm):
    content = load_content()

    submit = SubmitField(
        get_field_content(content, "home", "call_to_action"),
    )
