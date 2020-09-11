# Encoding: utf8

import pandas as pd

def traverse_strand(df, proteins):
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
