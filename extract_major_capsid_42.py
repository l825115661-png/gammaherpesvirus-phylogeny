from Bio import SeqIO
import glob
import os

keywords = [
    "major capsid",
    "BcLF1",
    "ORF25",
    "UL19",
    "VP5"
]

selected = []

for fasta in glob.glob("protein/*_proteins.fasta"):

    candidates = []

    for record in SeqIO.parse(fasta, "fasta"):

        desc = record.description.lower()

        if any(k.lower() in desc for k in keywords):
            candidates.append(record)

    if len(candidates) == 0:
        print(f"No major capsid found: {fasta}")

    elif len(candidates) == 1:
        selected.append(candidates[0])

    else:
        major = [
            r for r in candidates
            if "major capsid" in r.description.lower()
        ]

        if major:
            selected.append(major[0])
        else:
            selected.append(candidates[0])

os.makedirs("results/homology_groups", exist_ok=True)

out = "results/homology_groups/major_capsid_42.fasta"

SeqIO.write(selected, out, "fasta")

print(f"\nFound {len(selected)} sequences")
print(f"Saved to {out}")
