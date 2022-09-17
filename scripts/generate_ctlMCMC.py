#!/usr/bin/env python

"""
DESCRIPTION
python script to generate a control file (.ctl) needed for MCMCTree included in PAML v4.9

USAGE
python generate_ctlMCMC.py --phy [infile.phy] --nwk [infile.nwk] --ctl [outfile.ctl]
Provide absolute paths.
Run script with -h for help.

AUTHOR
Jonas Lescroart
17SEP22
"""

#import modules
import argparse

#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--phy', help="Absolute path to phylip file", type= str)
parser.add_argument('--nwk', help="Absolute path to corresponding tree file", type= str)
parser.add_argument('--ctl', help="Absolute path to output control file", type= str)
args = parser.parse_args()

#assertions
assert args.phy.endswith(tuple([".phy", ".phylip"])), "usage: python generate_ctlMCMC.py [-h] [--phy PHY] [--nwk NWK] [--ctl CTL]"
assert args.nwk, "usage: python generate_ctlMCMC.py [-h] [--phy PHY] [--nwk NWK] [--ctl CTL]"
assert args.ctl, "usage: python generate_ctlMCMC.py [-h] [--phy PHY] [--nwk NWK] [--ctl CTL]"

#write control file
with open(args.ctl, "w") as file:
    file.write("""          seed =  -1
       seqfile = """+args.phy+"""
      treefile = """+args.nwk+"""
       outfile = """+(".").join(args.ctl.split(".")[:-1])+"""_out.txt
      mcmcfile = """+(".").join(args.ctl.split(".")[:-1])+"""_mcmc.txt

         ndata = 1  * number of loci
       seqtype = 0  * 0: nucleotides; 1:codons; 2:AAs
       usedata = 1    * 0: no data; 1:seq like; 2:use in.BV; 3: out.BV

         clock = 1    * 1: global clock; 2: independent rates; 3: correlated rates.
       RootAge = '>9.80<9.82'  * boundaries for root age, here based on the 9.81 MYA Puma-Ocelot from Li et al. (2016)
         model = 0    * 0:JC69, 1:K80, 2:F81, 3:F84, 4:HKY85, maybe 7:GTR exists
         alpha = 0    * alpha for gamma rates at sites
         ncatG = 5    * No. categories in discrete gamma

     cleandata = 0    * remove sites with ambiguity data (1:yes, 0:no)?

       BDparas = 1 1 0.1    * birth, death, sampling
   kappa_gamma = 6 2      * gamma prior for kappa
   alpha_gamma = 1 1      * gamma prior for alpha

   rgene_gamma = 10 1000   * gamma prior for overall rates for genes. Together with the chosen timeunit in the RootAge, here 1 my, this determines your mutation rate mu, like so: mu = (10/1000)/1000000 = 1e-8
* sigma2_gamma = 1 10    * gamma prior for sigma^2   (only for clock=2 or 3)

*     finetune = 1: 0.1  0.1  0.1  0.01 .5  * auto (0 or 1) : times, musigma2, rates, mixing, paras, FossilErr [DEPRECATED]

         print = 1
        burnin = 500
      sampfreq = 1
*   checkpoint = 0  * 0: nothing; 1 : save; 2: resume
       nsample = 2000""")

