from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class NewPostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 128)])
    body = TextAreaField('正文', validators=[DataRequired()])
    submit = SubmitField('发表文章')


class EditPostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 128)])
    body = TextAreaField('正文', validators=[DataRequired()])
    submit = SubmitField('提交修改')
