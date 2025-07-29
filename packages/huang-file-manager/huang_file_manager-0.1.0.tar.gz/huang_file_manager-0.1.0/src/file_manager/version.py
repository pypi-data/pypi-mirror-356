import typer

app = typer.Typer(help="showing the version")


@app.command()
def version():
    print("My CLI Version 1.0")
