#!/usr/bin/env python3

from pathlib import Path
from Bio import SeqIO

protein_dir = Path("protein")
output_file = Path("results/homology_groups/glycoprotein_b_42.fasta")

keywords = [
    "glycoprotein B",
    "glycoprotein b",
    "gB",
    "BALF4",
    "ORF8",
    "UL27"
]

records = []

for fasta_file in sorted(protein_dir.glob("*_proteins.fasta")):
    virus_name = fasta_file.stem.replace("_proteins", "")
    found = False

    for record in SeqIO.parse(fasta_file, "fasta"):
        header = record.description

        if any(keyword.lower() in header.lower() for keyword in keywords):
            record.id = virus_name
            record.name = virus_name
            record.description = ""

            records.append(record)
            found = True
            break

    if not found:
        print(f"No polycoprotein B found: {fasta_file}")

output_file.parent.mkdir(parents=True, exist_ok=True)

SeqIO.write(records, output_file, "fasta")

print(f"\nFound {len(records)} sequences")
print(f"Saved to {output_file}")
