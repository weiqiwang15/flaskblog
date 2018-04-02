import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension


# 实例化 Flask 插件
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
moment = Moment()
toolbar = DebugToolbarExtension()


def create_app(script_info=None):

    # 实例化 Flask 应用
    app = Flask(
        __name__,
        template_folder='./templates',
        static_folder='./static',
    )

    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)

    # 配置 Flask 实例
    app_settings = os.getenv(
        'APP_SETTINGS',
        'app.config.DevelopmentConfig',
    )
    app.config.from_object(app_settings)

    # 设置 Flask 插件
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # 注册 blueprint
    from app.routes.home import main as home_blueprint
    from app.routes.user import main as user_blueprint
    from app.routes.post import main as post_blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(post_blueprint, url_prefix='/post')

    # 配置 Flask-Login
    from app.models.user import User, AnonymousUser
    login_manager.login_view = 'user.login'
    login_manager.session_protection = 'strong'
    login_manager.anonymous_user = AnonymousUser

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
