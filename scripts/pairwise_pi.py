#!/usr/bin/env python

"""
DESCRIPTION
Script to calculate per-site pairwise nucleotide differences (π).
Input is a multiple alignment file in fasta format.
Output is a matrix of pi values in csv format, printed to screen.

USAGE
python3 pairwise_pi.py infile.fasta > outfile.csv

Version: 13 January 2021
Author: Jonas Lescroart
"""

# Import modules
from Bio import SeqIO
import pandas as pd
import sys
import os
import re

# Define functions
def pairwise_pi(sequence1, sequence2):
    # Returns a single per-site pi value for two DNA sequences of equal length.
    # Sites with missing data are completely ignored.
    variable_sites = 0
    invariable_sites = 0

    zipped = zip(sequence1, sequence2)
    for i,j in zipped:
        if 'N' in (i.upper(), j.upper()):
            pass
        elif i.upper() == j.upper():
            invariable_sites += 1
        else:
            variable_sites += 1

    if variable_sites == invariable_sites == 0:
        pi = None
    else:
        pi = variable_sites/(invariable_sites + variable_sites)
    return pi

# Take input
if sys.argv[1].endswith(tuple([".fasta", "fa", "fas", "fna"])):
    infile = sys.argv[1]
else:
    raise Exception("Invalid input arguments")

#outfile = infiles[i].split(".")
#if re.match("fasta|fa|fas|fna", outfile[-1]):
#    outfile = outfile[:-1]
#outfile = ".".join(outfile) + ".csv"

# Calculate pairwise difference per file and output csv

with open(infile, "r") as handle:
    record_dict = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
    ids = [record_dict[k].id for k in record_dict.keys()]
    ids.sort()
    df = pd.DataFrame(columns = ids, index = ids)
    for i in df.index:
        for c in df.columns:
            df[i][c] = pairwise_pi(record_dict[i], record_dict[c])
    #df.to_csv(outfile)
    print(df.to_csv())

# Gather all csv for plots, genome-wide average etc (move to different script)
#assert df.index.values.tolist() == df2.index.values.tolist()
#assert df.columns.values.tolist() == df2.columns.values.tolist()
#if None in df.to_numpy():

#(df1 + df2 + ... + dfn)/n
