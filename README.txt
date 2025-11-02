# A simple utility to reproduce the CAFA6 contest labels

To run:
  - download [this raw data file](https://ftp.ebi.ac.uk/pub/databases/GO/goa/old/UNIPROT/goa_uniprot_all.gaf.226.gz) from the GOA ftp site and put it somewhere, e.g. /path/to/uniprot
  - download the CAFA6 train and test data from [Kaggle](https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/data) and it put it somewhere else, e.g. /path/to/cafa6
  - `docker build -t cafa6labels .`
  - `docker run -d --mount type=bind,source=/path/to/cafa6/,target=/cafa6  --mount type=bind,source=/path/to/uniprot/,target=/uniprot cafa6labels`

The docker container executes the sequence of commands in run_all.sh.  Running will generally take a few minutes, as the raw input data from GOA is about 20GB.  
The last step loads the official contest labels into memory, derives a set of labels from the GOA raw data (technically, a slimmed version of the raw data
made by the awk command in run_all.sh), and compares the two.  The labels derived from the GOA raw data are only stored in memory in this simple demo script; they are not written to disk.  
The expected output looks like this:


	len(contest)=537027; len(emulated)=537027
	precision=1.0
	recall=1.0
	f=1.0
	len(extras): 0; len(missing): 0

  
