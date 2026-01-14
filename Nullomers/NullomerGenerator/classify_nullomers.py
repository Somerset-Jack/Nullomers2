import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots_adjust
import pandas as pd
import numpy as np

def compare_genome_nullomers(nullomers, distinct):
    classified_nullomers = {}
    core_nullomers = []
    softcore_nullomers = []
    shell_nullomers = []
    cloud_nullomers = []

    for nullomer in distinct:
        count = 0
        for genomes, list_nullomers in nullomers.items():
            if nullomer in list_nullomers:
                count = count + 1
        if count == 69:
            core_nullomers.append(nullomer)
        if 62 < count < 69:
            softcore_nullomers.append(nullomer)
        if 7 < count < 63:
            shell_nullomers.append(nullomer)
        if count < 8:
            cloud_nullomers.append(nullomer)

    print("Core Nullomers: " + str(len(core_nullomers)))
    print("Softcore Nullomers: " + str(len(softcore_nullomers)))
    print("Shell Nullomerrs: " + str(len(shell_nullomers)))
    print("Cloud Nullomers: " + str(len(cloud_nullomers)))

    classified_nullomers.update({"Core Nullomers":core_nullomers})
    classified_nullomers.update({"Softcore Nullomers":softcore_nullomers})
    classified_nullomers.update({"Shell Nullomers":shell_nullomers})
    classified_nullomers.update({"Cloud Nullomers":cloud_nullomers})

    return classified_nullomers


def nullomers_to_dict(path):

    nullomer_file = open(path)
    nullomers = set([])
    for line in nullomer_file:
        if not line.startswith(">"):
            nullomer = line.strip()
            nullomers.add(nullomer)
    return nullomers
    #print(nullomer_dict)

def distinct_nullomers_to_list(path):
    distinct_nullomers = []
    nullomer_file = open(path)
    for line in nullomer_file:
        if not line.startswith(">"):
            nullomer = line.strip()
            distinct_nullomers.append(nullomer)
    return distinct_nullomers

def classes_to_fasta(classed):
    core_nullomers = classed.pop("Core Nullomers")
    softcore_nullomers = classed.pop("Softcore Nullomers")
    shell_nullomers = classed.pop("Shell Nullomers")
    cloud_nullomers = classed.pop("Cloud Nullomers")

    c = open("core_nullomers.fa", "w")
    for nullomer in core_nullomers:
        c.write(">" + '\n')
        c.write(nullomer + '\n')
    c.close()

    f = open("softcore_nullomers.fa", "w")
    for nullomer in softcore_nullomers:
        f.write(">" + '\n')
        f.write(nullomer + '\n')
    f.close()

    s = open("shell_nullomers.fa", "w")
    for nullomer in shell_nullomers:
        s.write(">" + '\n')
        s.write(nullomer + '\n')
    s.close()

    l = open("cloud_nullomers.fa", "w")
    for nullomer in cloud_nullomers:
        l.write(">" + '\n')
        l.write(nullomer + '\n')

if __name__ == "__main__":
    path_to_dir = "/home/jmb28/MPhil/Genomes/69Genomes/Pan_Genome_69_Arabidopsis/ncbi_dataset/data/69_Genomes/10_Nullomers/"
    path_to_dist_nulls = "/home/jmb28/MPhil/Genomes/69Genomes/Pan_Genome_69_Arabidopsis/ncbi_dataset/data/69_Genomes/PanNullomers/PanNullomers10.fa"

    #all_nullomers = {}
    #for root, dirs, files in os.walk(path_to_dir):
    #    for file in files:
    #        if file.endswith(".txt"):
    #            genome_id = (file.rsplit("_",3)[0])
                #print(genome_id)
    #            filepath = os.path.join(root, file)
    #            nullomers = nullomers_to_dict(filepath)
    #            all_nullomers.update({genome_id: nullomers})

    #distinct = distinct_nullomers_to_list(path_to_dist_nulls)
    #classified = compare_genome_nullomers(all_nullomers, distinct)
    #calculate_cpg(classified)
    #classes_to_fasta(classified)
    di_to_chart()