import typer
from .version import app as version_app
from .NullomerGenerator import app as nullomer_generator_app
app = typer.Typer()

app.add_typer(version_app)
app.add_typer(nullomer_generator_app)

if __name__ == '__main__':
    app()