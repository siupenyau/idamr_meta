import os, subprocess, glob, shutil, sys
import pandas as pd

print('Starting the Kraken2 analysis. Please wait.')

#Checking the sequencing FASTQ files in folder
inputdir=sys.argv[1]
pathtokraken2db=sys.argv[2]+str('/kraken2_db/pluspf/')
pathtohumandb=sys.argv[2]+str('/human_db/')
currentdir=os.getcwd()
fastqFile = glob.glob(str(inputdir) + '/nanofilt/*.fastq')
TotalfastqFile = sum('.fastq' in f for f in fastqFile)
print('The total number of sequencing fastq files in folder is: ' + str(TotalfastqFile))
fastqfiledictionary = dict(enumerate(fastqFile, 1)) #Setting a dictionary for the fastq files in folder

if not os.path.exists(str(inputdir) + '/kraken2_results/human/'):
	os.makedirs(str(inputdir) + '/kraken2_results/human/')

if not os.path.exists(str(inputdir) + '/kraken2_results/non_human_fq/'):
	os.makedirs(str(inputdir) + '/kraken2_results/non_human_fq/')

if not os.path.exists(str(inputdir) + '/kraken2_results/pluspf/'):
	os.makedirs(str(inputdir) + '/kraken2_results/pluspf/')

#kraken2 to remove human reads
def kraken2_filtering():
	a = 1
	PathtoFASTQfile = str(inputdir) + '/nanofilt/'
	inputFASTQfilename = []
	commandline = ''
	while a > 0 and a <= max(fastqfiledictionary, key=int):
		inputFASTQfilename = fastqfiledictionary[a]
		kraken2_filtering_commandline = 'kraken2 --db ' + str(pathtohumandb) + ' --threads 8 --report ' + str(inputdir) + '/kraken2_results/human/' + inputFASTQfilename.rsplit('/')[-1][:-6] + '_human.csv --confidence 0.1 --unclassified-out ' + str(inputdir) + '/kraken2_results/non_human_fq/' + inputFASTQfilename.rsplit('/')[-1][:-6] + '_microbial.fastq ' + str(inputFASTQfilename)
		print('Kraken2 filtering command: ' + kraken2_filtering_commandline)		
		print('Input file name: ' + inputFASTQfilename)
		subprocess.run(kraken2_filtering_commandline, shell = True)
		a = a + 1

kraken2_filtering()

#original command line "kraken2 --db /mnt/Backup2/kraken2_DB/human_db/ --threads 8 --report "./results/human/BC01_human.csv" --confidence 0.1 --unclassified-out "./results/non_human_fq/BC01_microbial.fastq" "./nanofilt/BC01_filtered.fastq"

microbialfastqFile = glob.glob(str(inputdir) + '/kraken2_results/non_human_fq/*_microbial.fastq')
TotalmicrobialfastqFile = sum('_microbial.fastq' in f for f in microbialfastqFile)
print('The total number of sequencing fastq files in the folder is: ' + str(TotalmicrobialfastqFile))
microbialfastqfiledictionary = dict(enumerate(microbialfastqFile, 1)) #Setting a dictionary for the microbial fastq files in folder

#kraken2 to classify microbial reads
def kraken2_classification():
    b = 1
    inputmicrobialFASTQfilename = []
    commandline = ''
    while b > 0 and b <= max(microbialfastqfiledictionary, key=int):
        inputmicrobialFASTQfilename = microbialfastqfiledictionary[b]
        kraken2_classification_commandline = 'kraken2 --db ' + str(pathtokraken2db) + ' --threads 8 --report ' + str(inputdir) + '/kraken2_results/pluspf/' + inputmicrobialFASTQfilename.rsplit('/')[-1][:-6] + '.csv --confidence 0.1 ' + str(inputmicrobialFASTQfilename)
        print('Kraken2 classification command: ' + kraken2_classification_commandline)        
        print('Input file name: ' + inputmicrobialFASTQfilename)
        subprocess.run(kraken2_classification_commandline, shell=True)
        bracken_commandline = 'bracken -d ' + str(pathtokraken2db) + ' -i ' + str(inputdir) + '/kraken2_results/pluspf/' + inputmicrobialFASTQfilename.rsplit('/')[-1][:-6] + '.csv -o ' + str(inputdir) + '/kraken2_results/pluspf/' + inputmicrobialFASTQfilename.rsplit('/')[-1][:-6] + '_t10.tsv -t 10'
        print('Bracken command: ' + bracken_commandline)        
        subprocess.run(bracken_commandline, shell=True)
        b = b + 1

kraken2_classification()

# original commandline "kraken2 --db /home/gilmansiu4/kraken2_db/pluspf/ --threads 8 --confidence 0.1 --report ./results/kraken2/BC01.csv ./results/non_human_fq/BC01_microbial.fastq"
# original commandline "bracken -d "/home/gilmansiu4/kraken2_db/pluspf/" -i ./results/kraken2/BC01.csv -o ./results/kraken2/BC01_t10.tsv -t 10"

