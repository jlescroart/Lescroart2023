#!/usr/bin/env python

"""
DESCRIPTION
Script to calculate the consensus of a series of MSMC2 bootstraps.
Input files are *.final.txt files for the bootstrap replicates.

USAGE
python msmc2_consensus.py
    --input /fullpath/*.final.txt
    --output /fullpath/SAMPLE_consensus.final.txt

Author: Jonas Lescroart
"""

#import modules
import argparse
import pandas as pd

#take command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input', help="Absolute path to bootstrap iteration *.final.txt files", nargs='+', type= str)
parser.add_argument('--output', help="Absolute path to *consensus.final.txt file", type= str)
args = parser.parse_args()

#assert obligatory arguments and create variables
assert args.input, "usage: msmc2_plot_bs.py [-h] [--input *.final.txt] [--output SAMPLE_consensus.final.txt]"
infiles = args.input

#average bootstraps
for file in range(len(infiles)):
    if file == 0:
        cons = pd.read_csv(infiles[file], delim_whitespace = True)
    else:
        cons += pd.read_csv(infiles[file], delim_whitespace = True)

cons = cons/len(infiles)
cons.to_csv(args.output, sep = "\t", index = False)
