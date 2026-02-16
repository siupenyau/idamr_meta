IDAMR_meta

A workflow for metagenomic species profiling and antimicrobial resistance (AMR) gene detection.

Overview

IDAMR_meta is a lightweight analysis pipeline designed for processing nanopore metagenomic sequencing reads. It performs read filtering, host read removal, taxonomic classification, species abundance estimation, and antimicrobial resistance (AMR) gene identification using established bioinformatics tools.

Workflow Summary
1. Read Filtering
Raw nanopore reads are first filtered using NanoFilt to remove low‑quality or short reads.
Reads shorter than 200 bp are discarded.
This step improves the accuracy of downstream classification.
2. Removal of Human Reads
To eliminate host contamination, filtered reads are processed with:
Kraken 2
Human reference database: GRCh38.p13
Reads classified as human are removed, ensuring only non‑host reads proceed to taxonomic and AMR analysis.
3. Taxonomic Classification
Non‑human reads are classified using:
Kraken 2
PlusPF database, which provides broad microbial coverage.
This step assigns taxa to each read with high throughput and accuracy.
4. Species Abundance Estimation
Species‑level abundance is refined using:
Bracken,
which re-estimates read counts from the Kraken 2 output to provide more reliable abundance quantification.
5. AMR Gene Identification
For antimicrobial resistance profiling:
Filtered reads (after host removal) are aligned using BLAST+
Against the NCBI Reference Gene Catalog, following the methodology described in the NTS workflow.
This step detects potential AMR genes present in the metagenomic sample.

Dependencies

- NanoFilt
- Kraken 2
- Bracken
- BLAST+

Databases:
- GRCh38.p13 (for host removal)
- PlusPF (for taxonomic classification)
- NCBI Reference Gene Catalog (for AMR identification)

Installation:
Download the environment.yml and run the following:

conda env create -f environment.yml
