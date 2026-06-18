from pathlib import Path
import csv

groups = ["dna_polymerase", "rnr_large", "rnr_small"]

indir = Path("results/homology_groups")

for group in groups:
    csv_file = indir / f"{group}.csv"
    fasta_file = indir / f"{group}.fasta"
    out_file = indir / f"{group}_named.fasta"

    mapping = {}
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            # row format: family, virus, accession, gene, product, pLDDT, pTM
            virus = row[1]
            acc = row[2]
            mapping[acc] = virus

    with open(fasta_file) as fin, open(out_file, "w") as fout:
        for line in fin:
            if line.startswith(">"):
                acc = line[1:].split()[0]
                new_name = mapping.get(acc, acc)
                fout.write(f">{new_name}\n")
            else:
                fout.write(line)

    print(f"Saved {out_file}")
