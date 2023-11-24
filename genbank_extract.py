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

def main(infile, out):

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

            # write to text file
            f.write(name + '\t')
            for i, id in enumerate(protein_ids):
                f.write(orientation[i] + id +';' )
            f.write('\n')

    f.close()

if __name__ == "__main__":
    main()




