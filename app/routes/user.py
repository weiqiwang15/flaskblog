from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    Blueprint,
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from app import db
from app.forms.user import (
    LoginForm,
    RegistrationForm,
    SettingUsernameForm,
    SettingPasswordForm,
    SettingSignatureForm,
)
from app.models.user import User
from app.models.post import Post


main = Blueprint('user', __name__)


@main.route('/login', methods=['GET', 'POST'])
def login():
    # 用户已登录
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    # 用户未登录
    else:
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.query.filter_by(username=form.username.data).first()
                if user is not None and user.verify_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    next = request.args.get('next')
                    if next is None or not next.startswith('/'):
                        next = url_for('home.index')
                    return redirect(next)
                else:
                    flash('用户名或密码无效')
                    return render_template('user/login.html', form=form)
            else:
                return render_template('user/login.html', form=form)
        else:
            return render_template('user/login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    # 用户已登录
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    # 用户未登录
    else:
        error = None
        form = RegistrationForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                new_user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                )
                db.session.add(new_user)
                db.session.commit()
                flash('恭喜, 您已成功注册, 请登录')
                return redirect(url_for('.login'))
            else:
                return render_template('user/register.html', form=form, error=error)
        else:
            return render_template('user/register.html', form=form, error=error)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录')
    return redirect(url_for('home.index'))


@main.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.time_modified.desc()).all()
    return render_template('user/user.html', user=user, posts=posts)


@main.route('/settings', methods=['GET'])
@login_required
def settings():
    user = current_user._get_current_object()
    form_username = SettingUsernameForm()
    form_password = SettingPasswordForm()
    form_signature = SettingSignatureForm()
    form_username.username.data = user.username
    form_signature.signature.data = user.signature
    return render_template(
        'user/settings.html',
        form_username=form_username,
        form_password=form_password,
        form_signature=form_signature,
    )


@main.route('/settings/change_username', methods=['POST'])
@login_required
def change_username():
    user = current_user._get_current_object()
    form_username = SettingUsernameForm()
    if form_username.validate_on_submit():
        user.username = form_username.username.data
        db.session.add(user)
        db.session.commit()
        flash('恭喜, 您已成功修改用户名!')
    return redirect(url_for('.settings'))


@main.route('/settings/change_password', methods=['POST'])
@login_required
def change_password():
    user = current_user._get_current_object()
    form_password = SettingPasswordForm()
    if form_password.validate_on_submit():
        user.password = form_password.password.data
        db.session.add(user)
        db.session.commit()
        flash('恭喜, 您已成功修改密码!')
    return redirect(url_for('.settings'))


@main.route('/settings/signature', methods=['POST'])
@login_required
def change_signature():
    user = current_user._get_current_object()
    form_signature = SettingSignatureForm()
    if form_signature.validate_on_submit():
        user.signature = form_signature.signature.data
        db.session.add(user)
        db.session.commit()
        flash('恭喜, 您已成功修改个性签名!')
    return redirect(url_for('.settings'))
