#!/usr/bin/env python

"""
DESCRIPTION 
Create a PCA plot from PLINK2 output .eigenvec and .eigenval files.

USAGE
plot_plink_pca.py /.../PREFIX.eigenvec /.../PREFIX.eigenval OUTGROUP_ID
Use absolute paths.

AUTHOR AND CHANGE LOG
Written by Jonas Lescroart on 27 January 2022
"""

# Import modules
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

# Initialize parser
msg = "Python script to plot a PCA from PLINK2 --pca output."
parser = argparse.ArgumentParser(description = msg)

# Adding arguments
parser.add_argument(
    "--vec", 
    metavar = "/.../PREFIX.eigenvec", 
    help = "PLINK2 output: absolute path to PREFIX.eigenvec file.")
parser.add_argument(
    "--val", 
    metavar = "/.../PREFIX.eigenval", 
    help = "PLINK2 output: absolute path to PREFIX.eigenval file.")
parser.add_argument(
    "-o", "--output", 
    metavar = "/.../PREFIX.svg", 
    help = "Absolute path to output file in svg format.")

# Read arguments from command line
args = parser.parse_args()

# Assertions
assert args.vec.endswith(".eigenvec")
assert args.val.endswith(".eigenval")
if args.output:
    assert args.output.endswith(".svg")
    outfile = args.output
else:
    outfile =  args.vec[:-9] + ".svg"

# Read input data
eigenvecs = pd.read_csv(args.vec, sep='\t', header=0)
eigenvecs['#FID']
eigenvecs = eigenvecs.set_index(eigenvecs['#FID'])
eigenvecs.pop('IID')
eigenvecs.pop('#FID')

with open(args.val,"r") as f:
    eigenvals = f.readlines()

# Dictionary linking PCs to their percentage of variation
column_names = eigenvecs.columns.values.tolist()
eigenvals = dict(zip(column_names, eigenvals))
for k in eigenvals:
    eigenvals[k] = float(eigenvals[k].rstrip())
sum_eigenvals = sum(eigenvals.values())
for k in eigenvals:
    eigenvals[k] = round((eigenvals[k]/sum_eigenvals) * 100)

# Create plot
pcx = 'PC1'
pcy = 'PC2'

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(1, 1, 1)

plt.scatter(eigenvecs[pcx], eigenvecs[pcy],c='red')
ax.set_xlabel(pcx + " (" + str(eigenvals[pcx]) + "%)")
ax.set_ylabel(pcy + " (" + str(eigenvals[pcy]) + "%)")

for i, sample_ID in enumerate(eigenvecs.index.values):
    ax.annotate(sample_ID, (eigenvecs[pcx][i], eigenvecs[pcy][i]))
#add PC3-4 to the plot.

# Save plot
plt.savefig(outfile, format = "svg")

