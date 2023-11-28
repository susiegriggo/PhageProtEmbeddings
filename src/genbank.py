"""
Handle genbank file

Code snippets copied from Phynteny https://github.com/susiegriggo/Phynteny
"""

# imports
from Bio import SeqIO
from loguru import logger
import binascii

def get_genbank(genbank):
    """
    Convert genbank file to a dictionary

    param genbank: path to genbank file
    return: genbank file as a dictionary
    """

    # if genbank.strip()[-3:] == ".gz":
    if is_gzip_file(genbank.strip()):
        try:
            with gzip.open(genbank.strip(), "rt") as handle:
                gb_dict = SeqIO.to_dict(SeqIO.parse(handle, "gb"))
            handle.close()
        except ValueError:
            logger.error(genbank.strip() + " is not a genbank file!")
            raise

    else:
        try:
            with open(genbank.strip(), "rt") as handle:
                gb_dict = SeqIO.to_dict(SeqIO.parse(handle, "gb"))
            handle.close()
        except ValueError:
            logger.error(genbank.strip() + " is not a genbank file!")
            raise

    return gb_dict


def extract_order(gb_dict, prefix, max=30, window=False):
    """
    Method to generate protein orders in the genbank file
    :param gb_dict: genbank file as dictionary
    :param prefix: prefix for output files
    :param max: maximum window size
    :param window: whether to generate windows of order
    """
    # get the phages
    phages = list(gb_dict.keys())

    # open file to write
    with open(prefix + '.tsv', 'w') as f:

        for p in phages:

            # get info
            name = gb_dict.get(p).name
            proteins = [i for i in gb_dict.get(p).features if i.type == 'CDS']
            protein_ids = [r.qualifiers.get('protein_id') for r in proteins]
            protein_ids = ['None' if i == None else i[0] for i in protein_ids]
            orientation = [str(p.location)[-2] for p in proteins]

            if window and len(protein_ids) >= max:

                # write to a text file
                line_num = 0

                # loop through proteins
                for i in range(len(protein_ids) - max):

                    # write header
                    f.write(name + '_' + str(line_num) + '\t')

                    # write each protein
                    for j in range(max):
                        f.write(orientation[i + j] + protein_ids[i + j])

                        if j < (max - 1):
                            f.write(';')

                    # prepare for next window
                    else:
                        line_num += 1
                        f.write('\n')


            else:

                # add counter variable before split needs to occur
                split_count = 0
                line_num = 0

                for i, id in enumerate(protein_ids):

                    # check if 30 proteins have already been written
                    if split_count % (max) == 0:
                        f.write('\n' + name + '_' + str(line_num) + '\t')
                        line_num += 1

                    else:
                        f.write(';')

                    # write the proteins to file
                    f.write(orientation[i] + id)
                    split_count += 1

    f.close()

def protein_fasta(gb_dict, prefix):
    """
    Generate a fasta file with the proteins in the genbank file
    :param gb_dict: genbank file as dictionary
    :param prefix: prefix for output files
    :return:
    """

    # get the phages
    phages = list(gb_dict.keys())

    with open(prefix + '.faa', 'w') as f:

        # loop through the phages
        for p in phages:

            # fetch details
            proteins = [i for i in gb_dict.get(p).features if i.type == 'CDS']
            protein_ids = [r.qualifiers.get('protein_id') for r in proteins]
            protein_ids = ['None' if i == None else i[0] for i in protein_ids]
            protein_seqs = [r.qualifiers.get('translation')[0] for r in proteins]

        # write to file
        for i in range(len(proteins)):
            f.write(">" + protein_ids[i] + "\n" + protein_seqs[i] + "\n")

    f.close()

def is_gzip_file(f):
    """
    Method copied from Phispy see https://github.com/linsalrob/PhiSpy/blob/master/PhiSpyModules/helper_functions.py

    This is an elegant solution to test whether a file is gzipped by reading the first two characters.

    See https://stackoverflow.com/questions/3703276/how-to-tell-if-a-file-is-gzip-compressed for inspiration
    :param f: the file to test
    :return: True if the file is gzip compressed else false
    """
    with open(f, "rb") as i:
        return binascii.hexlify(i.read(2)) == b"1f8b"

