from storage import Storage
from cli import CLI
from predefined_data import load_predefined_data


def main():
    """
    Entry point for the Habit Tracker application.
    Initialises storage, loads predefined data,
    and starts the CLI.
    """
    storage = Storage()
    load_predefined_data(storage)
    cli = CLI(storage)
    cli.run()


if __name__ == "__main__":
    main()
    