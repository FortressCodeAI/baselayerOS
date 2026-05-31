import importlib
import pkgutil
import click


def autoload_commands(group: click.Group, package: str) -> None:
    """
    Auto-discovers all Click commands inside baselayeros.cli.commands.
    Any file that defines a top-level Click command or group will be loaded.
    """
    module = importlib.import_module(package)

    for mod in pkgutil.iter_modules(module.__path__, module.__name__ + "."):
        imported = importlib.import_module(mod.name)

        # Register any click.Command or click.Group found at module level
        for attr_name in dir(imported):
            attr = getattr(imported, attr_name)
            if isinstance(attr, click.Command):
                group.add_command(attr)
