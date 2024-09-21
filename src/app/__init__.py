from flask import Flask
from config.config import Config
from .routes import main_bp
from utils.log_utils import setup_logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_logging()
    app.register_blueprint(main_bp)

    return app
