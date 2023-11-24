"""
Script to extract gene orders from genbank file

TODO: add code to also generate a fasta file with the proteins
"""

__author__ = "Susanna Grigson"
__maintainer__ = "Susanna Grigson"
__license__ = "MIT"
__version__ = "0"
__email__ = "susie.grigson@gmail.com"
__status__ = "development"

# imports
from src import genbank
import click
import sys

@click.command()
@click.argument("infile", type=click.Path(exists=True))
@click.option(
    "-o",
    "--out",
    type=click.STRING,
    default="",
    help="output file",
)
@click.option(
    "-w",
    "--window",
    is_flag=True,
)
@click.option(
    "-m",
    "--max",
    default=30,
    show_default=True,
    help="maximum number of proteins included on each line or 'contig'"
)


def main(infile, out, max, window):

    # fetch the genbank file
    gb_dict = genbank.get_genbank(infile)
    if not gb_dict:
            click.echo('Error: no sequences found in genbank file')
            sys.exit()

    # extract the relevant info
    phages = list(gb_dict.keys())


    # open file to write
    with open(out, 'w') as f:

        for p in phages:

            # get info
            name = gb_dict.get(p).name
            proteins = [i for i in gb_dict.get(p).features if i.type == 'CDS']
            protein_ids = [p.qualifiers.get('protein_id') for p in proteins]
            protein_ids = ['None' if i == None else i[0] for i in protein_ids]
            orientation = [str(p.location)[-2] for p in proteins]

            if window and len(protein_ids) >= max:

                # write to a text file
                line_num = 0

                # loop through proteins
                for i in range(len(protein_ids)-max):

                    # write header
                    f.write(name + '_' + str(line_num) + '\t')

                    # write each protein
                    for j in range(max):
                        f.write(orientation[i + j] + protein_ids[i+j])

                        if j < (max - 1):
                            f.write(';')

                    # prepare for next window
                    else:
                        line_num +=1
                        f.write('\n')


            else:

                # write to text file
                #f.write(name + '\t')

                # add counter variable before split needs to occur
                split_count = 0
                line_num = 0

                for i, id in enumerate(protein_ids):

                    # check if 30 proteins have already been written
                    if split_count % (max) == 0:
                        f.write(name + '_' + str(line_num) + '\t')
                        line_num += 1

                    else:
                        f.write(';')

                    # write the proteins to file
                    f.write(orientation[i] + id )
                    split_count += 1

                f.write('\n')

    f.close()

if __name__ == "__main__":
    main()




