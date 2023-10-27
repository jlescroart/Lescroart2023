#!/usr/bin/env python

"""
DESCRIPTION
Script to plot MSMC2 rCCR output.
Input fileis something like combined_pardinoides_oncilla_consensus.final.txt

USAGE
python msmc2_plot.py combined_pardinoides_oncilla_consensus.final.txt

Author: Jonas Lescroart
"""

#import modules
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#define functions
def getCCRintersect(df, val):
    xVec = generation_time * ((df.left_time_boundary + df.right_time_boundary)/2) / mutation_rate
    yVec = 2.0 * df.lambda_01 / (df.lambda_00 + df.lambda_11)
    i = 0
    while yVec[i] < val:
        i += 1
    assert i > 0 and i <= len(yVec), "CCR intersection index out of bounds: {}".format(i)
    assert yVec[i - 1] < val and yVec[i] >= val, "this should never happen"
    intersectDistance = (val - yVec[i - 1]) / (yVec[i] - yVec[i - 1])
    return xVec[i - 1] + intersectDistance * (xVec[i] - xVec[i - 1])

#take arguments and variables
files = sys.argv[1:]
mutation_rate = 0.86e-8
generation_time = 3.8 #use 1 to express time in generations, use biological generation time to express time in years

#Manual plotting of the relative cross-coalescent rate.
# Code based on https://github.com/StatisticalPopulationGenomics/MSMCandMSMC2/blob/master/plot_msmc.py
msmc_out=pd.read_csv(files[0], sep='\t', header=0)
t_years=generation_time * ((msmc_out.left_time_boundary + msmc_out.right_time_boundary)/2) / mutation_rate

plt.figure(figsize = [10, 8])
plt.subplot(211)
plt.semilogx(t_years, (1/msmc_out.lambda_00)/(2*mutation_rate), drawstyle='steps', color='purple', label='Andean tiger cat')
plt.semilogx(t_years, (1/msmc_out.lambda_11)/(2*mutation_rate), drawstyle='steps', color='red', label='Costa Rica tiger cat')
plt.xlabel("Years before present (μ = " + str(mutation_rate) + " mutations/bp/gen; generation time = " + str(generation_time)  + "y)")
plt.xlim(left = 3e3, right = 5e6)
plt.ylabel("Effective population size (Ne)")
plt.ylim(0,10e4)
plt.legend()

plt.subplot(212)
relativeCCR=2.0 * msmc_out.lambda_01 / (msmc_out.lambda_00 + msmc_out.lambda_11)
relativeCCR = relativeCCR * plt.ylim()[1] #scale rCCR (0-1) with popsize
plt.semilogx(t_years,relativeCCR, drawstyle='steps', color = "grey", label = "Relative cross-coalescent rate")
plt.xlim(left = 3e3, right = 5e6)
plt.ylim(0,1)
plt.ylabel("Relative cross-coalescent rate (rCCR)")

#split = getCCRintersect(msmc_out, 0.5)
split = getCCRintersect(msmc_out, (max(relativeCCR)/2)/plt.ylim()[1])

plt.vlines(split, plt.ylim()[0], plt.ylim()[1], color = "black", linestyle='dashed', linewidth = 0.5, label = "50% rCCR")
plt.annotate(" {:.1e}".format(split), (split, 1e4))
plt.xlabel("Estimated split time is " + str(round(split/1000)) + " kya")

plt.legend()
plt.savefig("rCCR_pardinoides_oncilla_consensus.pdf")

print(split) #Print out the time when relativeCCR=0.5
