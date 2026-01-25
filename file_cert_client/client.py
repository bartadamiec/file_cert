import typer
import requests
from typing import Annotated
from pathlib import Path
from rich import print # print with colors
from jose import JWTError
client = typer.Typer()

BASE_URL = "http://127.0.0.1:8000/api"

@client.command()
def register(
        username: Annotated[str, typer.Option(prompt=True)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):
    """
    Registering a new user and downloading the generated PKCS#12 certificate.

    :param username: Username for the new account
    :param password: Password for account creation and certificate encryption
    :raise typer.Exit: If registration fails or server is unreachable
    :return: None
    """

    data = {
        "username": username,
        "password": password
    }

    try:
        r = requests.post(f"{BASE_URL}/register", data=data)
        content = r.content

        if r.status_code == 200:
            path = Path("")
            with open(path / f"{username}.p12", "wb") as f:
                f.write(content)
            print("[bold green]Successfully registered![/bold green] [bold red]Keep your certificate .p12[/bold red]")
        else:
            print(f"[bold red]{r.json()["detail"]}[/bold red]")
            raise typer.Exit()

    except Exception:
        print(f"[bold red]Server Error[/bold red]")
        raise typer.Exit()

@client.command()
def login(
        username: Annotated[str, typer.Option(prompt=True)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):
    """
    Authenticating user against the server and saving the session token.

    :param username: Username for authentication
    :param password: User's password
    :raise typer.Exit: If authentication fails or server is unreachable
    :return: None
    """

    data = {
        "username": username,
        "password": password
    }
    try:
        r = requests.post(f"{BASE_URL}/login", data=data)
        content = r.json()
        token = content['access_token']
        if r.status_code == 200:
            path = Path("")

            with open(path / f"{username}.token", "w", encoding='utf-8') as f:
                f.write(token)

            with open(path / "last_user.txt", "w", encoding='utf-8') as f:
                f.write(username)

                print("[bold green]Successfully signed in![/bold green] 15-minutes session started!")

        else:
            print(f"[bold red]{r.json()["detail"]}[/bold red]")
            raise typer.Exit()

    except Exception:
        print(f"[bold red]Server Error[/bold red]")
        raise typer.Exit()

def validate_token(token_path: Path, username: str):
    """
    Validating local session token and preparing authentication headers.

    :param token_path: Path to the file storing the access token
    :param username: Username for which the session is validated
    :raise typer.Exit: If the token file does not exist (inactive session)
    :return: Dictionary containing the Authorization header
    """

    if not token_path.is_file():
        print(f"[bold red]Error: Inactive session for {username}. Please try again.[/bold red]")
        raise typer.Exit()

    with open(token_path, "r") as f:
        token = f.read().strip()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return headers

@client.command() # File must be in working directory
def upload(
        filename: Annotated[str, typer.Option(prompt=True)],
        username: str | None = None,
        token_path: Path | None = None):
    """
    Uploading a PDF file to the server for processing.

    :param filename: Name of the PDF file to be uploaded (must exist locally)
    :param username: Username of the uploader (optional)
    :param token_path: Path to the authentication token file (optional)
    :raise typer.Exit: If the session is inactive or file does not exist
    :return: None
    """

    try:
        try:
            with open(Path("last_user.txt"), "r", encoding="utf-8") as f:
                username = f.read()

            if token_path == None:
                token_path = Path(f"./{username}.token")

            headers = validate_token(token_path=token_path, username=username)

            with open(filename, "rb") as f:
                files = {"file": (filename, f, "application/pdf")}
                r = requests.post(f"{BASE_URL}/upload", headers=headers, files=files)

            if r.status_code == 200:
                print("[bold green]File uploaded successfully[/bold green]")

            else:
                print(f"[bold red]Error {r.status_code}[/bold red]")
                typer.Exit()
        except FileNotFoundError:
            print(f"[bold red]{filename} not found in current working directory.[/bold red]")
    except JWTError:
        print(f"[bold red]ERROR 401: Inactive session[/bold red]")
        raise typer.Exit()

@client.command()
def sign(
        filename: Annotated[str, typer.Option(prompt=True)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
        username: str | None = None,
        token_path: Path | None = None):
    """
    Requesting server to digitally sign a PDF document using user's certificate.

    :param filename: Name of the PDF file to sign
    :param password: Password to unlock user's private key container PKCS#12
    :param username: Username of the signer (optional)
    :param token_path: Path to the authentication token file (optional)
    :raise typer.Exit: If the session is inactive or server error occurs
    :return: None
    """

    try:
        with open(Path("last_user.txt"), "r", encoding="utf-8") as f:
            username = f.read()
        token_path = Path(f"./{username}.token")
        headers = validate_token(token_path=token_path, username=username)

        json = {
            "filename": filename,
            "password": password,
        }

        r = requests.post(f"{BASE_URL}/sign", headers=headers, stream=True, json=json)

        if r.status_code == 200:
            with open(Path("") / f"{filename[:-4]}_signed.pdf", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[bold green]Successfully signed[/bold green] {filename}")

        elif r.status_code == 401:
            raise JWTError

        else:
            print(f"[bold red]Error {r.status_code}[/bold red]")
            typer.Exit()

    except JWTError:
        print(f"[bold red]ERROR 401: Inactive session[/bold red]")
        raise typer.Exit()

@client.command()
def verify(
        filename: Annotated[str, typer.Option(prompt=True)],
        signer: Annotated[str, typer.Option(prompt=True)],
        token_path: Path | None = None):
    """
    Requesting server to verify file signature and downloading validation report.

    :param filename: Name of the file to verify
    :param signer: Common Name of the signer to verify
    :param token_path: Path to the authentication token file (optional)
    :raise typer.Exit: If the session is inactive or server error occurs
    :return: None
    """

    try:
        with open(Path("last_user.txt"), "r", encoding="utf-8") as f:
            username = f.read()
        token_path = Path(f"./{username}.token")
        headers = validate_token(token_path=token_path, username=username)

        json = {
            "filename": filename,
            "signer": signer
        }

        r = requests.post(f"{BASE_URL}/verify", headers=headers, json=json, stream=True)

        if r.status_code == 200:
            with open(Path("") / f"{filename[:-4]}_report.pdf", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"[bold green]Report successfully downloaded[/bold green] {filename}")

        elif r.status_code == 401:
            raise JWTError

        else:
            print(f"[bold red]Error {r.status_code}[/bold red]")
            typer.Exit()

    except JWTError:
        print(f"[bold red]ERROR 401: Inactive session[/bold red]")
        raise typer.Exit()

if __name__ == "__main__":
    client()