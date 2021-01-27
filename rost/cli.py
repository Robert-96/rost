import click
from click_help_colors import HelpColorsGroup

from .generator import Rost


CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


searchpath = click.option(
    "--searchpath", type=click.Path(exists=True, file_okay=False),
    default="templates/", show_default=True,
    help="The directory to look in for templates.")

outputpath = click.option(
    "--outputpath", type=click.Path(exists=False, file_okay=False),
    default="dist/", show_default=True,
    help="The directory to place rendered files in.")

staticpath = click.option(
    "--staticpath", "staticpaths", type=click.Path(exists=False),
    default=("static/", ), show_default=True, multiple=True,
    help="The directory (or directories) within searchpath where static files (such as CSS and JavaScript) are stored.")


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


@click.group(
    context_settings=CONTEXT_SETTINGS,
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green"
)
@click.version_option(None, "--version", "-v")
def cli():
    """A simple static site generator based on Jinja2 with a CLI build using Click."""


@cli.command()
@add_options([
    searchpath,
    outputpath,
    staticpath
])
def build(searchpath, outputpath, staticpaths):
    """Build the project."""

    print(searchpath)
    print(outputpath)
    print(staticpaths)

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)
    rost.build()


@cli.command()
@add_options([
    searchpath,
    outputpath,
    staticpath
])
def watch(searchpath, outputpath, staticpaths):
    """Start an development server and re-build the project if the source directory for change."""

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)
    rost.watch()


if __name__ == "__main__":
    cli()
