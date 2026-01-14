import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots_adjust
import pandas as pd
import numpy as np


def classify_nullomers(path_to_nullomers, distinct_nullomers):

    all_nullomers = {}
    for root, dirs, files in os.walk(path_to_nullomers):
        for file in files:
            if file.endswith(".txt"):
                genome_id = (file.rsplit("_",3)[0])
                print(genome_id)
                filepath = os.path.join(root, file)
                nullomers = nullomers_to_dict(filepath)
                all_nullomers.update({genome_id: nullomers})
    distinct = distinct_nullomers_to_list(distinct_nullomers)
    classified = compare_genome_nullomers(all_nullomers, distinct)
    classes_to_fasta(classified)

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

def distinct_nullomers_to_list(distinct_nullomers):
    distinct_nullomers_list = []
    for nullomer in distinct_nullomers.keys():
        distinct_nullomers_list.append(nullomer)
    return distinct_nullomers_list

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