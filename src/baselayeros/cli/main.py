import click
from baselayeros.cli.autoload import autoload_commands


@click.group(help="BaseLayerOS Command Line Interface")
def main():
    pass


# Auto-load all commands from baselayeros.cli.commands
autoload_commands(main, "baselayeros.cli.commands")


if __name__ == "__main__":
    main()
