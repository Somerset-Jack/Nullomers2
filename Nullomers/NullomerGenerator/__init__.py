import typer

from .nullomer_controller import app as generate_nullomer_app
from .nullomer_statistics import app as generate_nullomer_statistics_app
from .random_pan_statistics import app as random_pan_statistics_app

app = typer.Typer()

app.add_typer(generate_nullomer_app)
app.add_typer(generate_nullomer_statistics_app)
app.add_typer(random_pan_statistics_app)