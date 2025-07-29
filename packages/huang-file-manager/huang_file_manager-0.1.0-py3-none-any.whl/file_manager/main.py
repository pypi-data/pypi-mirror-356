import typer

from .users import app as users_app
from .version import app as version_app

app = typer.Typer(help="A simple CLI tool for managing users")

app.add_typer(version_app,help="Show the version of the tool")
app.add_typer(users_app, name="users",help="Manage users")


if __name__ == "__main__":
    app()
