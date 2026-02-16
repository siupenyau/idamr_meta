import pandas as pd
import os
import sys
import glob
import openpyxl

inputdir = sys.argv[1]
samplelistfile = sys.argv[2]

print('Input directory: ' + inputdir)
print('Sample list file: ' + samplelistfile)

# Checking the sample list and concatenating the sequencing read files.
samplelisttable = pd.read_excel(samplelistfile)
samplelist = list(samplelisttable.iterrows())
print('Number of samples on the provided sample list = ' + str(len(samplelist)))
if len(samplelist) == 0:
    print('The provided sample list is empty. Please input the barcodes and the samples into the excel template.')
    sys.exit(1)  # Exit the program with an error code and message
else:
    for _, row in samplelist:
        barcode = str(row[0])
        print('Barcode: ' + barcode)
        sampleID = str(row[1])
        print('SampleID: ' + sampleID)
        sample_prefix = str(sampleID)

        # Read CSV1 and extract columns 0 and 1
        csv1_file = os.path.join(inputdir, 'AMR_results', 'AMR', f'{sample_prefix}_filtered_microbial_AMR_hit_table.csv')
        if not os.path.isfile(csv1_file) or os.path.getsize(csv1_file) == 0:
            print(f"CSV file not found or empty for {sample_prefix}. Skipping to the next sample.")
            continue

        csv1_data = pd.read_csv(csv1_file, delimiter='\t', header=None)
        csv1_extracted = csv1_data.iloc[:, [0, 1]]

        # Read CSV2 and extract columns 1, 2, and 3
        csv2_file = os.path.join(inputdir, 'AMR_results', 'nt', f'{sample_prefix}_filtered_microbial_AMR_nt_hit_table.csv')
        if not os.path.isfile(csv2_file) or os.path.getsize(csv2_file) == 0:
            print(f"CSV file not found or empty for {sample_prefix}. Skipping to the next sample.")
            continue

        csv2_data = pd.read_csv(csv2_file, delimiter='\t', header=None)
        csv2_extracted = csv2_data.iloc[:, [0, 1, 2]]

        # Merge the extracted data based on column 0 (index 0)
        merged_data = pd.merge(csv1_extracted, csv2_extracted, left_on=0, right_on=0)

        # Save the merged data as a new CSV file without the header
        final_csv_file = os.path.join(inputdir, 'AMR_results', f'{sample_prefix}_filtered_microbial_AMR_final.csv')
        merged_data.to_csv(final_csv_file, index=False, header=False)

        print('The final AMR hit table saved in:', final_csv_file)