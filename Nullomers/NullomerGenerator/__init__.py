import typer

from .nullomer_controller import app as generate_nullomer_app

app = typer.Typer()

app.add_typer(generate_nullomer_app)