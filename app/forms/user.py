from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='此项不能为空')])
    password = PasswordField('密码', validators=[DataRequired(message='此项不能为空')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='此项不能为空'),
            Length(2, 32, message='用户名的字符长度必须大于2小于32'),
        ],
    )
    email = StringField(
        '邮箱',
        validators=[
            DataRequired(message='此项不能为空'),
            Email(),
            Length(1, 64, message='用户名的字符长度必须大于1小于64'),
        ],
    )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='此项不能为空'),
            Length(2, 20, message='密码的字符长度必须大于2小于20'),
        ],
    )
    password2 = PasswordField(
        '确认密码',
        validators=[
            DataRequired('此项不能为空'),
            EqualTo('password', message='两次输入的密码必须一致'),
        ],
    )
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被注册')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被注册')


class SettingUsernameForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='此项不能为空'),
            Length(2, 32, message='用户名的字符长度必须大于2小于32'),
        ],
    )
    submit = SubmitField('提交修改')


class SettingPasswordForm(FlaskForm):
    password = PasswordField(
        '新密码',
        validators=[
            DataRequired(message='此项不能为空'),
            Length(2, 20, message='密码的字符长度必须大于2小于20'),
        ],
    )
    password2 = PasswordField(
        '确认新密码',
        validators=[
            DataRequired('此项不能为空'),
            EqualTo('password', message='两次输入的密码必须一致'),
        ],
    )
    submit = SubmitField('提交修改')


class SettingSignatureForm(FlaskForm):
    signature = TextAreaField(
        '个性签名',
    )
    submit = SubmitField('提交修改')
