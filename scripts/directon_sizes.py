# Encoding: utf8

def directon_sizes(directons, genomes_dir):

    # iterate through directon_ids since some protein share directon_id
    ids = list(set([directon[1] for directon in directons.values()]))

    # iterate through the directons
    for id in ids:
        genome = 
