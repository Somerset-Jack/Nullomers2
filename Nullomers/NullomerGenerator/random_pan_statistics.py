import csv
import random
import shutil
from pathlib import Path
from typing import Annotated

import typer

from Nullomers.NullomerGenerator import classify_nullomers
from Nullomers.NullomerGenerator import pan_nullomer
from Nullomers.NullomerGenerator.nullomer_controller import file_finder

app = typer.Typer()

FASTA_EXTENSIONS = {".fa", ".fasta", ".fna"}


@app.command()
def random_pan_stats(
        path_to_genomes: Annotated[
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
        output_dir: Annotated[
            Path,
            typer.Option(
                "--output-dir",
                "-o",
                file_okay=False,
                dir_okay=True,
                resolve_path=True,
            ),
        ] = Path("random_pan_stats_output"),
        nullomer_length: Annotated[int, typer.Option(min=3, max=12)] = 10,
        repetitions: Annotated[int, typer.Option(min=1)] = 100,
        minimum_genomes: Annotated[int, typer.Option(min=1)] = 10,
        maximum_genomes: Annotated[int, typer.Option(min=1)] = 69,
        random_seed: Annotated[int | None, typer.Option()] = None,
        force_regenerate_nullomers: Annotated[
            bool,
            typer.Option("--force-regenerate-nullomers/--reuse-existing-nullomers"),
        ] = False,
        keep_replicate_nullomer_files: Annotated[
            bool,
            typer.Option("--keep-replicate-nullomer-files/--delete-replicate-nullomer-files"),
        ] = True,
        write_classification_fastas: Annotated[
            bool,
            typer.Option("--write-classification-fastas/--no-write-classification-fastas"),
        ] = False,
):
    """
    Randomly samples genomes from a pan-genome, classifies nullomers for each sample,
    and writes average core, softcore, shell, and cloud nullomer counts.

    Nullomers are generated once for the full input genome set. Each random replicate
    then classifies only the sampled genomes' nullomer files.
    """

    if random_seed is not None:
        random.seed(random_seed)

    output_dir.mkdir(parents=True, exist_ok=True)

    genome_files = find_genome_files(path_to_genomes)

    if len(genome_files) == 0:
        raise typer.BadParameter("No FASTA files were found in the genome directory.")

    if len(genome_files) < maximum_genomes:
        raise typer.BadParameter(
            f"maximum-genomes is {maximum_genomes}, but only {len(genome_files)} FASTA files were found."
        )

    if minimum_genomes > maximum_genomes:
        raise typer.BadParameter("minimum-genomes cannot be larger than maximum-genomes.")

    typer.echo(f"Found {len(genome_files)} genome files.")
    typer.echo(f"Output directory: {output_dir}")
    typer.echo(f"Nullomer length: {nullomer_length}")
    typer.echo(f"Repetitions per sample size: {repetitions}")
    typer.echo(f"Sample sizes: {minimum_genomes} to {maximum_genomes}")

    generated_nullomer_dir = path_to_genomes / f"{nullomer_length}_Nullomers"

    if force_regenerate_nullomers and generated_nullomer_dir.exists():
        typer.echo(f"Removing existing nullomer directory: {generated_nullomer_dir}")
        shutil.rmtree(generated_nullomer_dir)

    if not generated_nullomer_dir.exists():
        typer.echo("Generating nullomers for the full genome set.")
        file_finder(str(path_to_genomes), nullomer_length)
    else:
        typer.echo(f"Reusing existing nullomer directory: {generated_nullomer_dir}")

    check_expected_nullomer_files(genome_files, generated_nullomer_dir)

    all_results_path = output_dir / "all_random_pan_stats.csv"
    averages_path = output_dir / "average_random_pan_stats.csv"

    all_rows = []

    for sample_size in range(minimum_genomes, maximum_genomes + 1):
        typer.echo(f"Processing random samples of {sample_size} genomes.")

        sample_size_dir = output_dir / f"{sample_size}_genomes"
        sample_size_dir.mkdir(parents=True, exist_ok=True)

        size_rows = []

        for repetition in range(1, repetitions + 1):
            typer.echo(f"  Repetition {repetition} of {repetitions}")

            selected_genomes = random.sample(genome_files, sample_size)

            replicate_dir = sample_size_dir / f"replicate_{repetition:03d}"
            sampled_nullomer_dir = replicate_dir / "nullomers"
            classification_dir = replicate_dir / "classification"

            sampled_nullomer_dir.mkdir(parents=True, exist_ok=True)

            selected_nullomer_files = copy_selected_nullomer_files(
                selected_genomes,
                generated_nullomer_dir,
                sampled_nullomer_dir,
            )

            distinct_nullomers = pan_nullomer.file_by_file(sampled_nullomer_dir)

            fasta_output_dir = None
            if write_classification_fastas:
                fasta_output_dir = classification_dir

            classified = classify_nullomers.classify_nullomers(
                sampled_nullomer_dir,
                distinct_nullomers,
                output_dir=fasta_output_dir,
            )

            row = {
                "sample_size": sample_size,
                "repetition": repetition,
                "selected_genomes": ";".join([genome.name for genome in selected_genomes]),
                "selected_nullomer_files": ";".join([file.name for file in selected_nullomer_files]),
                "core_nullomers": len(classified["Core Nullomers"]),
                "softcore_nullomers": len(classified["Softcore Nullomers"]),
                "shell_nullomers": len(classified["Shell Nullomers"]),
                "cloud_nullomers": len(classified["Cloud Nullomers"]),
            }

            size_rows.append(row)
            all_rows.append(row)

            write_replicate_counts(replicate_dir, row)

            if not keep_replicate_nullomer_files:
                shutil.rmtree(sampled_nullomer_dir)

        write_sample_size_results(sample_size_dir, size_rows)
        write_all_results(all_results_path, all_rows)
        write_averages(averages_path, all_rows)

    typer.echo("Random pan-genome statistics complete.")
    typer.echo(f"All replicate results: {all_results_path}")
    typer.echo(f"Average results: {averages_path}")


def find_genome_files(path_to_genomes):
    genome_files = []

    for file in sorted(path_to_genomes.iterdir()):
        if file.is_file() and file.suffix.lower() in FASTA_EXTENSIONS:
            genome_files.append(file)

    return genome_files


def check_expected_nullomer_files(genome_files, generated_nullomer_dir):
    missing_files = []

    for genome_file in genome_files:
        nullomer_file = generated_nullomer_dir / f"{genome_file.stem}_nullomers.txt"

        if not nullomer_file.exists():
            missing_files.append(str(nullomer_file))

    if missing_files:
        missing_text = "\n".join(missing_files)
        raise FileNotFoundError(
            "Some expected nullomer files were not found:\n" + missing_text
        )


def copy_selected_nullomer_files(selected_genomes, generated_nullomer_dir, sampled_nullomer_dir):
    selected_nullomer_files = []

    for genome_file in selected_genomes:
        nullomer_file = generated_nullomer_dir / f"{genome_file.stem}_nullomers.txt"

        if not nullomer_file.exists():
            raise FileNotFoundError(
                f"Expected nullomer file was not found: {nullomer_file}"
            )

        destination = sampled_nullomer_dir / nullomer_file.name
        shutil.copy2(nullomer_file, destination)
        selected_nullomer_files.append(destination)

    return selected_nullomer_files


def write_replicate_counts(replicate_dir, row):
    replicate_dir.mkdir(parents=True, exist_ok=True)

    counts_path = replicate_dir / "classification_counts.csv"

    with open(counts_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)


def write_sample_size_results(sample_size_dir, rows):
    if not rows:
        return

    results_path = sample_size_dir / "replicate_results.csv"

    with open(results_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def write_all_results(path, rows):
    if not rows:
        return

    with open(path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def write_averages(path, rows):
    if not rows:
        return

    grouped_rows = {}

    for row in rows:
        sample_size = row["sample_size"]

        if sample_size not in grouped_rows:
            grouped_rows[sample_size] = []

        grouped_rows[sample_size].append(row)

    average_rows = []

    for sample_size, sample_rows in sorted(grouped_rows.items()):
        average_rows.append({
            "sample_size": sample_size,
            "repetitions": len(sample_rows),
            "average_core_nullomers": average_count(sample_rows, "core_nullomers"),
            "average_softcore_nullomers": average_count(sample_rows, "softcore_nullomers"),
            "average_shell_nullomers": average_count(sample_rows, "shell_nullomers"),
            "average_cloud_nullomers": average_count(sample_rows, "cloud_nullomers"),
        })

    with open(path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=average_rows[0].keys())
        writer.writeheader()
        writer.writerows(average_rows)


def average_count(rows, field):
    return sum(row[field] for row in rows) / len(rows)