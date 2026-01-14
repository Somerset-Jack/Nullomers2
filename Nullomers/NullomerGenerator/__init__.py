import typer

from .nullomer_controller import app as generate_nullomer_app
from .nullomer_statistics import app as generate_nullomer_statistics_app

app = typer.Typer()

app.add_typer(generate_nullomer_app)
app.add_typer(generate_nullomer_statistics_app)