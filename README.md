# PhageProtEmbeddings
Code to use gLM (https://github.com/y-hwang/gLM) to generate context-aware embeddings of phage proteins. Work in progress. 

## generate order file 

Run the command 
```angular2html
python genbank_extract.py test_data/test_phage.gbk -p out -m 30 --window -f
```
the `-m` flag specifies the maximum number of genes per line. Default 30. <br> 
the `--window` flag specifies to run the script in window mode where each contig/phage with greater than the maximum number of genes is repeated with a window of length m. <br>
the   `-f` flag will also generate a fasta file of the amino acid sequences in the genbank file <br>
out.tsv will map the gene orders as outlined by gLM
