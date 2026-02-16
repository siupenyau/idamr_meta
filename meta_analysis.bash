#!/bin/sh

python3 file_management_sampleID.py $1 $2 $3

#Changing the environment
conda activate nanofilt

#Starting the NanoFilt filtering
python3 nanofilt_linux_sampleID.py $2

conda activate base

#Starting kraken2

conda activate kraken2

python3 kraken2.py $2 $4

conda activate base

conda activate blastplus

export BLASTDB=$BLASTDB:$4/blast_db/

python3 AMR_ID.py $2 $4

python3 extract_AMR_seq.py $2

python3 blastn.py $2 $4

python3 combine_AMR_nt_result.py $2 $3

conda activate base

#Counting reads

conda activate seqkit

find "$2" -name "*_microbial.fastq" -exec seqkit stat {} \; > "$2/kraken2_results/non_human_fq/summary.txt"

find "$2" -name "*.fastq.gz" -exec seqkit stat {} \; > "$2/summary.txt"

conda activate base
