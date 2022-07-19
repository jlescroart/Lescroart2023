#!/usr/bin/env python

"""
DESCRIPTION
Script to plot MSMC2 output with bootstraps.
Input files are a *.final.txt file for the main sample
and additional *.final.txt files for the bootstrap replicates.

USAGE
python msmc2_plot_bs.py
    --input /fullpath/SAMPLE.final.txt
    --output /fullpath/SAMPLE.pdf
    --bootstrap /fullpath/*.final.txt
    --mu [mutation rate, default 1e-8]
    --gen [generation time, default 1]

Author: Jonas Lescroart
"""

#import modules
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

#take command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input', help="Absolute path to *.final.txt file", type= str)
parser.add_argument('--output', help="Absolute path to *.pdf file", type= str)
parser.add_argument('--bootstrap', help="Absolute path to bootstrap iteration *.final.txt files", nargs='+', type= str)
parser.add_argument('--mu', help="Mutation rate", default=1e-8, type=float)
parser.add_argument('--gen', help="Generation time. Use default (1) to display time in generations instead of years", default=1, type=int)
args = parser.parse_args()

#assert obligatory arguments and create variables
assert args.input, "usage: msmc2_plot_bs.py [-h] [--input SAMPLE.final.txt] optional: [--output] [--bootstrap] [--mu] [--gen]"
in_file = args.input
sample_id = in_file.split('/')[-1][:-10]

#initiate figure
plt.figure(figsize = [10, 5])

#add bootstrap lines if present
if args.bootstrap:
    bs_files = args.bootstrap
    for file in range(len(bs_files)):
        if file == 0: #label for first entry to add to legend once
            data = pd.read_csv(bs_files[file], delim_whitespace = True)
            plt.step(data["left_time_boundary"]/args.mu*args.gen,
            (1/data["lambda"])/(2*args.mu),
            color = "lightblue", linestyle='dashed', linewidth = 0.5,
            label = "Bootstrap x" + str(len(bs_files)))
        else:
            data = pd.read_csv(bs_files[file], delim_whitespace = True)
            plt.step(data["left_time_boundary"]/args.mu*args.gen,
            (1/data["lambda"])/(2*args.mu),
            color = "lightblue", linestyle='dashed', linewidth = 0.5)

#add main line element
data = pd.read_csv(in_file, delim_whitespace = True)
plt.step(data["left_time_boundary"]/args.mu*args.gen,
(1/data["lambda"])/(2*args.mu),
color = "blue",
label = sample_id)

#plot other elements
if args.gen == 1:
    plt.xlabel("Generations (μ = " + str(args.mu) + ")")
    plt.xlim(left = 1e3, right = 1e6)
else:
    plt.xlabel("Years before present (μ = " + str(args.mu) + ")")
    plt.xlim(left = 1e3)
plt.ylim(0,40e4)
plt.ylabel("Effective population size (Ne)")
plt.gca().set_xscale("log")
plt.legend()
plt.title(sample_id)

#save plot and close
if args.output:
    plt.savefig(args.output, format = "pdf")
else:
    if in_file.startswith("/"):
        path = str(('/').join(in_file.split('/')[:-1])) + '/'
    else:
        path = os.getcwd() + '/'
    plt.savefig(path + sample_id + ".pdf", format = "pdf")
plt.close()
