# PhageProtEmbeddings
Code to use gLM (https://github.com/y-hwang/gLM) to generate context-aware embeddings of phage proteins. Work in progress. 

## generate order file 

Run the command 
```angular2html
 python genbank_extract.py test_data/test_phage.gbk -o out.tsv
```
out.tsv will map the gene orders as outlined by gLM 

(possibly slight issues in formatting)


## TODO 
modify genbank_extract.py to also output a fasta file of the proteins in the genbank file so that embeddings can be generated from a fasta file 
