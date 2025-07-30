from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Any, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import typer
from rich.console import Console
from typing_extensions import override

from cli.cloud.auth_tokens import list_and_select_personal_token
from cli.errors import ErrorPrinter
from cli.settings import TokenNotFoundError, settings
from cli.utils.rest_helper import RestHelper as Rest

httpd: HTTPServer

console = Console()


def generate_pkce_pair() -> Tuple[str, str]:
    """
    PKCE is used for all cli login flows, both headless and browser.
    """
    code_verifier_ = secrets.token_urlsafe(64)  # High-entropy string
    code_challenge_ = base64.urlsafe_b64encode(hashlib.sha256(code_verifier_.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    return code_verifier_, code_challenge_


code_verifier, code_challenge = generate_pkce_pair()
state = secrets.token_urlsafe(16)

short_lived_token = None


class S(BaseHTTPRequestHandler):
    def _set_response(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    @override
    def log_message(self, format: Any, *args: Any) -> None:
        return

    # Please do not change this into lowercase!
    @override
    def do_GET(self) -> None:  # type: ignore # noqa: PLR0912
        self._set_response()

        parsed_url = urlparse(self.path)

        # Get query parameters as a dict
        query_params = parse_qs(parsed_url.query)

        # Example: Get the value of the "error" parameter if it exists
        error_value = query_params.get("error", [None])[0]
        path = self.path
        auth_code = path[1:]  # Remotive /
        time.sleep(1)
        httpd.server_close()

        killerthread = Thread(target=httpd.shutdown)
        killerthread.start()
        if error_value is None:
            res = Rest.handle_get(
                f"/api/open/token?code={auth_code}&code_verifier={code_verifier}",
                return_response=True,
                skip_access_token=True,
                allow_status_codes=[401, 400],
            )
            if res.status_code != 200:
                ErrorPrinter.print_generic_error(
                    "Failed to fetch token. Please try again, if the problem persists please reach out to support@remotivelabs.com"
                )
                self.wfile.write(
                    "Failed to fetch token. Please try again, if the problem persists please reach out to support@remotivelabs.com".encode(
                        "utf-8"
                    )
                )
                sys.exit(1)
            self.wfile.write("Successfully setup CLI, return to your terminal to continue".encode("utf-8"))
            access_token = res.json()["access_token"]
            # token = tf.TokenFile(
            #    name="CLI_login_token",
            #    token=access_token,
            #    created=str(datetime.datetime.now().isoformat()),
            #    expires="unknown",
            # )

            global short_lived_token  # noqa: PLW0603
            short_lived_token = access_token

            # settings.add_and_activate_short_lived_cli_token(tf.dumps(token))
            # print("Successfully logged on, you are ready to go with cli")
        else:
            if error_value == "no_consent":
                self.wfile.write(
                    """
                Authorization was cancelled.<br/>
                To use RemotiveCLI, you need to grant access to your RemotiveCloud account.
                <br/><br/>
                Run `remotive cloud auth login` to try again.
                """.encode("utf-8")
                )
                ErrorPrinter.print_generic_error("You did not grant access to RemotiveCloud, login aborted")
            else:
                self.wfile.write(f"Unknown error {error_value}, please contact support@remotivelabs.com".encode("utf-8"))
                ErrorPrinter.print_generic_error(f"Unexpected error {error_value}, please contact support@remotivelabs.com")
            sys.exit(1)


def prepare_local_webserver(server_class: type = HTTPServer, handler_class: type = S, port: Optional[int] = None) -> None:
    if port is None:
        env_val = os.getenv("REMOTIVE_LOGIN_CALLBACK_PORT" or "")
        if env_val and env_val.isdigit():
            port = int(env_val)
        else:
            port = 0

    server_address = ("", port)
    global httpd  # noqa: PLW0603
    httpd = server_class(server_address, handler_class)


def create_personal_token() -> None:
    response = Rest.handle_post(
        url="/api/me/keys",
        return_response=True,
        body=json.dumps({"alias": "roine"}),
        access_token=short_lived_token,
    )
    token = response.json()
    email = token["account"]["email"]
    existing_file = settings.get_token_file_by_email(email=email)
    if existing_file is not None:
        # ErrorPrinter.print_hint(f"Revoking and deleting existing credentials [remove_me]{existing_file.name}")
        res = Rest.handle_patch(
            f"/api/me/keys/{existing_file.name}/revoke",
            quiet=True,
            access_token=short_lived_token,
            allow_status_codes=[400, 404],
        )
        if res is not None and res.status_code == 200:
            Rest.handle_delete(
                f"/api/me/keys/{existing_file.name}",
                quiet=True,
                access_token=short_lived_token,
            )
        settings.remove_token_file(existing_file.name)

    settings.add_personal_token(response.text, activate=True)

    print("Successfully logged on")


def login(headless: bool = False) -> bool:  # noqa: C901, PLR0912, PLR0915
    """
    Initiate login
    """

    #
    # Check login.md flowchart for better understanding
    #
    # 1. Check for active token valid and working credentials
    #
    try:
        activate_token = settings.get_active_token_file()

        if not activate_token.is_expired():
            if Rest.has_access("/api/whoami"):
                console.print(f"You are already signed in with valid credentials that expires in {activate_token.expires_in_days()} days")
                files = settings.list_personal_token_files()
                if len(files) > 0:
                    print("")
                    console.print("You have available credentials on disk, [bold]choose one or press q to login again[/bold]")
                    token_selected = list_and_select_personal_token(skip_prompt=False)
                    if token_selected:
                        return True
                # list_and_select_personal_token(skip_prompt=True)
                # print("")
                # typer.confirm("Are you sure you want to login again?", abort=True)
                # If we are here, user still wants to login
            else:
                settings.clear_active_token()
                raise TokenNotFoundError()
        else:
            # TODO - Cleanup token since expired
            pass

    except TokenNotFoundError:
        #
        # 2. If no token was found, let user choose an existing if exists
        #
        files = settings.list_personal_token_files()
        if len(files) > 0:
            print("")
            token_selected = list_and_select_personal_token(
                skip_prompt=False,
                info_message="You have available credentials on disk, choose one or press q to login again",
            )
            if token_selected:
                return True

    prepare_local_webserver()

    def force_use_webserver_callback() -> bool:
        env_val = os.getenv("REMOTIVE_LOGIN_FORCE_CALLBACK" or "no")
        if env_val and env_val == "yes":
            return True
        return False

    def login_with_callback_but_copy_url() -> None:
        """
        This will print a url the will trigger a callback later so the webserver must be up and running.
        """
        print("Copy the following link in a browser to login to cloud, and complete the sign-in prompts:")
        print("")

        url = (
            f"{Rest.get_base_frontend_url()}/login"
            f"?state={state}"
            f"&cli_version={Rest.get_cli_version()}"
            f"&response_type=code"
            f"&code_challenge={code_challenge}"
            f"&redirect_uri=http://localhost:{httpd.server_address[1]}"
        )
        console.print(url, style="bold")
        httpd.serve_forever()

    def login_headless() -> None:
        """
        Full headless, opens a browser and expects a auth code to be entered and exchanged for the token
        """
        print("Copy the following link in a browser to login to cloud, and complete the sign-in prompts:")
        print("")

        url = (
            f"{Rest.get_base_frontend_url()}/login"
            f"?state={state}"
            f"&cli_version={Rest.get_cli_version()}"
            f"&response_type=code"
            f"&code_challenge={code_challenge}"
        )
        console.print(url, style="bold")

        code = typer.prompt(
            "Once finished, enter the verification code provided in your browser",
            hide_input=False,
        )
        res = Rest.handle_get(
            f"/api/open/token?code={code}&code_verifier={code_verifier}",
            return_response=True,
            skip_access_token=True,
            allow_status_codes=[401],
        )
        if res.status_code == 401:
            ErrorPrinter.print_generic_error(
                "Failed to fetch token. Please try again, if the problem persists please reach out to support@remotivelabs.com"
            )
            sys.exit(1)
        access_token = res.json()["access_token"]
        # res = Rest.handle_get("/api/whoami", return_response=True, access_token=access_token)
        global short_lived_token  # noqa: PLW0603
        short_lived_token = access_token
        create_personal_token()
        # current_user = res.json()
        # token = tf.TokenFile(
        #    type="authorized_user",
        #    name="CLI_login_token",
        #    token=access_token,
        #    created=str(datetime.datetime.now().isoformat()),
        #    expires="unknown",
        #    account=TokenFileUser(email=current_user["email"], uid=current_user["uid"], project=None),
        # )
        # settings.add_and_activate_short_lived_cli_token(tf.dumps(token))
        # console.print("Successfully logged on, you are ready to go with cli", style="green bold")

    if headless and not force_use_webserver_callback():
        login_headless()
    elif headless and force_use_webserver_callback():
        login_with_callback_but_copy_url()
    else:
        could_open = webbrowser.open_new_tab(
            f"{Rest.get_base_frontend_url()}/login"
            f"?state={state}"
            f"&cli_version={Rest.get_cli_version()}"
            f"&response_type=code"
            f"&code_challenge={code_challenge}"
            f"&redirect_uri=http://localhost:{httpd.server_address[1]}"
        )

        if not could_open:
            print(
                "Could not open a browser on this machine, this is likely because you are in an environment where no browser is avaialble"
            )
            print("")
            if force_use_webserver_callback():
                login_with_callback_but_copy_url()
            else:
                login_headless()
        else:
            httpd.serve_forever()

        # Once we received our callback or code we are logged in and ready to go
        create_personal_token()

    return True
