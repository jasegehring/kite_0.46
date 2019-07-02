# _kite_: kallisto indexing and tag extraction

This package includes utilities that enable fast and accurate pre-processing of Feature Barcoding experiments, a common datatype in single-cell genomics. In Feature Barcoding assays, cellular data are recorded as short DNA sequences using procedures adapted from single-cell RNA-seq. 

The __kite ("kallisto indexing and tag extraction__") package is used to prepare input files prior to running the [kallisto | bustools](https://www.kallistobus.tools/getting_started.html) scRNA-seq pipeline. Starting with a .csv file containing Feature Barcode names and Feature Barcode sequences, the command line program `featuremap.py` generates a "mismatch map" and outputs "mismatch" fasta and "mismatch" transcript-to-gene (t2g) files. The mismatch files, containing the Feature Barcode sequences and their Hamming distance = 1 mismatches, are used to run kallisto | bustools on Feature Barcoding data. 

The mismatch fasta file is used by `kallisto index` with a k-mer length `-k` set to the length of the Feature Barcode. 

The mismatch t2g file is used by `bustools count` to generate a Features x Cells matrix. 

In this way, kallisto | bustools will effectively search the sequencing data for the Feature Barcodes and their Hamming distance = 1 neighbors. We find that for Feature Barcodes of moderate length (6-15bp) pre-processing is remarkably fast and the results equivalent to or better than those from traditional alignment.

A walk-through from the kallisto | bustools [Tutorials](https://www.kallistobus.tools/tutorials) page is reproduced below, and a copmlete Feature Barcode analysis can be found in the [docs](https://github.com/pachterlab/kite/tree/master/docs/) directory of the `kite` GitHub repository.

## kite Installation
Clone the GitHub repo and use pip to install the kite package
```
!mkdir ./FeatureBarcoding
!cd ./FeatureBarcoding
!git clone https://github.com/pachterlab/kite
!pip install -e ./kite
```
## System Requirements
Feature Barcode pre-processing requires `kite` as well as up-to-date versions of `kallisto` and `bustools`
```
kite 0.0.1
kallisto 0.46 or higher
bustools 0.39.0 or higher
```

For downstream analysis, we use [ScanPy](https://scanpy.readthedocs.io/en/stable/installation.html) (Wolf et. al, Genome Biology 2018) and the [LeidenAlg](https://github.com/vtraag/leidenalg) clustering package (Traag et. al, arXiv 2018).

## kite Utilities

#### `featuremap.py FeatureBarcodes.csv`
This command line program is the easiest way to use `kite` for Feature Barcoding experiments. It takes a .csv input and outputs "mismatch" transcript-to-gene (t2g) and fasta files that can be used by kallisto | bustools to complete pre-processing (see below and Vignettes).

FeatureBarcodes.csv: path to a .csv-formatted file containing Feature Barcode names and sequences (example below).

returns mismatch t2g and fasta files saved to the working directory

#### `kite_mismatch_maps(FeatureBarcodes.csv, mismatch_t2g_path, mismatch_fasta_path)`
This Python wrapper function is the easiest way to use `kite` from within Python. It outputs "mismatch" t2g and fasta files that can be used by kallisto | bustools to complete pre-processing(see below and Vignettes).

FeatureBarcodes.csv: path to a a .csv-formatted file containing Feature Barcode names and sequences (example below).
mismatch_t2g_path: filepath for a new "mismatch" t2g file  
mismatch_fasta_path: filepath for a new "mismatch" fasta file

returns mismatch t2g and fasta files to the specified directories

#### `make_mismatch_map(FeatureDict)`
This function returns all sample tags and and their single base mismatches (Hamming distance 1) as an OrderedDict object. The number of elements in the object is (k=the length of the Feature Barocdes)*(3=altnerative base pairs for each base)*(N=number of Feature Barocdes) + (N=number of Feature Barcode sequences). For the 10x example dataset, 17 Feature Barcodes of length k=15 are used. These yield 15x3x17+17=782 entries in the OrderedDict object. 

FeatureDict: a Python dictionary with Feature Barcode name : Feature Barcode sequence as key:value pairs

returns an OrderedDict object including correct and mismatch sequences for each whitelist Feature Barcode

#### `write_mismatch_map(tag_map, mismatch_t2g_path, mismatch_fasta_path)`
Saves the OrderedDict generated by `make_mismatch_map` to file in fasta and t2g formats for building the kallisto index and running bustools count, respectively.

tag_map: OrderedDict object produced by `make_mismatch_map`
mismatch_t2g_path: filepath for a new "mismatch" t2g file 
mismatch_fasta_path: filepath for a new "mismatch" fasta file

returns mismatch t2g and fasta files to the specified directories

## NOTE: Use only odd values for k-mer length during `kallisto index` 
To avoid potential pseudoalignment errors arising from inverted repeats, kallisto only accepts odd values for the k-mer length `-k`. If your Feature Barcodes have an even length, just add an appropriate constant base on one side and follow the protocol as suggested. Adding constant bases in this way increases specificity and may be useful for experiments with low sequencing quality or very short Feature Barcodes. 

## Brief Example: 1k PBMCs from a Healthy Donor - Gene Expression and Cell Surface Protein

The [docs](https://github.com/jgehringUCB/kite/tree/master/docs) folder contains a complete analysis ([10x_kiteVignette.ipynb](https://github.com/jgehringUCB/kite/tree/master/docs/10X_kiteVignette.ipynb)) for a 10x dataset collected on ~730 peripheral blood mononuclear cells (PBMCs) labeled with 17 unique Feature Barcoded antibodies. The dataset can be found [here](https://support.10xgenomics.com/single-cell-gene-expression/datasets/3.0.0/pbmc_1k_protein_v3).

The following is an abbreviated reproduced in the [Tutorials](https://www.kallistobus.tools/tutorials) section of the kallisto | bustools website. 

### Download Files for Example Data

Navigate to a new directory and download 10x data with wget. Unzip files as shown.
The 10x 3M-february 2018 cell barcode whitelist is included with the `kite` GitHub repo [here](https://github.com/jgehringUCB/kite/blob/master/docs/3M-february-2018.txt.gz). __Place it in the same directory.__
```
$wget http://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_1k_protein_v3/pbmc_1k_protein_v3_fastqs.tar
$tar -xvf ./pbmc_1k_protein_v3_fastqs.tar
$wget http://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_1k_protein_v3/pbmc_1k_protein_v3_feature_ref.csv
$wget http://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_1k_protein_v3/pbmc_1k_protein_v3_filtered_feature_bc_matrix.tar.gz
$!tar xvzf ./pbmc_1k_protein_v3_filtered_feature_bc_matrix.tar.gz
```

The directory now includes the raw fastqs, the Feature Barcode whitelist reference, the 10x 3M-february-2018 cell barcode whitelist, and the CellRanger Features x Cells matrix. See notebook for example. 
```
pbmc_1k_protein_v3_fastqs/
pbmc_1k_protein_v3_feature_ref.csv
3M-february-2018.txt
filtered_feature_bc_matrix/
```

We start by making a Python dictionary containing Feature Barcode names and Feature Barcode sequences as key:value pairs. Code to generate this dictionary from the 10x `pbmc_1k_protein_v3_feature_ref.csv` is provided with the iPython notebook in the [docs](https://github.com/pachterlab/kite/tree/master/docs/) folder. 

| Feature Barcode name  | Feature Barcode sequence |
| ------------- | ------------- |
| CD3_TotalSeqB | AACAAGACCCTTGAG |
| CD8a_TotalSeqB | TACCCGTAATAGCGT |
| CD14_TotalSeqB | GAAAGTCAAAGCACT |
| CD15_TotalSeqB | ACGAATCAATCTGTG |
| CD16_TotalSeqB | GTCTTTGTCAGTGCA |
| CD56_TotalSeqB | GTTGTCCGACAATAC |
| CD19_TotalSeqB | TCAACGCTTGGCTAG |
| CD25_TotalSeqB | GTGCATTCAACAGTA |
| CD45RA_TotalSeqB | GATGAGAACAGGTTT |
| CD45RO_TotalSeqB | TGCATGTCATCGGTG |
| PD-1_TotalSeqB | AAGTCGTGAGGCATG |
| TIGIT_TotalSeqB | TGAAGGCTCATTTGT |
| CD127_TotalSeqB | ACATTGACGCAACTA |
| IgG2a_control_TotalSeqB | CTCTATTCAGACCAG |
| IgG1_control_TotalSeqB | ACTCACTGGAGTCTC |
| IgG2b_control_TotalSeqB | ATCACATCGTTGCCA |

The kite_mismatch_maps function takes the Python dictionary (featurebarcodes) and writes a mismatch t2g and mismatch fasta. In this way, the 17 original Feature Barcodes become a mismatch fasta file and a mismatch t2g file, each with 782 entries.

```
import kite
kite.kite_mismatch_maps(featurebarcodes, './10xFeatures_t2g.txt', './10xFeaturesMismatch.fa')
```

Processing Feature Barcodes is similar to processing transcripts except instead of looking for transcript fragments of length `-k` (the k-mer length) in the reads, a "mismatch" index is used to search the raw reads for the Feature Barcode whitelist and mismatch sequences. Please refer to the [kallisto documentation](https://www.kallistobus.tools/documentation) for more information on the kallisto | bustools workflow. 

Because Feature Barcodes are typically designed to be robust to some sequencing errors, each Feature Barcode and its mismatches are unique across an experiment, thus each Feature Barcode equivalence class has a one-to-one correspondence to a member of the Feature Barcode whitelist. This is reflected in the t2g file, where each mismatch Feature Barcode points to a unique parent Feature Barcode from the whitelist, analogous to the relationship between genes and transcripts in the case of cDNA processing. 

```
!head -4 ./10xFeatures_t2g.txt
CD3_TotalSeqB	CD3_TotalSeqB	CD3_TotalSeqB
CD3_TotalSeqB-0-1	CD3_TotalSeqB	CD3_TotalSeqB
CD3_TotalSeqB-0-2	CD3_TotalSeqB	CD3_TotalSeqB
CD3_TotalSeqB-0-3	CD3_TotalSeqB	CD3_TotalSeqB

!head -8 ./10xFeaturesMismatch.fa
>CD3_TotalSeqB
AACAAGACCCTTGAG
>CD3_TotalSeqB-0-1
TACAAGACCCTTGAG
>CD3_TotalSeqB-0-2
GACAAGACCCTTGAG
>CD3_TotalSeqB-0-3
CACAAGACCCTTGAG
```

The mismatch fasta is used to run `kallisto index`. 

```
!kallisto index -i ./index_path.idx -k 15 ./fasta_path.fa
[build] loading fasta file /home/jgehring/scRNAseq/kITE/10xTest/10xFeaturesMismatch.fa
[build] k-mer length: 15
[build] counting k-mers ... done.
[build] building target de Bruijn graph ...  done 
[build] creating equivalence classes ...  done
[build] target de Bruijn graph has 782 contigs and contains 782 k-mers 
```

Next, `kallisto bus` and `bustools` are used without modifications. 

```
!kallisto bus -i ./index_path.idx -o ./ -x 10xv3 -t 4 \
./pbmc_1k_protein_v3_fastqs/pbmc_1k_protein_v3_antibody_fastqs/pbmc_1k_protein_v3_antibody_S2_L001_R1_001.fastq.gz \
./pbmc_1k_protein_v3_fastqs/pbmc_1k_protein_v3_antibody_fastqs/pbmc_1k_protein_v3_antibody_S2_L001_R2_001.fastq.gz \
./pbmc_1k_protein_v3_fastqs/pbmc_1k_protein_v3_antibody_fastqs/pbmc_1k_protein_v3_antibody_S2_L002_R1_001.fastq.gz \
./pbmc_1k_protein_v3_fastqs/pbmc_1k_protein_v3_antibody_fastqs/pbmc_1k_protein_v3_antibody_S2_L002_R2_001.fastq.gz \
```

We now have a BUS file for this pseudoalignment. 
```
!bustools correct -w ./3M-february-2018.txt ./output.bus -o ./output_corrected.bus

!bustools sort -t 4 -o ./output_sorted.bus ./output_corrected.bus

!bustools count -o ./ --genecounts -g ./t2g_path.t2g -e ./matrix.ec -t ./transcripts.txt ./output_sorted.bus

```

`Bustools count` outputs a .mtx-formatted Features x Cells matrix and vectors of gene names and cell barcodes (genes.txt and barcodes.txt). From here, standard analysis packages like ScanPy and Seurat can be used to continue the Feature Barcode analysis. 
