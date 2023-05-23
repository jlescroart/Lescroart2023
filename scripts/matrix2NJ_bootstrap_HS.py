### Code from Hannes Svardal received on 14MAY2021.
### Additions by Jonas Lescroart on 09SEP21 and 22MAY23.
### Computes neighborjoining tree from pairwaise distance matrix in python, with bootstrapping.
### To import functions from this file to a python environment: from matrix2NJ_bootstrap_HS.py import *

### Environment dependencies
# $ conda install ete3
# $ conda install dendropy
# $ conda install scikit-bio
# $ git clone https://github.com/feilchenfeldt/pypopgen3.git

### Python modules
import pandas as pd
import copy
import skbio
import numpy as np
import sys
import io
#sys.path.append('/media/labgenoma4/DATAPART4/jonasl/bin/') # Do only once
from pypopgen3.modules import treetools


### To make a NJ tree in Newick string from a csv file with a pairwise distance matrix:

csv_matrix = pd.read_csv(infile_csv, sep = ",", index_col = 0)
distance_matrix = skbio.DistanceMatrix(csv_matrix, ids=sample_names) # converts to distance matrix format used by skbio
nj_newick = skbio.nj(distance_matrix, result_constructor=str)


### To make a NJ tree with bootstrapping support:

### Load functions
def is_supported(node, test_tree):
    leaves = node.get_leaf_names()
    b_node = test_tree.get_common_ancestor(leaves)
    b_leaves = b_node.get_leaf_names()
    if set(leaves) != set(b_leaves):
        return False
    else:
        return True

def get_bootstrap_support(real_tree, pwd_window, n_bootstrap_samples, outgroup):
    support_dic = {}
    support_tree = copy.deepcopy(real_tree)
    n_windows = pwd_window.shape[1]
    
    for node in support_tree.iter_descendants():
        if not node.is_leaf():
            setattr(node, 'n_support', 0)

    for i in range(n_bootstrap_samples):
        t = np.random.choice(n_windows, size=n_windows )
        sample = pwd_window.iloc[:, t]
        sample_pwd = sample.sum(axis=1).unstack() 
        distance_matrix = skbio.DistanceMatrix(sample_pwd, ids=sample_pwd.index) # converts to distance matrix format used by skbio
        nj_newick = skbio.nj(distance_matrix, result_constructor=str) # computes a neighbour-joining tree and outpus a newick string
        test_tree = treetools.HsTree(nj_newick) # convert tree to an object class designed by Hannes Svardal in the package pypopgen3
        test_tree.set_outgroup(outgroup,end_at_present=False)
           
        for node in support_tree.iter_descendants():
            if not node.is_leaf():
                supported = is_supported(node, test_tree)
                node.n_support += int(supported)

    for node in support_tree.iter_descendants():
        if not node.is_leaf():
            setattr(node, 'pct_support', 100*node.n_support/n_bootstrap_samples)
            support_dic.update({node.get_name():node.pct_support})

    support_s = pd.Series(support_dic)
    support_s.name = "Percentage bootstrap support"
    return support_tree, support_s

### Open csv files from file with the csv filenames
with open("/media/../filenames.txt", "r") as filenames:
    pwd_files = filenames.read().splitlines() # pwd short for pairwise distance
pwd_window = []
for file in pwd_files:
    df = pd.read_csv(file, index_col=0)
    s = df.stack()
    pwd_window.append(s)
pwd_window = pd.concat(pwd_window, axis=1)

# Apply bootstrapping. If the windows have different accessible sizes this should be the weighted mean rather than the mean
sum_pwd = pwd_window.mean(axis=1).unstack()
outgroup = 'Puma_concolor'
distance_matrix = skbio.DistanceMatrix(sum_pwd, ids=sum_pwd.index)
nj_newick = skbio.nj(distance_matrix, result_constructor=str)
nj_tree = treetools.HsTree(nj_newick)
nj_tree.set_outgroup(outgroup,end_at_present=False) # Setting an outgroup should not really make a difference

support_tree, support_s = get_bootstrap_support(nj_tree, pwd_window, n_bootstrap_samples=1000, outgroup=outgroup)

# Print to file
with open("/media/labgenoma4/DATAPART4/jonasl/sandbox/nj_bootstrap/sum_pairwise_pi_mLynCan_repeatmasked_bs.txt", "w") as f:
    print(support_tree, file = f)
    print(support_s, file = f)
	