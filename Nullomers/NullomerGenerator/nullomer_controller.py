import argparse
import os
import typer
from typing import Annotated
from pathlib import Path
from Nullomers.NullomerGenerator import generate_nullomers
from Nullomers.NullomerGenerator import index_kmers

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

    file_finder(str(path_to_genome), nullomer_length)

def file_finder(path, length):
    directory = path
    no_of_file = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    print("Number of files found in directory: " + str(no_of_file))
    # Iterates over each file in the selected directory and passes this information to the controller.
    for filename in os.listdir(path):
        # Checking if the file is of FASTA format.
        if filename.endswith(".fa"):
            print(filename + " Is now being processed")
            controller(filename, directory, length)
        elif filename.endswith(".fasta"):
            print(filename + " Is now being processed")
            controller(filename, directory, length)
        elif filename.endswith(".fna"):
            print(filename + " Is now being processed")
            controller(filename, directory, length)
        else: print(filename + " Is not a FASTA file and will not be processed")


def controller(filename, path, length):
    # Calls the correct functions and send the correct the arguments.
    indexed_kmers = index_kmers.run_jellyfish(filename, path, length)
    nullomers = generate_nullomers.nullomer_generation(length, indexed_kmers, filename, path)


#if __name__ == '__main__':



#    parser = argparse.ArgumentParser()
#    parser.add_argument("kmer_length", type=int)
#    parser.add_argument("path")
#    args = parser.parse_args()

#    kmer_length = args.kmer_length
#    filepath = args.path

#    file_finder(filepath, kmer_length)

