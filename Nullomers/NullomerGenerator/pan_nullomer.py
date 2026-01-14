import os


def distinct_nullomers(directory):
    unique_nullo = file_by_file(directory)
    all_nullomers_to_fasta(unique_nullo)


def file_by_file(path):
    unique_nullomers = {}
    core_nullomers= set()
    for file in os.listdir(path):
        if file.endswith("nullomers.txt"):
            print("Loading file in: " + file)
            infile = open(file)
            for line in infile:
                nullomer = line.strip()
                if nullomer not in unique_nullomers:
                    unique_nullomers[nullomer] = 1
                else:
                    count = unique_nullomers[nullomer]
                    new_count = count + 1
                    unique_nullomers[nullomer] = new_count
    print("Number of Unique Nullomers: " + str(len(unique_nullomers)))
    for nullomer in unique_nullomers.keys():
        count = unique_nullomers.get(nullomer)
        if count == 69:
            core_nullomers.add(nullomer)
            print("Nullomer " + nullomer + "appears ")
            print(str(unique_nullomers[nullomer]) + " times")
    #print(len(core_nullomers))
    return unique_nullomers


def all_nullomers_to_fasta(all_nullomers):
    f = open("PanNullomers11.fa", "w")
    for nullomer, v in all_nullomers.items():
        f.write(">" + str(v) + '\n')
        f.write(nullomer + '\n')
    f.close()