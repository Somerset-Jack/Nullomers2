from typing import Annotated
import typer
from pathlib import Path
app = typer.Typer()

@app.command()
def generate_nullomers(
        path_to_genome: Annotated[
            Path,
            typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            writable=False,
            resolve_path=True,
            readable=True,
        ),
    ],
        nullomer_length: Annotated[int, typer.Option(min=3, max=12)] = 10,
):
    print(f'Location of genomes: {path_to_genome}')
    print(f'Nullomer length chosen: {nullomer_length}')