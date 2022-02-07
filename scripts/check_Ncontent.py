#!/usr/bin/env python

"""
DESCRIPTION
This python script is (originally) part of the dfoil pipeline outlined in 'Dfoil_pipeline.pptx'.
Script to turn 'uninformative' windows into complete strings of N's so that they are completely masked.
After masking with WindowMasker (and replacing lowercase nucl. with uppercase N's) it seems appropriate to
remove windows with huge amounts of N from the analysis,
but cutting them out would alter the length of the genome, so it's better to mask them completely
to prevent a false positive signal of hybridization.
If this is not done, dfoil can mark a window as introgressed 
even when the information content (number of nucl., compared to number of N's) is really low (eg when 9 in 10 bases are N).

The cut-off value refers to the percentage of [ACGT] that is demanded.
As soon as one sequence (taxon) in a fasta has too many N's, all sequences (taxa) in that fasta are replaced by N's

USAGE
python check_Ncontent.py [FULL DIRECTORY] [CUT-OFF]
e.g. python check_Ncontent.py /home/jlescroa/eclipse-workspace/PUCRS/windows 70
Directory is the folder containing the fastas and must be specified.
Newly created directory will be at the height of /home/jlescroa/eclipse-workspace/PUCRS/ (in this example).
Cut-off value is given in as percentage from 0 to 100 and is optional, default is 50.

Author: Jonas Lescroart

UPDATES
11JAN21: included IUPAC ambiguity codes in assertion of function 'informative'.
03MAR21: additional output: list with filenames of informative windows, for input in RAxML
"""

#import modules
import sys
import os

#assertions about directory
assert len(sys.argv) > 1, "Please provide a full directory as first argument."
assert os.path.isdir(sys.argv[1]), "Please make sure the first argument is a full directory."
os.chdir(sys.argv[1])
print("Folder is: " + sys.argv[1])

#assertions about cut-off
if len(sys.argv) == 3:
    assert float(sys.argv[2])
    assert int(sys.argv[2]) <= 100 and int(sys.argv[2]) >= 0, "Cut-off value must be an int between 0 and 100"
    temp_cutoff = int(sys.argv[2])
    print("Cut-off is set to " + str(temp_cutoff) + " percent")
else:
    temp_cutoff = 50
    print("Cut-off is " + str(temp_cutoff) + " percent by default.")

cutoff_str = str(int(temp_cutoff))

#load functions    
def informative(sequence, cutoff = 50):
    count = 0
    for nucl in sequence:
        assert nucl in "ACGTMRWSYKVHDBN-", "Sequence contains symbols other than A,T,C,G, IUPAC ambiguity codes or N, -"
        if nucl == "N" or nucl == "-":
            count += 1
    count -= 0.00000000001
    if count < ((1 - (float(cutoff) / float(100))) * len(sequence)):
        flag = True
    else:
        flag = False
    return flag

def Nserter(sequence):
    length = len(sequence)
    new_sequence = "N" * length
    return new_sequence

#create new directory
new_dir = os.getcwd().split("/")
new_dir[-2] = new_dir[-2] + cutoff_str
new_dir = ("/").join(new_dir)

if not os.path.exists(new_dir):
    os.makedirs(new_dir)

#set initial values
total_fastas = 0
uninformative_fastas = 0
informative_filenames = []

#iterate through .fasta and .fa files
for filename in os.listdir(str(sys.argv[1])):
    if filename.endswith(".fa") or filename.endswith(".fasta"): 
        
        #determine whether window is informative
        total_fastas += 1
        window = open(filename, "r")
        window_content = window.readlines()
        good_window = True

        for line in window_content:
            if line[0] != ">" and line[0] in "ACGTN" and good_window == True:
                good_window = informative(line.rstrip(), temp_cutoff)
            else:
                pass
        window.close()

        #creat new file
        window = open(new_dir +"/" + filename, "w")
        
        #if not informative, transform in N's
        if not good_window:
            uninformative_fastas += 1
            count = 0
            for line in window_content:
                if line[0] != ">" and line[0] in "ACGTN":
                    window_content[count] = (Nserter(line.rstrip()) + "\n")
                else:
                    pass
                count +=1 

        elif good_window:
            informative_filenames.append(filename)
        
        for line in window_content:
            window.write(line)
        window.close()
        
    else:
        None    

#output summary statements
sum_dir = new_dir.split("/")
del sum_dir[-1]
sum_dir = ("/").join(sum_dir)

summary = open(sum_dir + "/summary_" + cutoff_str + ".txt", "w")
summary.write("Start folder is: " + sys.argv[1] + "\n" + 
              "Cut-off: " + str(temp_cutoff) + "\n" +
              "Total number of files processed: " + str(total_fastas) + "\n" + 
              "Folder contained " + str((float(uninformative_fastas) / float(total_fastas)) * 100) + "% uninformative files." + "\n" + 
              "Number of files converted to N-strings: " + str(uninformative_fastas)
              )
summary.close()

#output list with filenames of informative windows
filenames = open(sum_dir + "/filenames_informative.txt", "w")
informative_filenames = map(lambda x:x + '\n', informative_filenames)
filenames.writelines(informative_filenames)
filenames.close()
