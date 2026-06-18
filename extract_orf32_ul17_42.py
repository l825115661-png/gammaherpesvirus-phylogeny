from Bio import SeqIO
from pathlib import Path

ids = set()

with open("orf32_ul17_ids.txt") as f:
    for line in f:
        ids.add(line.strip())

records = []

for record in SeqIO.parse("all_gammaherpes_proteins.fasta", "fasta"):
    if record.id in ids:
        records.append(record)

print(f"Found {len(records)} sequences")

output_file = Path("results/homology_groups/orf32_ul17_42.fasta")
output_file.parent.mkdir(parents=True, exist_ok=True)

SeqIO.write(records, output_file, "fasta")

print(f"Saved to {output_file}")
