"""This encapsulates the logic of each user action as command object

This follows the command pattern of writing software:
source: https://en.wikipedia.org/wiki/Command_pattern
"""

from database import DatabaseManager
from datetime import datetime

import sys

# why this though??
# Is this like a global variable??

db = DatabaseManager("bookmarks.db")


# but why create it as a class? and not just a method, because of the command pattern
class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table(
            "bookmarks",
            {
                "id": " integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


class AddBookmarkCommand:
    def execute(self, data):
        # adds the current datetime when the record is added to the table
        data["date_added"] = datetime.utcnow().isoformat()
        db.add("bookmarks", data)
        return "Bookmark added!"


class ListBookmarksCommand:
    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self):
        return db.select("bookmarks", order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    def execute(self, data):
        db.delete("bookmarks", {"id": data})
        return "Bookmark deleted!"


class QuitCommand:
    def execute(self):
        sys.exit()
