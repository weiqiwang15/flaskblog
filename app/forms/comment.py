from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class PostCommentForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('发表评论')
