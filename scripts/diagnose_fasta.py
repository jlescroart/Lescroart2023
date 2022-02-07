#!/usr/bin/env python

"""
DESCRIPTION
Script to check fasta files for ACGT-content.
Maybe I'll add graphs and other parameters later.

USAGE
python diagnose_fasta.py FILENAME1.fasta FILENAME2.fasta ...

Version: 06 November 2020
Author: Jonas Lescroart
"""

#import modules
from Bio import SeqIO
import sys
import os
import re
import datetime

if sys.argv[1].endswith(tuple([".fasta", "fa", "fas", "fna"])):
    infiles = sys.argv[1:]
else:
    raise Exception("Invalid input arguments")

outfiles = list()
date = datetime.datetime.now()

for i in range(len(infiles)):
    outfile = infiles[i].split(".")
    if re.match("fasta|fa|fas|fna", outfile[-1]):
        outfile = outfile[:-1]
    outfile = ".".join(outfile) + ".info"
    outfiles.append(outfile)

for i in range(len(infiles)):

    with open(infiles[i], 'r') as handle:
        length_total, a_total, t_total, c_total, g_total, n_total = [0]*6

        with open(outfiles[i], 'w') as output:
            sequencelvl_info = ""
            sequence_ids = []
            for record in SeqIO.parse(handle, 'fasta'):
                sequence_ids.append(record.id)

                length_seq = len(record.seq)
                a_seq = str(record.seq).count("A") + str(record.seq).count("a")
                t_seq = str(record.seq).count("T") + str(record.seq).count("t")
                c_seq = str(record.seq).count("C") + str(record.seq).count("c")
                g_seq = str(record.seq).count("G") + str(record.seq).count("g")
                n_seq = str(record.seq).count("N") + str(record.seq).count("n")
                #reverse search for other characters? like - or x
                #also needs a count for iupac characters like Y, R, ...

                length_total += length_seq
                a_total += a_seq
                t_total += t_seq
                c_total += c_seq
                g_total += g_seq
                n_total += n_seq

                sequencelvl_info = (
                sequencelvl_info +
                ">" + record.id + "\nseq length: " + '{:,}'.format(length_seq) +
                "\nATCG-count: " +
                "\nA " + '{:,}'.format(a_seq) + ' {:.0%}'.format(a_seq/length_seq) +
                "\nT " + '{:,}'.format(t_seq) + ' {:.0%}'.format(t_seq/length_seq) +
                "\nC " + '{:,}'.format(c_seq) + ' {:.0%}'.format(c_seq/length_seq) +
                "\nG " + '{:,}'.format(g_seq) + ' {:.0%}'.format(g_seq/length_seq) +
                "\nN " + '{:,}'.format(n_seq) + ' {:.0%}'.format(n_seq/length_seq) + "\n\n"
                )

            output.write(
            "Diagnostics file for " + infiles[i] + " generated on " +
            date.strftime("%d %B %Y.") + "\n\n" +
            "Total length: " + '{:,}'.format(length_total) +
            "\nOverall ATCG-count: " +
            "\nA " + '{:,}'.format(a_total) + ' {:.0%}'.format(a_total/length_total) +
            "\nT " + '{:,}'.format(t_total) + ' {:.0%}'.format(t_total/length_total) +
            "\nC " + '{:,}'.format(c_total) + ' {:.0%}'.format(c_total/length_total) +
            "\nG " + '{:,}'.format(g_total) + ' {:.0%}'.format(g_total/length_total) +
            "\nN " + '{:,}'.format(n_total) + ' {:.0%}'.format(n_total/length_total) + "\n\n"
            + "Number of sequences: " + str(len(sequence_ids)) + "\n"
            + str(sequence_ids) + "\n\n"
            + sequencelvl_info
            )

        output.close()

        print(
        infiles[i] +
        "\nTotal length: " + '{:,}'.format(length_total) +
        "\nOverall ATCG-count: " +
        "\nA " + '{:,}'.format(a_total) + ' {:.0%}'.format(a_total/length_total) +
        "\nT " + '{:,}'.format(t_total) + ' {:.0%}'.format(t_total/length_total) +
        "\nC " + '{:,}'.format(c_total) + ' {:.0%}'.format(c_total/length_total) +
        "\nG " + '{:,}'.format(g_total) + ' {:.0%}'.format(g_total/length_total) +
        "\nN " + '{:,}'.format(n_total) + ' {:.0%}'.format(n_total/length_total) + "\n"
        + "Number of sequences: " + str(len(sequence_ids)) + "\n"
        )
