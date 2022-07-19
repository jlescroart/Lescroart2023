#!/bin/bash

# Script written by Gabriel Renaud
# Downloaded from https://github.com/grenaud/mappability_snpable.git
#usage: bash snpable.bash [ref genome] [path to dir to seqbility]
#seqbility is from lh3_misc from https://github.com/lh3/misc
# /storage/software/lh3_misc/seq/seqbility/
#example:
# bash snpable.bash hg38.fa /storage/software/lh3_misc/seq/seqbility/
# requires in path:
#    bwa
#    samtools
#    gzip
#    bgzip
#    bedtools

REFGENOME=$1

DIRSEQBILITY=$2
REFGENOMEFAI=$1".fai"

bwa index $REFGENOME
samtools index $REFGENOME

bwa aln -t 10 -R 1000000 -O 3 -E 3 $REFGENOME  <($DIRSEQBILITY/splitfa $REFGENOME 35 ) |bwa samse $REFGENOME /dev/stdin <($DIRSEQBILITY/splitfa $REFGENOME 35 ) | $DIRSEQBILITY/gen_raw_mask.pl |gzip > rawMask_35.fa.gz

$DIRSEQBILITY/gen_mask -l 35 -r 0.99 <(zcat rawMask_35.fa.gz ) | $DIRSEQBILITY/apply_mask_l /dev/stdin <(cat $REFGENOMEFAI  |awk '{ for(i=1;i<$2;i++){ print $1"\t"i;}  }')  |awk '{print $1"\t"($2-1)"\t"$2}' |  bedtools merge  |bgzip -c > mappable_99.bed.gz

tabix -p bed mappable_99.bed.gz
