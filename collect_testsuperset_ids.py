from Bio import SeqIO
import pickle

f_out=open("/cafa6/testsuperset_ids.dat","wb")

test_ids=[]
fasta_sequences=SeqIO.parse(open("/cafa6/Test/testsuperset.fasta"),"fasta")
for i,fasta in enumerate(fasta_sequences):
  test_ids.append(fasta.id)
  f_out.write(fasta.id.encode('utf-8')+b"\n")

f_out.close()

with open("/cafa6/testsuperset_ids.pickle","wb") as f:
  pickle.dump(test_ids,f,-1)


