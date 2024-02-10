import sqlite3
import click
from flask import current_app, g


# current_app and g are flask objects that help to interact with application and storage
# current app object points to the flask app handling the current activity
# it can be used to access application-specific data, ie environment data
# g, refers to a global namespace object that can be used as a temp store 
# when a user makes a request

# so here we want to initialize the db if it doesn't exist or get the existing connection


def init_app(app):

    # registers the close_db function to be called with the db object in g is popped
    app.teardown_appcontext(close_db) # closes any lingering db connection, when the a
    
    app.cli.add_command(init_db_command)

@click.command("init-db")
def init_db_command():
    """initializes a database for the application"""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


def get_db():
    """initializes a database or reset an existing database
    """

    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # allows the database column by name ie providing a dictionary-like interface for accessing its data
        g.db.row_factory = sqlite3.Row 
    
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()