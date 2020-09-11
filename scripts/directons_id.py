# Encoding: utf8


def directons_id(raw_directons):
    proteins       = sorted(raw_directons.keys())

    # eacht directon list to strin so I can do set() later
    all_directons = [(";").join(directon) for directon in raw_directons.values()]

    uniq_directons = sorted(list(set(all_directons)))
    #print(uniq_directons)

    i = 1
    ids = dict()
    for directon in uniq_directons:
        ids[directon] = "directon-{}".format(i)
        i += 1

    table = dict()
    for protein in proteins:
        table[protein] = [';'.join(raw_directons[protein]), ids[';'.join(raw_directons[protein])]]

    return table
