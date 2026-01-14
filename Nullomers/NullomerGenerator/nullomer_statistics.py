import typer
from typing import Annotated, Literal
from pathlib import Path
from Nullomers.NullomerGenerator import pan_nullomer
from Nullomers.NullomerGenerator import classify_nullomers

app = typer.Typer()


@app.command()
def nullomer_stats(
        path_to_nullomers: Annotated[
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
        stats: Annotated[Literal["classify", "dinucleotide", "all"], typer.Option()] = "all",
):
    print("Location of nullomers: ", path_to_nullomers)
    print("Statistics chosen: ", stats)
    if stats == "classify":
        nullomer_classification(path_to_nullomers)
    elif stats == "dinucleotide":
        dinucleotide_content(path_to_nullomers)
    elif stats == "all":
        nullomer_classification(path_to_nullomers)
        dinucleotide_content(path_to_nullomers)


def nullomer_classification(path_to_nullomers: Path):
    distinct_nullomers = pan_nullomer.distinct_nullomers(path_to_nullomers)
    classified_nullomers = classify_nullomers.classify_nullomers(path_to_nullomers, distinct_nullomers)

def dinucleotide_content(path_to_nullomers: Path):
    do_something = 2