import pandas as pd
import re
import gzip
import pickle
import obonet

def load_labels(df):
  ls=set()
  for i in range(len(df)):
    acc=df.iloc[i]["EntryID"]
    go_id=df.iloc[i]["term"]
    ls.add((acc,go_id))
  return ls


def extract_tags_from_awkskim(filename,graph):
  #filename is something like "/uniprot/goa_uniprot_all.awkskim.tsv"
  #load graph in calling function using syntax like:
  #  graph=obonet.read_obo("/cafa6/Train/go-basic.obo")
  id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}

  experimental_codes=set(['EXP', 'IDA', 'IMP','IGI', 'HDA', 'HEP', 'HGI', 'HMP', 'HTP', 'IEP', 'IPI','TAS','IC'])

  tags=dict()
  with open(filename,"r") as f:
    for line in f:
      acc,qual,go_id,evcode=re.split("\t",line[:-1])
      if "NOT" in qual:
        continue
      if go_id not in id_to_name:
        continue

      if acc not in tags:
        tags[acc]=dict()
      if go_id not in tags[acc]:
        tags[acc][go_id]=set()
      tags[acc][go_id].add(evcode)


  exp_tags=dict()
  for accession in tags:
    for GO_ID in tags[accession]:
      good_codes = experimental_codes & tags[accession][GO_ID]

      if len(good_codes)==0:
        continue
      if accession not in exp_tags:
        exp_tags[accession]=dict()
      assert GO_ID not in exp_tags[accession]
      exp_tags[accession][GO_ID]=good_codes

  return exp_tags

def flatten_labels(tags):
  retval=set()
  for acc in tags:
    for go_id in tags[acc]:
      retval.add((acc,go_id))
  return retval


contest=load_labels(pd.read_csv("/cafa6/Train/train_terms.tsv",sep="\t"))
graph=obonet.read_obo("/cafa6/Train/go-basic.obo")
emulated=flatten_labels(extract_tags_from_awkskim("/uniprot/goa_uniprot_all.awkskim.tsv",graph))

print("len(contest)="+str(len(contest))+"; len(emulated)="+str(len(emulated)),flush=True)

inter=len(contest & emulated)
precision=inter/len(emulated)
recall=inter/len(contest)
f=2*precision*recall/(precision+recall)

print("precision="+str(precision),flush=True)
print("recall="+str(recall),flush=True)
print("f="+str(f),flush=True)


extras = emulated - contest
missing = contest - emulated

print("len(extras): "+str(len(extras))+"; len(missing): "+str(len(missing)),flush=True)

if len(extras)>0:
  print("a few extras:",flush=True)
  for ex in list(extras)[0:20]:
    print("  "+str(ex),flush=True)

if len(missing)>0:
  print("\n\na few missing: ",flush=True)
  for ex in list(missing)[0:20]:
    print("  "+str(ex),flush=True)
