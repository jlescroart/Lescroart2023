#!/usr/bin/env python

"""
DESCRIPTION
Python script to convert a fasta files to a phylip file.

USAGE
python fasta2phylip.py --input [infile.fasta] --output [outfile.phy]
Provide full paths.
Make sure output file doesn't exist yet, else it will be overwritten.

Author: Jonas Lescroart

CHANGE LOG
17SEP22: script created from fasta2phylipBPP.py 
"""

#import modules
import os
import string
import re
import argparse

#take command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input', help = "Absolute path to fasta file", type = str)
parser.add_argument('--output', help = "Absolute path to phylip file", type = str)
args = parser.parse_args()

#assertions
assert args.input.endswith(tuple([".fa", ".fasta", ".fna"])), "Provide a fasta file as input"
assert args.output.endswith(tuple([".phy", ".phylip"])), "Provide a phylips filename as output"

#define functions
def fasta2phylip(oldlines):
    
    #empty start variables
    firstlines = []
    newlines = []
    templines = []
    taxa = 0
    bp = 0
    
    #iterate through fasta of one window, line by line
    for line in oldlines:
        if line.startswith(">"):
            line = line.replace(">", "").rstrip()
            line += " " * (13 - len(line))
            line = "\n" + line
            templines.append(line)
            taxa += 1
        elif line.startswith(("A", "C", "G", "T", "N")):
            line = line.replace("N", "?").rstrip()
            templines[-1] += line
            bp = len(templines[-1]) - 14
        else:
            None
    
    #create phylip style header and add sequences
    newlines.append("   " + str(taxa) + "   " + str(bp)+ "\n")
    newlines += templines
    
    #return as list of lines
    return(newlines)

#variables
infile = args.input
outfile = args.output

#convert
fasta = open(infile, "r")
fasta_lines = fasta.readlines()
fasta.close()

phylip = open(outfile, "w")
phylip.write("".join(fasta2phylip(fasta_lines)))
phylip.close()

