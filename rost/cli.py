import logging

import click
from click_help_colors import HelpColorsGroup

from .generator import Rost


ASCI_ART = """\

    RRRRRRRRRRRRRRRRR                                              tttt
    R::::::::::::::::R                                          ttt:::t
    R::::::RRRRRR:::::R                                         t:::::t
    RR:::::R     R:::::R                                        t:::::t
      R::::R     R:::::R   ooooooooooo       ssssssssss   ttttttt:::::ttttttt
      R::::R     R:::::R oo:::::::::::oo   ss::::::::::s  t:::::::::::::::::t
      R::::RRRRRR:::::R o:::::::::::::::oss:::::::::::::s t:::::::::::::::::t
      R:::::::::::::RR  o:::::ooooo:::::os::::::ssss:::::stttttt:::::::tttttt
      R::::RRRRRR:::::R o::::o     o::::o s:::::s  ssssss       t:::::t
      R::::R     R:::::Ro::::o     o::::o   s::::::s            t:::::t
      R::::R     R:::::Ro::::o     o::::o      s::::::s         t:::::t
      R::::R     R:::::Ro::::o     o::::ossssss   s:::::s       t:::::t    tttttt
    RR:::::R     R:::::Ro:::::ooooo:::::os:::::ssss::::::s      t::::::tttt:::::t
    R::::::R     R:::::Ro:::::::::::::::os::::::::::::::s       tt::::::::::::::t
    R::::::R     R:::::R oo:::::::::::oo  s:::::::::::ss          tt:::::::::::tt
    RRRRRRRR     RRRRRRR   ooooooooooo     sssssssssss              ttttttttttt

"""


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


def validate_log_level(ctx, param, value):
    if value is None or isinstance(value, int):
        return value

    log_level = getattr(logging, value.upper(), None)
    if not isinstance(log_level, int):
        raise click.BadParameter("Level {!r} is not a valid log level.".format(value))

    return log_level


def config_logging(log_level, log_file=None):
    if log_level is None:
        return

    logger = logging.getLogger(__package__)
    logger.setLevel(log_level)

    if log_file:
        logger.addHandler(logging.FileHandler(log_file))
    else:
        logger.addHandler(logging.StreamHandler())


CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


searchpath_option = click.option(
    "--searchpath", type=click.Path(exists=True, file_okay=False),
    default="templates/", show_default=True,
    help="The directory to look in for templates."
)

outputpath_option = click.option(
    "--outputpath", type=click.Path(exists=False, file_okay=False),
    default="dist/", show_default=True,
    help="The directory to place rendered files in."
)

staticpath_option = click.option(
    "--staticpath", "staticpaths", type=click.Path(exists=False),
    default=("static/", ), show_default=True, multiple=True,
    help="The directory (or directories) within searchpath where static files (such as CSS and JavaScript) are stored."
)

livereload_option = click.option(
    "--livereload/--no-livereload", "use_livereload", is_flag=True, default=False, show_default=True,
    help="If set will start a livereload server."
)

bind_option = click.option(
    "--bind", "-b", default="localhost", show_default=True,
    help="The address to which the server should bind."
)

port_option = click.option(
    "--port", "-p", default=8080, show_default=True,
    help="The port to which the server should lissen."
)

log_level_option = click.option(
    "--log-level", type=click.UNPROCESSED, callback=validate_log_level,
    help="The log level for the package level logger."
)

log_file_option = click.option(
    "--log-file", type=click.Path(),
    help="If set will log to a file rather that stderr."
)


@click.group(
    context_settings=CONTEXT_SETTINGS,
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green"
)
@click.version_option(None, "--version", "-v")
def cli():
    """A simple static site generator based on Jinja2 with a CLI build using Click."""

    click.secho(ASCI_ART, fg="bright_black", bold=True)


@cli.command()
@add_options([
    searchpath_option,
    outputpath_option,
    staticpath_option,
    log_level_option,
    log_file_option,
])
def build(searchpath, outputpath, staticpaths, log_level, log_file):
    """Build the project."""

    config_logging(log_level, log_file)

    click.echo("    Searchpath:  {}".format(click.style(searchpath, fg="blue", bold=True)))
    click.echo("    Outputpath:  {}".format(click.style(outputpath, fg="blue", bold=True)))
    click.echo("    Staticpaths: {}".format(", ".join([click.style(p, fg="blue", bold=True) for p in staticpaths])))
    click.echo("")

    click.secho(">>> Build project...", bold=True, fg="bright_black")

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths)
    rost.build()

    click.secho(">>> Project successfully build.\n", bold=True, fg="green")


@cli.command()
@add_options([
    searchpath_option,
    outputpath_option,
    staticpath_option,
    bind_option,
    port_option,
    livereload_option,
    log_level_option,
    log_file_option
])
def watch(searchpath, outputpath, staticpaths, bind, port, use_livereload, log_level, log_file):
    """Start a development server and re-build the project on change."""

    config_logging(log_level, log_file)

    def before_callback(**kwargs):
        click.echo()
        click.secho(">>> Build project...", bold=True, fg="bright_black")

    def after_callback(**kwargs):
        click.secho(">>> Successfully build.", bold=True, fg="green")
        click.echo()

    monitorpaths = []
    url = "http://{}:{}/".format(bind, port)

    click.echo("    Searchpath:   {}".format(click.style(searchpath, fg="blue", bold=True)))
    click.echo("    Outputpath:   {}".format(click.style(outputpath, fg="blue", bold=True)))
    click.echo("    Staticpaths:  {}".format(", ".join([click.style(p, fg="blue", bold=True) for p in staticpaths])))
    click.echo("    Monitorpaths: {}".format(", ".join([click.style(p, fg="blue", bold=True) for p in monitorpaths])))
    click.echo()

    click.secho(">>> Serving on {}".format(click.style(url, fg="cyan")), bold=True, fg="bright_black")
    click.secho(">>> Press Ctrl + C to stop...", bold=True, fg="bright_black")

    rost = Rost(searchpath=searchpath, outputpath=outputpath, staticpaths=staticpaths,
                before_callback=before_callback, after_callback=after_callback)
    rost.watch(monitorpaths=monitorpaths, bind=bind, port=port, use_livereload=use_livereload)

    click.echo()
    click.secho(">>> Server closed.", bold=True, fg="bright_black")
    click.secho(">>> File monitor closed.", bold=True, fg="bright_black")
    click.echo()


if __name__ == "__main__":
    cli()
