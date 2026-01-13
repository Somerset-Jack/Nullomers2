import os


def run_jellyfish(filename, path, kmer_length):

    if not os.path.isdir(path + '/jellyfishfiles'):
        # Creates and runs the command to create a temporary directory that store the files output from jellyfish.
        make_cmd = ("mkdir " + path + "/jellyfishfiles")
        os.system(make_cmd)

    if not os.path.isdir(path + '/indexed_kmers'):
         # Creates and runs the command to create a temporary directory that stores the index kmers from jellyfish
        make_out = ("mkdir " + path + "/indexed_kmers")
        os.system(make_out)

    # Two string that are used so that Jellyfish knows where to get and store files while processing.
    jelly_out_path = (path + "/jellyfishfiles")
    kmers_out_path = (path + "/indexed_kmers/")

    # Command created to run Jellyfish count with the correct parameters as specified by the user.
    cmd = ("jellyfish count -m " + str(kmer_length) + " -s 135M -t 4 " + path + "/" + filename + " -o " + jelly_out_path + "/counts.jf")
    # print(cmd)
    os.system(cmd)
    print("K-mers Successfully Indexed")

    # Command created to run Jellyfish dump, and dump in the correct location.
    dump_cmd = ("jellyfish dump " + jelly_out_path + "/counts.jf > " + kmers_out_path + "dumps.fa" )
    os.system(dump_cmd)
    print("K-mers Successfully Dumped")

    # Returns the full filepath and name of where Jellyfish has output the FASTA file of present k-mers
    return kmers_out_path + "dumps.fa"


if __name__ == '__main__':
    run_jellyfish("test_files/Ignore/3MERTEST.fa", '/Nullomer Creation and Comparison/test_files', 3)
