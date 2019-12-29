from flask import Flask, request

from app.i18n.babel_extension import babel
from config import get_env_config


def create_app(config_filename):
    app = Flask(__name__)

    # setup application environment
    app.config.from_object(config_filename)
    app.url_map.strict_slashes = False

    from app.i18n.babel_extension import babel
    babel.init_app(app)

    from app.database.sqlalchemy_extension import db
    db.init_app(app)

    from app.api.jwt_extension import jwt
    jwt.init_app(app)

    from app.api.api_extension import api
    api.init_app(app)

    from app.api.mail_extension import mail
    mail.init_app(app)

    from app.schedulers.background_scheduler import init_scheduler
    init_scheduler()

    return app


application = create_app(get_env_config())


@application.before_first_request
def create_tables():
    from app.database.sqlalchemy_extension import db
    db.create_all()


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(application.config['LANGUAGES'])


if __name__ == "__main__":
    application.run(port=5000)
