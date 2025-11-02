#!/bin/bash

python collect_testsuperset_ids.py
gunzip -c /uniprot/goa_uniprot_all.gaf.226.gz | awk -F'\t' 'BEGIN{OFS="\t"} NR==FNR{K[$1]=1; next} ($2 in K){print $2, $4, $5, $7}' /cafa6/testsuperset_ids.dat - > /uniprot/goa_uniprot_all.awkskim.tsv
python compare_label_sets.py


