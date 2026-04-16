from storage import Storage
from cli import CLI
from predefined_data import load_predefined_data


def main():#entry point for habit which launches the app
    storage = Storage()
    load_predefined_data(storage)
    cli = CLI(storage)
    cli.run()


if __name__ == "__main__":
    main()
    