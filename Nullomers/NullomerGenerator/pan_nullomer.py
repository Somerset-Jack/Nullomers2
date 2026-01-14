import os


def distinct_nullomers(directory):
    unique_nullo = file_by_file(directory)
    all_nullomers_to_fasta(unique_nullo)


def file_by_file(path):
    unique_nullomers = {}
    for file in os.listdir(path):
        if file.endswith("nullomers.txt"):
            infile = open(str(path) + "/" + file)
            for line in infile:
                nullomer = line.strip()
                if nullomer not in unique_nullomers:
                    unique_nullomers[nullomer] = 1
                else:
                    count = unique_nullomers[nullomer]
                    new_count = count + 1
                    unique_nullomers[nullomer] = new_count
    print("Number of Unique Nullomers: " + str(len(unique_nullomers)))
    return unique_nullomers


def all_nullomers_to_fasta(all_nullomers):
    f = open("distinct_nullomers", "w")
    for nullomer, v in all_nullomers.items():
        f.write(">" + str(v) + '\n')
        f.write(nullomer + '\n')
    f.close()