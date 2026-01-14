import os
import pandas as pd


def dinucleotide_content(path):
    file_to_fasta(path)
    run_jellyfish(path)
    jelly_dump(path)
    combine_dinuc(path)


def file_to_fasta(filepath):
    for file in os.listdir(filepath):
        if file.endswith(".txt"):
            genome_id = "_".join(file.split("_", 2)[:2])
            infile = open(str(filepath) + "/" + file)
            seqs = []
            for line in infile:
                seqs.append(line.strip())
            f = open(genome_id + "_nullomers.fna", "w")
            for N in seqs:
                f.write(">" + '\n')
                f.write(N + '\n')
            f.close()


def run_jellyfish(path):
    for file in os.listdir(path):
        if file.endswith(".fna"):
            genome_id = "_".join(file.split("_", 2)[:2])
            jelly = ("jellyfish count -m 2 -s 135M -t 4 " + file + " -o " + genome_id + "_di_counts.jf")
            os.system(jelly)


def jelly_dump(path):
    for file in os.listdir(path):
        if file.endswith("di_counts.jf"):
            genome_id = "_".join(file.split("_", 2)[:2])
            jelly = ("jellyfish dump -c " + file + " > " + genome_id + "_di_dump.tsv")
            os.system(jelly)


def combine_dinuc(path):
    all_dinucleotides = {}
    for file in os.listdir(path):
        dinucleotides = {}
        if file.endswith("di_dump.tsv"):
            with open(file) as f:
                for line in f:
                    clean_line = line.strip()
                    (di, c) = clean_line.split(sep=" ")
                    dinucleotides[di] = c
            genome_id = "_".join(file.split("_", 2)[:2])
            all_dinucleotides[genome_id] = dinucleotides

    di_df = pd.DataFrame(all_dinucleotides)
    di_df.to_csv("Dinucleotide count.csv")