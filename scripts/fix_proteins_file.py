#!/usr/bin/env python

from Bio import SeqIO
import os
import argparse
from pathlib import Path

###
def parse_args():
    parser = argparse.ArgumentParser(description='Parses a PATRIC protein file '
                                                    'to retain on the id')

    requiredArgs = parser.add_argument_group("required arguments")
    requiredArgs.add_argument('-i', '--input-file',
                              dest='ifile',
                              type=lambda p: Path(p).resolve(strict=True),
                              required=True,
                              help=""
                              )
    requiredArgs.add_argument('-o', '--parsed-file',
                              dest='ofile',
                              type=lambda p: Path(p).resolve(),
                              required=True,
                              help="")
    requiredArgs.add_argument('-lcl', '--lcl-files',
                              dest='lcl',
                              type=lambda p: Path(p).resolve(),
                              required=True,
                              help="File to save files where 'lcl| were detected'")



    return parser.parse_args()

###
def parse_fasta(ifile, ofile, lcl):
    with open(ifile, "r") as handle:
        seqs = list()
        for record in SeqIO.parse(handle, "fasta"):
            # change the whole header to contain only the first id
            record.description = record.id

            # Check lcl presence
            if "lcl|" in record.id:
                os.system("touch {}".format(lcl))
            else:
                seqs.append(record)

    SeqIO.write(seqs, ofile, "fasta")


### MAIN ###


args = parse_args()
parse_fasta(args.ifile, args.ofile, args.lcl)
