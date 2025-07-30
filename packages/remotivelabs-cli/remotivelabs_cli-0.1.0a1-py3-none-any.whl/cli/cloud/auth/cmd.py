from __future__ import annotations

import sys

import typer

from cli.cloud.auth.login import login as do_login
from cli.errors import ErrorPrinter
from cli.settings import TokenNotFoundError, settings
from cli.typer import typer_utils
from cli.utils.rest_helper import RestHelper as Rest

from .. import auth_tokens
from ..organisations import do_select_default_org

HELP = """
Manage how you authenticate with our cloud platform
"""
app = typer_utils.create_typer(help=HELP)
# app.add_typer(auth_tokens.app, name="credentials", help="Manage account credentials")


@app.command(name="login")
def login(browser: bool = typer.Option(default=True, help="Does not automatically open browser, instead shows a link")) -> None:
    """
    Login to the cli using browser

    If not able to open a browser it will show fallback to headless login and show a link that
    users can copy into any browser when this is unsupported where running the cli - such as in docker,
    virtual machine or ssh sessions.

    This will be used as the current access token in all subsequent requests. This would
    be the same as activating a personal access key or service-account access key.
    """
    do_login(headless=not browser)
    if settings.get_cli_config().get_active_default_organisation() is None:
        set_default_organisation = typer.confirm(
            "You have not set a default organisation\nWould you like to choose one now?", abort=False, default=True
        )
        if set_default_organisation:
            do_select_default_org(get=False)


@app.command()
def whoami() -> None:
    """
    Validates authentication and fetches your account information
    """
    try:
        Rest.handle_get("/api/whoami")
    except TokenNotFoundError as e:
        ErrorPrinter.print_hint(str(e))
        sys.exit(1)


@app.command()
def print_access_token() -> None:
    """
    Print current active token
    """
    try:
        print(settings.get_active_token())
    except TokenNotFoundError as e:
        ErrorPrinter.print_hint(str(e))
        sys.exit(1)


def print_access_token_file() -> None:
    """
    Print current active token and its metadata
    """
    try:
        print(settings.get_active_token_file())
    except TokenNotFoundError as e:
        ErrorPrinter.print_hint(str(e))
        sys.exit(1)


# @app.command(help="Clears active credentials")
def logout() -> None:
    settings.clear_active_token()
    print("Access token removed")


app.command("activate")(auth_tokens.select_personal_token)
app.command("list")(auth_tokens.list_pats_files)
