from itertools import product
import os


def nullomer_generation(kmer_length, indexed_kmers, filename, path):
    # Calls the required functions within this file and provides the correct arguments.
    all_kmers = generate_all_kmers(kmer_length)
    present_kmers = jf_to_dict(indexed_kmers)
    nullomers = nullomer_generator(all_kmers, present_kmers)
    nullomers_to_file(filename, nullomers, path, kmer_length)
    print("Nullomers successfully generated")
    return nullomers


def generate_all_kmers(kmer_length):
    # Generates tuples containing each possible k-mer
    all_kmers = product('ATCG', repeat=kmer_length)
    all_kmer_dict = {}
    # Iterates through the tuples and stores the k-mers as keys in a dictionary
    for k in list(all_kmers):
        count = 0  # The count variable is used to break the tuple at the correct location for the k-mer length.
        kmer = ''
        while count < kmer_length:
            kmer += k[count]  # Accessing the tuple in this way allows for the k-mer to be then stored in the
            # dictionary without any commas or breaks.
            count = count + 1
        all_kmer_dict.update({kmer: 1})
    if not len(all_kmer_dict.keys()) == 4 ** kmer_length:
        raise RuntimeError("Generate all k-mers calculated incorrect")
    return all_kmer_dict


def jf_to_dict(filename):
    fasta_as_dict = {}

    # Opens the file generated from the Jellyfish dump command.
    infile = open(filename)
    for line in infile:
        # Iterates over each line in the file and stores each k-mer in a dictionary.
        if line.startswith('>'):
            occurances = line
        else:
            kmer = line.strip()
            fasta_as_dict[kmer] = 1
    return fasta_as_dict


def nullomer_generator(all_kmers, present_kmers):
    nullomer_dict = {}
    # Checks the set of present k-mers against the set of all possible k-mers, returns a dictionary of nullomers.
    for l in all_kmers:
        if l not in present_kmers:
            nullomer_dict[l] = 1
    return nullomer_dict


def nullomers_to_file(filename, nullomers, path, length):
    if not os.path.isdir(path + '/' + str(length) +'_Nullomers'):
        # Creates and runs the command to create a temporary directory that store the files output from jellyfish.
        make_cmd = ("mkdir " + path + '/' + str(length) +"_Nullomers")
        os.system(make_cmd)
    os.chdir(path + '/' + str(length) + "_Nullomers")
    fname = (filename.rsplit(".",1)[0] + "_nullomers.txt")
    f = open(fname, "w")
    for n in nullomers.keys():  # Iterates through the keys of the dictionary and writes them to a new line in the file
        f.write(n + '\n')
    f.close()


if __name__ == '__main__':
    jf_to_dict("/Nullomer Creation and Comparison/test_files/indexed_kmers/dumps.fa")