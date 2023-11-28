# Lescroart2023

Archived code for analyses in Lescroart et al. (2023). 

Snakemake code consists of six interlinked pipelines: (1) QC and mapping of raw reads (‘fastq2bam’), (2) assemblage of mitogenomes from raw reads and subsequent phylogenetic analysis (‘fastq2mtdna’), (3, 4) base calling into consensus genomes and a SNP data set (resp. ‘bam2fasta’ and ‘bam2vcf’), (5) phylogenomic analysis (‘phylogeny’), and (6) genomic diversity measures (‘diversity’). For a quick overview of each pipeline, see the associated rulegraphs. Each pipeline comes with its own Conda environment (specs_\*.txt).

### Full citation:

Lescroart, J., Bonilla-Sánchez, A., Napolitano, C., Buitrago-Torres, D. L., Ramírez-Chaves, H. E., Pulido-Santacruz, P., Murphy, W. J., Svardal, H., Eizirik, E. (2023). Extensive phylogenomic discordance and the complex evolutionary history of the Neotropical cat genus *Leopardus*. *Molecular Biology and Evolution*, msad255. doi: [10.1093/molbev/msad255](https://doi.org/10.1093/molbev/msad255).

### Abstract:

Even in the genomics era, the phylogeny of Neotropical small felids comprised in the genus *Leopardus* remains contentious. We used whole-genome resequencing data to construct a time-calibrated consensus phylogeny of this group, quantify phylogenomic discordance, test for interspecies introgression, and assess patterns of genetic diversity and demographic history. We infer that the *Leopardus* radiation started in the Early Pliocene as an initial speciation burst, followed by another in its subgenus *Oncifelis* during the Early Pleistocene. Our findings challenge the long-held notion that ocelot (*Leopardus pardalis*) and margay (*L. wiedii*) are sister species and instead indicate that margay is most closely related to the enigmatic Andean cat (*L. jacobita*), whose whole-genome data are reported here for the first time. In addition, we found that the newly sampled Andean tiger cat (*L. tigrinus pardinoides*) population from Colombia associates closely with Central American tiger cats (*L. tigrinus oncilla*). Genealogical discordance was largely attributable to incomplete lineage sorting, yet was augmented by strong gene flow between ocelot and the ancestral branch of *Oncifelis*, as well as between Geoffroy's cat (*L. geoffroyi*) and southern tiger cat (*L. guttulus*). Contrasting demographic trajectories have led to disparate levels of current genomic diversity, with a nearly tenfold difference in heterozygosity between Andean cat and ocelot, spanning the entire range of variability found in extant felids. Our analyses improved our understanding of the speciation history and diversity patterns in this felid radiation, and highlight the benefits to phylogenomic inference of embracing the many heterogeneous signals scattered across the genome.

Financial support to J. Lescroart was provided by Research Foundation - Flanders under grant agreement N° 1128621N.

### Raw data access:

Raw WGS reads generated for this study can be found on SRA under BioProject accession number [PRJNA985552](https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA985552). 
