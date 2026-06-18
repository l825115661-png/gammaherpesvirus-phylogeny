from Bio import SeqIO
from pathlib import Path

ids = set()

with open("bglf5_ids.txt") as f:
    for line in f:
        ids.add(line.strip())

records = []

for record in SeqIO.parse("all_gammaherpes_proteins.fasta", "fasta"):
    accession = record.id
    if accession in ids:
        records.append(record)

print(f"Found {len(records)} sequences")

output_file = Path("results/homology_groups/bglf5_42.fasta")
output_file.parent.mkdir(parents=True, exist_ok=True)

SeqIO.write(records, output_file, "fasta")

print(f"Saved to {output_file}")

