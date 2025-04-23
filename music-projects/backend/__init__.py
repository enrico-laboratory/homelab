import logging
from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api

from backend.db import db
from backend.routes.choir import blp as choir_blp
from backend.routes.music_project import blp as music_project_blp
from backend.routes.task import blp as task_blp

MUSIC_PROJECT_SQLITE_DB_FOLDER = 'instance/'
MUSIC_PROJECT_SQLITE_DB_FILENAME = 'music_projects.db'
MUSIC_PROJECTS_SQLITE_DB_URL = 'sqlite:///{folder}{filename}'

load_dotenv('.env')

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def create_app(db_url=None) -> Flask:

    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or getenv(
        "DATABASE_URL", "sqlite:///music_projects.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    api = Api(app)
    api.register_blueprint(choir_blp)
    api.register_blueprint(music_project_blp)
    api.register_blueprint(task_blp, url_prefix='/api')

    db.init_app(app)

    return app