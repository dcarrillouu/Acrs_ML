# Encoding: utf8

# This sript will assess the directon space of the provided proteins (ids).

import os
import sys
import pandas as pd

# Path to the genomes folder

# ref_geno_dir = '/home/danielc/projects/Gussov_2020_ML/test/genomes'
ref_geno_dir = '/media/dani/UUI/Gussov_2020_ML/test/genomes'
#test_ids_file = '/home/danielc/projects/Gussov_2020_ML/test/test_ids.txt'
test_ids_file = '/media/dani/UUI/Gussov_2020_ML/test/test_ids.txt'
outdir       = '/home/danielc/projects/Gussov_2020_ML/test/directons'



def check_strand(df, proteins):
    '''
    Function that given the strand iterates it looking for the directons where
    proteins are present
    '''
    contigs = df.accession.tolist()
    starts  = df.start.tolist()
    ends    = df.end.tolist()
    IDs     = df.patric_id.tolist()

    # initialize the directons list and iterate through proteins:
    directons_dict = dict()

    for protein in proteins:
        #print(protein)
        try:
            # define checks for iterations up and down the PATRIC.features.tab
            # CAUTION: start/end on the negative strand follow the same behaviour
            #          than in the positive strand: end > start
            up   = True
            down = True
            directon = [protein]

            i = IDs.index(protein)
            while up:
                diff = starts[i] - ends[i-1]
                if diff <= 100 and contigs[i] == contigs[i-1]:
                    directon.append(IDs[i-1])
                    i -= 1
                else: # stop up iteration
                    up = False

            i = IDs.index(protein)
            while down:
                diff = starts[i+1] - ends[i]
                if diff <= 100 and contigs[i] == contigs[i+1]:
                    directon.append(IDs[i+1])
                    i += 1
                else: # stop up iteration
                    down = False

            directons_dict[protein] = sorted(directon)

        # if the protein is not in this strand
        except ValueError:
            pass

    return directons_dict


TO CONTINUE FROM HERE
def directons_id(raw_directons):
    proteins       = sorted(raw_directons.keys())
    uniq_directons = sorted(raw_directons.values())

    i = 1
    directon_ids = dict()
    for directon in uniq_directons:
        directon_ids[directon] = "directon-{}".format(i)
        i += 1

    table = list()
    for protein in proteins:
        table.append([protein, ';'.join(raw_directon[protein]), directon_ids[raw_directon[protein]]])

    return table



def search_directons(infile, genomes_dir): # outdir, outfile):
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
        directons_neg = check_strand(strand_neg, proteins)
        directons_pos = check_strand(strand_pos, proteins)

        if directons_neg:
            all_directons.update(directons_neg)

        if directons_pos:
            all_directons.update(directons_pos)

    print(directons_id(all_directons))












search_directons(test_ids_file, ref_geno_dir)
