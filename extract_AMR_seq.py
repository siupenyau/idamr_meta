from Bio import SeqIO
import csv, sys, glob, os

inputdir = sys.argv[1]

def extract_sequences(fasta_file, csv_file, output_file):
    # Read the CSV file and extract sequence IDs
    sequence_ids = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            sequence_ids.append(row[0])

    # Extract fasta sequences based on sequence IDs
    sequences = []
    with open(fasta_file, 'r') as fastafile:
        for record in SeqIO.parse(fastafile, "fasta"):
            if record.id in sequence_ids:
                sequences.append(record)

    # Create the output directory if it doesn't exist
    output_directory = str(inputdir) + "/AMR_results/AMR_fasta/"
    os.makedirs(output_directory, exist_ok=True)

    # Write the extracted sequences to the output FASTA file
    output_file = output_directory + os.path.basename(fasta_file)[:-6] + "_AMR.fasta"
    with open(output_file, 'w') as outfile:
        SeqIO.write(sequences, outfile, "fasta")

    print("Extraction complete. Sequences are saved in", output_file)


FASTAFile = glob.glob(str(inputdir) + '/kraken2_results/non_human_fq/*.fasta')
TotalFASTAFile = sum('.fasta' in f for f in FASTAFile)
print('The total number of sequencing FASTA files is:', TotalFASTAFile)
FASTAfiledictionary = dict(enumerate(FASTAFile, 1)) #Setting a dictionary for the FASTA files in folder

for a in range(1, len(FASTAfiledictionary) + 1):
    fasta_file = FASTAfiledictionary[a]
    csv_file = str(inputdir) + '/AMR_results/AMR/' + os.path.basename(fasta_file)[:-6] + '_AMR_hit_table.csv'
    extract_sequences(fasta_file, csv_file, "")
