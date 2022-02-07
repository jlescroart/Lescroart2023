#!/usr/bin/env python

"""
DESCRIPTION 
Concatenate each genome to generate alignment window blocks using a *.list file or list of genomes
List file or list of arguments: The absolute path for the genomes in order, one per line

USAGE
createWindow_aln_JL.py DATASETXXX.list
Or: createWindow_aln_JL.py genome1.fasta genome2.fasta ...

AUTHOR AND CHANGE LOG
Written by: Henrique V Figueiro - henriquevf@gmail.com
Adapted by Jonas Lescroart on 04 October 2020
Following changes were made:
1/ number of input genomes is determined from list file rather than hardcoded in script;
2/ input genomes can be given from command line as alternative to list file;
3/ output txt file is produced listing all the names of output alignment files;
4/ bunch of smaller changes
"""

from Bio import SeqIO
import sys
import os

#Take arguments, either list file with genomes or genomes directly

if sys.argv[1].endswith(tuple([".txt", ".list"])):
    dataset = open(sys.argv[1], 'r')
    lines = dataset.read().splitlines()
elif sys.argv[1].endswith(tuple([".fasta", "fa", "fas", "fna"])):
    lines = sys.argv[1:]
else:
    raise Exception("Invalid input arguments")

#Create windows folder

if not os.path.exists(os.getcwd() + '/windows/'):
    os.makedirs(os.getcwd() + '/windows/')

chr_dir = os.getcwd() + '/windows/'

#Read genome filenames and get spp names

names = list()

for i in range(len(lines)):
    line = lines[i]
    name = str(('.').join(line.split('/')[-1].split('.')[:-1]))
    names.append(name)
    print(names[i])

#Create each window fasta file and append the subsequent genomes

for i in range(len(lines)):
    with open(str(lines[i].rstrip()), 'r') as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            with open(chr_dir + record.id + ".fasta", 'a') as out_file:
                seq_name = str('>' + names[i])
                seq =  str(record.seq)
                out_file.write(seq_name + '\n' + seq + '\n')
            out_file.close()
            if i == 0: # produce txt file with names of output files for downstream processing
                with open("filenames.txt", 'a') as out_file:
                    out_file.write(record.id + ".fasta" + '\n')
                out_file.close()
