from flask import Flask

from . import pages


# This is an application factory
def create_app():
    app = Flask(__name__)

    app.register_blueprint(pages.bp)
    return app

