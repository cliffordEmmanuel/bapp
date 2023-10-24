import sqlite3


class DatabaseManager:
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        """Uses the cursor to execute SQL statements"""
        with self.connection:  # creates a database transaction context
            cursor = self.connection.cursor()
            cursor.execute(statement,values or [])  # provides any passed in values to the placeholders
            return cursor
