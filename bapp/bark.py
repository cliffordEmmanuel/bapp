"""This is the presentation layer for the cli application"""
import os

import commands


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call  # accounts for an optional preparation step for a specific command

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        # return the option as its name
        return self.name


def print_options(options):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    """Gets the user specified choice ie the symbol also making sure only the valid choice is chosen.

    :param options: Dictionary containing the specific action and its corresponding symbol
    :return: an option object that points to a specific command tied to the user chosen symbol.
    """
    # Quite interesting pattern for using the while loop:

    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")

    return options[choice.upper()]  # this is an Option object


# Handling commands where the extra input is needed from the user ie bookmark information
# So we're writing general purpose functions to encapsulate specific behavior
def get_user_input(label, required=True):
    """General purpose function for getting data from the user

    :param label: the associated info needed to be displayed to the user
    :param required:
    :return:
    """
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


def get_new_bookmark_data():
    """Prompts user for bookmark data

    :return:
    """
    return {
        "title": get_user_input("Title"),
        "url": get_user_input("URL"),
        "notes": get_user_input("Notes", required=False),
    }


def get_bookmark_id_for_deletion():
    return get_user_input("Enter a bookmark ID to delete")


def clear_screen():
    """Clear screen

    :return:
    """
    clear = "cls" if os.name == "nt" else "clear"
    os.system(clear)


def loop():
    options = {
        "A": Option(
            "Add a bookmark",
            commands.AddBookmarkCommand(),
            prep_call=get_new_bookmark_data,
        ),
        "B": Option("List bookmarks by date", commands.ListBookmarksCommand()),
        "T": Option(
            "List bookmarks by title", commands.ListBookmarksCommand(order_by="title")
        ),
        "D": Option(
            "Delete a bookmark",
            commands.DeleteBookmarkCommand(),
            prep_call=get_bookmark_id_for_deletion,
        ),
        "Q": Option("Quit", commands.QuitCommand()),
    }

    clear_screen()
    print_options(options)
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()


if __name__ == "__main__":
    commands.CreateBookmarksTableCommand().execute()

    print("Welcome to Bark!")

    while True:
        loop()
