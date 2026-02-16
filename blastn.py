import os, subprocess, glob, shutil, sys
import pandas as pd

print('Starting the BLAST_nt analysis. Please wait.')

inputdir=sys.argv[1]
blastdb=sys.argv[2]+str('/blast_db/')
currentdir=os.getcwd()

if not os.path.exists(str(inputdir) + '/AMR_results/nt/'):
	os.makedirs(str(inputdir) + '/AMR_results/nt/')


#Checking the sequencing alignment FASTA files in folder
FASTAFile = glob.glob(str(inputdir) + '/AMR_results/AMR_fasta/*_AMR.fasta')
TotalFASTAFile = sum('.fasta' in f for f in FASTAFile)
print('The total number of sequencing FASTA files is: ' + str(TotalFASTAFile))
FASTAfiledictionary = dict(enumerate(FASTAFile, 1)) #Setting a dictionary for the FASTA files in folder


#Submitting the FASTA files to BLAST analysis.
def blast_analysis():
	b = 1
	inputFASTAfilename = []
	commandline = ''
	while b > 0 and b <= max(FASTAfiledictionary, key=int):
		inputFASTAfilename = FASTAfiledictionary[b]
		blast_commandline = 'blastn -db ' + str(blastdb) + '/nt -num_threads 8 -perc_identity 90 -qcov_hsp_perc 20 -evalue 1e-5 -outfmt "6 qseqid sseqid sscinames qcovs pident qstart qend sstart send evalue" -max_target_seqs 1 -query ' + str(inputFASTAfilename) + ' -out ' + str(inputdir) + '/AMR_results/nt/' + inputFASTAfilename.rsplit('/')[-1][:-6] + '_nt_hit_table.csv'
		print('BLASTN command: ' + blast_commandline)		
		print('Input file name: ' + inputFASTAfilename)
		subprocess.run(blast_commandline, shell = True)
		b = b + 1

blast_analysis()


print('BLAST_nt analysis is complete. Please check the results in folder.')

#original command line = 'blastn -db nt -num_threads 8 -perc_identity 90 -qcov_hsp_perc 20 -evalue 1e-5 -outfmt "6 qseqid sseqid sscinames qcovs pident qstart qend sstart send evalue" -max_target_seqs 1 -query "./results/AMR_results/AMR_fasta/BC01_AMR.fasta" -out "./results/AMR_results/nt/BC01_nt_hit_table.csv"
