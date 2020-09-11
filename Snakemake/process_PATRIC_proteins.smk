configfile: 'config/config.yaml'

import glob, os, time

start = time.time()
genomes = [os.path.basename(file) for file in glob.glob(config["genomes_folder"]+ "/*")]
end = time.time()

print('{} seconds to list genomes'.format(end-start))


rule all:
    input:
        expand(config["fixed_proteins_folder"] + "/{genome}.PATRIC.fixed.faa", genome=genomes),


rule create_lcl_folder:
    input: config["fixed_proteins_folder"]
    output: directory(config["lcl_folder"])
    shell:
        "mkdir -p {output}"

rule fix_fasta:
    input:
        fin = config["genomes_folder"] + "/{genome}/{genome}.PATRIC.faa",
        dir = directory(config["lcl_folder"])
    output:
        fout = config["fixed_proteins_folder"] + "/{genome}.PATRIC.fixed.faa",
    params:
        lclfolder = directory(config["lcl_folder"]),
        lcl = config["lcl_folder"] + "/{genome}.lcl"
    shell:
        "python ../scripts/fix_proteins_file.py "
        "-i {input.fin} "
        "-o {output.fout} "
        "-lcl {params.lcl}"
