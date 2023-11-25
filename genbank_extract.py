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
    "-p",
    "--prefix",
    type=click.STRING,
    default="",
    help="prefix for output files",
)
@click.option(
    "-w",
    "--window",
    is_flag=True,
    help='generate windows of length max'
)
@click.option(
    "-f",
    "--fasta",
    is_flag=True,
    help='include fasta of proteins'
)
@click.option(
    "-m",
    "--max",
    default=30,
    show_default=True,
    help="maximum number of proteins included on each line or 'contig'"
)


def main(infile, prefix, max, window, fasta):

    # fetch the genbank file
    gb_dict = genbank.get_genbank(infile)
    if not gb_dict:
            click.echo('Error: no sequences found in genbank file')
            sys.exit()

    # generate gene order file
    genbank.extract_order(gb_dict, prefix, max, window)

    # generate the fasta file
    if fasta:
        genbank.protein_fasta(gb_dict, prefix)

if __name__ == "__main__":
    main()




