# Encoding: utf8

# This sript will assess the directon space of the provided proteins (ids).

import os
import sys
import pandas as pd

from traverse_strand import traverse_strand
from directons_id import directons_id
from directon_sizes import directon_sizes

# ref_geno_dir = '/home/danielc/projects/Gussov_2020_ML/test/genomes'
ref_geno_dir = '/home/dani/Desktop/papers/Gussov et al 2020/Acrs_ML/test/genomes'
#test_ids_file = '/home/danielc/projects/Gussov_2020_ML/test/test_ids.txt'
test_ids_file = '/home/dani/Desktop/papers/Gussov et al 2020/Acrs_ML/test/test_ids.txt'
#outdir       = '/home/danielc/projects/Gussov_2020_ML/test/directons'


def get_directons(infile, genomes_dir): # outdir, outfile):
    ids = [line.strip() for line in open(infile).readlines()]

    # Identify the genomes where proteins belong to
    genomes_sample = ['.'.join(id.replace('fig|','').split('.')[:2]) for id in ids]
    genomes_sample = list(set(genomes_sample))
    #print(genomes_sample)

    # Initialize dictionary to store the relation genome-proteins
    genomes_dict = {genome:[] for genome in genomes_sample}
    #print(genomes_dict)

    # iterate through ids to store into genomes
    for id in ids:
        genome = '.'.join(id.replace('fig|','').split('.')[:2])
        genomes_dict[genome].append(id)

    #print(genomes_dict)

    # iniatialize a dict to contain the directons for ALL the proteins
    all_directons = dict()

    # read features table
    for genome, proteins in genomes_dict.items():
        table = pd.read_csv(genomes_dir + '/' + genome + '/' + genome + '.PATRIC.features.tab',
        sep='\t')
        # separate positive and negative strands
        strand_pos = table[(table.strand == '+') & (table.feature_type == 'CDS')]
        strand_neg = table[(table.strand == '-') & (table.feature_type == 'CDS')]

        # iterate through both strands
        directons_neg = traverse_strand(strand_neg, proteins)
        directons_pos = traverse_strand(strand_pos, proteins)

        if directons_neg:
            all_directons.update(directons_neg)

        if directons_pos:
            all_directons.update(directons_pos)

    # add an identifier to each directon
    all_directons_id = directons_id(all_directons)

    # add size measures of the directons
    directon_sizes(all_directons_id, genomes_dir)










get_directons(test_ids_file, ref_geno_dir)
