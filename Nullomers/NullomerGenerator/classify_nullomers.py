import os
from pathlib import Path

def classify_nullomers(path_to_nullomers, distinct_nullomers, output_dir=None):

    all_nullomers = {}

    for root, dirs, files in os.walk(path_to_nullomers):
        for file in files:
            if file.endswith(".txt"):
                genome_id = file.rsplit("_", 3)[0]
                filepath = os.path.join(root, file)
                nullomers = nullomers_to_dict(filepath)
                all_nullomers.update({genome_id: nullomers})

    distinct = distinct_nullomers_to_list(distinct_nullomers)
    classified = compare_genome_nullomers(all_nullomers, distinct)

    if output_dir is not None:
        classes_to_fasta(classified, output_dir)

    return classified

def compare_genome_nullomers(nullomers, distinct):
    classified_nullomers = {}
    core_nullomers = []
    softcore_nullomers = []
    shell_nullomers = []
    cloud_nullomers = []

    genome_count = len(nullomers)

    if genome_count == 0:
        raise ValueError("No nullomer files were found to classify.")

    for nullomer in distinct:
        count = 0

        for genomes, list_nullomers in nullomers.items():
            if nullomer in list_nullomers:
                count = count + 1

        proportion = count / genome_count

        if count == genome_count:
            core_nullomers.append(nullomer)
        elif proportion >= 0.90:
            softcore_nullomers.append(nullomer)
        elif proportion >= 0.10:
            shell_nullomers.append(nullomer)
        else:
            cloud_nullomers.append(nullomer)

    print("Genomes classified: " + str(genome_count))
    print("Core Nullomers: " + str(len(core_nullomers)))
    print("Softcore Nullomers: " + str(len(softcore_nullomers)))
    print("Shell Nullomers: " + str(len(shell_nullomers)))
    print("Cloud Nullomers: " + str(len(cloud_nullomers)))

    classified_nullomers.update({"Core Nullomers": core_nullomers})
    classified_nullomers.update({"Softcore Nullomers": softcore_nullomers})
    classified_nullomers.update({"Shell Nullomers": shell_nullomers})
    classified_nullomers.update({"Cloud Nullomers": cloud_nullomers})

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


def distinct_nullomers_to_list(nullomers_distinct):
    distinct_nullomers_list = []
    for nullomer in nullomers_distinct.keys():
        distinct_nullomers_list.append(nullomer)
    return distinct_nullomers_list


def classes_to_fasta(classed, output_dir="."):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    core_nullomers = classed["Core Nullomers"]
    softcore_nullomers = classed["Softcore Nullomers"]
    shell_nullomers = classed["Shell Nullomers"]
    cloud_nullomers = classed["Cloud Nullomers"]

    c = open(output_path / "core_nullomers.fa", "w")
    for nullomer in core_nullomers:
        c.write(">" + '\n')
        c.write(nullomer + '\n')
    c.close()

    f = open(output_path / "softcore_nullomers.fa", "w")
    for nullomer in softcore_nullomers:
        f.write(">" + '\n')
        f.write(nullomer + '\n')
    f.close()

    s = open(output_path / "shell_nullomers.fa", "w")
    for nullomer in shell_nullomers:
        s.write(">" + '\n')
        s.write(nullomer + '\n')
    s.close()

    l = open(output_path / "cloud_nullomers.fa", "w")
    for nullomer in cloud_nullomers:
        l.write(">" + '\n')
        l.write(nullomer + '\n')
    l.close()