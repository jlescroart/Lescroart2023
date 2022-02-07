import sys

filename=sys.argv[1]

with open(filename) as f:
    lines = f.readlines()
    for i in lines:
        i=i.split()
        sum_values=float(i[0]) + float(i[1])
        het=float(i[1])/sum_values
        sample=filename.split("/")[-1][:-7]
        print(str('{:.15f}'.format(het))+"\t"+sample)
