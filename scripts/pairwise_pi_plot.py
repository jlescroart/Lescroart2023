#!/usr/bin/env python

"""
DESCRIPTION
Script to sum and average per-site pairwise nucleotide differences (π).
Input is a series of csv files generated with pairwise_pi.py,
or text file listing the path to csv files one per line.
Output is a matrix of average pi values in csv format,
printed to screen or to file with -o option.

USAGE
python3 pairwise_pi_plot.py --help
python3 pairwise_pi_plot.py -l filenames.txt -o outfile.csv
or
python3 pairwise_pi_plot.py -i file1.csv file2.csv -o outfile.csv

Version: 18 January 2021
Author: Jonas Lescroart
"""

# Import modules
import pandas as pd
import argparse
import os

# Initialize parser
msg = "Use the output csv files of pairwise_pi.py and input here as either separate files (-i file1.csv file2.csv...) or with a text file containing the full path to all the csv files (-l filenames.txt). If no output file specified, prints to std out."
parser = argparse.ArgumentParser(description = msg)

# Adding arguments
parser.add_argument("-l", "--list", metavar = "filenames.txt", help = "Textfile listing the absolute paths to input csv files. Don't use together with -i.")
parser.add_argument("-i", "--input",
    nargs = "+",
    metavar = "input.csv",
    help = "One or multiple input files in csv format. Don't use together with -l.")
parser.add_argument("-o", "--output", help = "Absolute path to output file in csv format.")

# Read arguments from command line
args = parser.parse_args()
print(args)

if args.input:
    infiles = args.input

if args.list:
    with open(args.list) as filelist:
        infiles = [infile.strip() for infile in filelist.readlines()]

if args.output:
    outfile = args.output

# Assert that input files are csv format
for infile in infiles:
    if not infile.endswith(".csv"):
        raise Exception("Invalid input files: must be .csv files")

# Iterate over csv files and sum pi values
for i in range(len(infiles)):
    csv = pd.read_csv(infiles[i], sep = ",", index_col = 0, na_values = ["None"])
    if csv.isnull().values.any():
        pass
    else:
        if "total" not in globals():
            total = csv
            counter = 1
        else:
            assert csv.index.values.tolist() == total.index.values.tolist()
            assert csv.columns.values.tolist() == total.columns.values.tolist()
            total += csv
            counter += 1

# Output average pi values
average = total/counter
average.to_csv(outfile)

# NJ tree from distance matrix. Now implemented as function directly in the Snakefile so redundant here.
#import skbio

#distance_matrix = skbio.DistanceMatrix(average, ids = average.index.values.tolist())
#nj_newick = skbio.nj(distance_matrix, result_constructor=str)
#with open(outfile[:-4]+".nwk", "w") as nwk:
#    nwk.write(nj_newick)

# Add bootsstrap later

# Add plots

