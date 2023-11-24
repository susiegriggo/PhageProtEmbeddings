# PhageProtEmbeddings
Code to use gLM (https://github.com/y-hwang/gLM) to generate context-aware embeddings of phage proteins. Work in progress. 

## generate order file 

Run the command 
```angular2html
python genbank_extract.py test_data/test_phage.gbk -o out -m 30 --window
```
the `-m` flag specifies the maximum number of genes per line. Default 30. <br> 
the `--window` flag specifies to run the script in window mode where each contig/phage with greater than the maximum number of genes is repeated with a window of length m. <br>
out.tsv will map the gene orders as outlined by gLM

## TODO 
modify genbank_extract.py to also output a fasta file of the proteins in the genbank file so that embeddings can be generated from a fasta file 
