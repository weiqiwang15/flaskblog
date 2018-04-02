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
)
from app.models.user import User
from app.models.post import Post


main = Blueprint('home', __name__)


@main.route('/')
@main.route('/index')
def index():
    posts = Post.query.all()
    return render_template('home/index.html', posts=posts)
