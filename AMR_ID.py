import os, subprocess, glob, shutil, sys
import pandas as pd

print('Starting the BLAST_amr analysis. Please wait.')

#Checking the sequencing alignment FASTQ files in folder
inputdir=sys.argv[1]
amrdb=sys.argv[2]+str('/amr_db/')
currentdir=os.getcwd()
fastqFile = glob.glob(str(inputdir) + '/kraken2_results/non_human_fq/*_microbial.fastq')
TotalfastqFile = sum('.fastq' in f for f in fastqFile)
print('The total number of sequencing fastq files in folder is: ' + str(TotalfastqFile))
fastqfiledictionary = dict(enumerate(fastqFile, 1)) #Setting a dictionary for the fastq files in folder

if not os.path.exists(str(inputdir) + '/AMR_results/AMR/'):
	os.makedirs(str(inputdir) + '/AMR_results/AMR/')

#Converting the FASTQ files to the FASTA files.
def FASTQtoFASTA():
	a = 1
	inputFASTQfilename = []
	commandline = ''
	while a > 0 and a <= max(fastqfiledictionary, key=int):
		inputFASTQfilename = fastqfiledictionary[a]
		FASTQtoFASTA_commandline = 'seqkit fq2fa ' + str(inputFASTQfilename) + ' > ' + str(inputFASTQfilename)[:-6] + '.fasta'
		print('Seqkit command: ' + FASTQtoFASTA_commandline)		
		print('Input file name: ' + inputFASTQfilename)
		subprocess.run(FASTQtoFASTA_commandline, shell = True)
		a = a + 1

FASTQtoFASTA()


#Checking the sequencing alignment FASTA files in folder
FASTAFile = glob.glob(str(inputdir) + '/kraken2_results/non_human_fq/*.fasta')
TotalFASTAFile = sum('.fasta' in f for f in FASTAFile)
print('The total number of sequencing FASTA files is: ' + str(TotalFASTAFile))
FASTAfiledictionary = dict(enumerate(FASTAFile, 1)) #Setting a dictionary for the FASTA files in folder

#Submitting the FASTA files to BLASTN analysis.
def BLASTN():
	b = 1
	PathtoFASTAfile = str(inputdir) + '/kraken2_results/non_human_fq/'
	inputFASTAfilename = []
	commandline = ''
	while b > 0 and b <= max(FASTAfiledictionary, key=int):
		inputFASTAfilename = FASTAfiledictionary[b]
		BLASTN_commandline = 'blastn -db ' + str(amrdb) +'/AMR_CDS -evalue 1e-5 -perc_identity 90 -qcov_hsp_perc 20 -num_threads 8 -outfmt "6 qseqid sseqid sscinames qcovs pident qstart qend sstart send evalue" -max_target_seqs 1 -query ' + str(inputFASTAfilename) + ' -out ' + str(inputdir) + '/AMR_results/AMR/' + inputFASTAfilename.rsplit('/')[-1][:-6] + '_AMR_hit_table.csv'
		print('BLASTN command: ' + BLASTN_commandline)		
		print('Input file name: ' + inputFASTAfilename)
		subprocess.run(BLASTN_commandline, shell = True)
		b = b + 1

# original commandline "blastn -db /home/gilmansiu4/miniconda3/envs/amrfinderplus/share/amrfinderplus/data/2023-08-08.2/AMR_CDS -evalue 1e-5 -perc_identity 90 -qcov_hsp_perc 20 -num_threads 8 -outfmt "6 qseqid sseqid sscinames qcovs pident qstart qend sstart send evalue" -max_target_seqs 1 -query "./results/non_human_fq/BC01_microbial.fasta" -out "./results/AMR_results/AMR/BC01_AMR_hit_table.csv"

BLASTN()

print('BLAST_amr analysis is complete.')
