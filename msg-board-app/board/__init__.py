import os
from dotenv import load_dotenv
from flask import Flask

from board import pages, posts, database

load_dotenv()

# This is the application factory
def create_app():
    app = Flask(__name__)
    # makes all environment variables that start with FLASK_ available to the app
    app.config.from_prefixed_env() 

    database.init_app(app)

    app.register_blueprint(pages.bp)
    app.register_blueprint(posts.bp)
    print(f"Current Environment: {os.getenv('ENVIRONMENT')}") # for any other environment variables
    print(f"Using Database: {app.config.get('DATABASE')}") # shortcut access to FLASK_ environment variables...
    return app

