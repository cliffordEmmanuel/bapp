import sqlite3


class DatabaseManager:
    """Manages the database connection, and executes sql statements"""

    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        """Uses the cursor to execute SQL statements"""
        with self.connection:  # creates a database transaction context
            cursor = self.connection.cursor()
            cursor.execute(
                statement, values or []
            )  # provides any passed in values to the placeholders
            return cursor

    def create_table(self, table_name, columns):
        # expected format looks like this:
        # CREATE TABLE IF NOT EXISTS bookmarks
        # (
        #   id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     title TEXT NOT NULL,
        #     url TEXT NOT NULL,
        #     notes TEXT,
        #     date_added TEXT NOT NULL
        # );

        # columns is dictionary of columns mapped to their data types and constraints
        columns_with_types = [
            f"{column_name} {data_type}" for column_name, data_type in columns.items()
        ]

        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            """
        )

        # generalization isn't the same as optimization??
        # Case for this I know we're working with just bookmarks
        # but rather than hard code the table name we choose to make it a variable
        # the same for the create table query.
        # parameterized than hard coded or??

        # Building the C in CRUD ie Adding records

        # A record looks like this:
        # INSERT INTO bookmarks
        # (title, url, notes, date_added)
        # VALUES('GitHub', 'https://github.com', 'A place to store repositories of code', '2019-02-01T18:46:32.125467');

        # It's a good idea to use placeholders in building sql queries

    def add(self, table_name, data):
        # data is a dictionary mapping column names to column values
        placeholders = ", ".join("?" * len(data))  # once again generalization huh!!
        column_names = ", ".join(data.keys())
        column_values = tuple(
            data.values()
        )  # cursor.execute for sqlite3 cannot handle the dict_values object

        self._execute(
            f"""
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            """,
            column_values,
        )

    # Building the D in CRUD ie delete records
    # query should look like this
    # DELETE FROM bookmarks
    # WHERE ID = 3;

    def delete(self, table_name, criteria):
        # constructs the value for the where clause
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            """,
            tuple(criteria.values()),
        )

    # Building the R in CRUD ie Read records
    # query should look like this:
    # SELECT * FROM bookmarks
    # WHERE ID = 3;

    # In addition, you can sort results by a specific column using an ORDER BY clause:
    # SELECT * FROM bookmarks
    # WHERE ID = 3
    # ORDER BY title;

    # This select method by default will fetch all records,
    # you can use the criteria to specify the specific columns to return
    # also an order by argument that specifies a column to sort the results by (default is the primary key)

    def select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}

        query = f"SELECT * FROM {table_name}"

        if criteria:
            placeholders = [f"{column} ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"

        # TODO: check this
        # why no placeholders for the order by columns,
        # how to specify the primary default, will it be a string?? or a list
        if order_by:
            query += f" ORDER BY {order_by}"

        return self._execute(
            query,
            tuple(criteria.values()),
        )
