import typer
import requests
from typing import Annotated
from pathlib import Path
from rich import print # print with colors

client = typer.Typer()

BASE_URL = "http://127.0.0.1:8000/api"

@client.command()
def register(
        username: Annotated[str, typer.Option(prompt=True)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):

    data = {
        "username": username,
        "password": password
    }

    r = requests.post(f"{BASE_URL}/register", data=data)
    content = r.content

    if r.status_code == 200:
        path = Path(".")
        with open(path / f"{username}.p12", "wb") as f:
            f.write(content)
        print("[bold green]Successfully registered![/bold green] [bold red]Keep your certificate .p12[/bold red]")
    else:
        print(r.json())
        print("[bold red]Something went wrong please try again.[/bold red]")
        raise typer.Exit()
        
@client.command()
def login(
        username: Annotated[str, typer.Option(prompt=True)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):

    data = {
        "username": username,
        "password": password
    }

    r = requests.post(f"{BASE_URL}/login", data=data)
    content = r.json()
    token = content['access_token']

    if r.status_code == 200:
        path = Path(".")
        with open(path / f"{username}.token", "w", encoding='utf-8') as f:
            f.write(token)
        print("[bold green]Successfully signed in![/bold green] 15-minutes session started!")
    else:
        print("[bold red]Something went wrong please try again.[/bold red]")
        raise typer.Exit()

def validate_token(token_path: Path, username: str):

    if not token_path.is_file():
        print(f"[bold red]Error: Inactive session for {username}. Please try again.[/bold red]")
        raise typer.Exit()

    with open(token_path, "r") as f:
        token = f.read()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return headers

@client.command() # File must be in working directory
def upload(filename: str, username: str, token_path: Path | None = None):
    try:
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
    except Exception as e:
        print(f"[bold red]{e}[/bold red]")

@client.command()
def sign(filename: str, username: str | None = None, token_path: Path | None = None):

    headers = validate_token(token_path=token_path, username=username)
    files = {"file": open(filename, "rb")}
    data = {"password": password}

    r = requests.post(f"{BASE_URL}/sign", headers=headers, files=files, stream=True, data=data)
    with open(Path(".") / f"{filename}_signed.pdf", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

# @client.command()
# def download(filename: str):
#
# @client.command()
# def verify(filename: str = typer.Argument()):
#     pass


if __name__ == "__main__":
    client()
