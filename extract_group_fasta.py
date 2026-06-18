from pathlib import Path
from Bio import SeqIO

accession_file = "results/homology_groups/rnr_small_accessions.txt"
fasta_files = list(Path("protein").rglob("*.fasta"))
output_file = "results/homology_groups/rnr_small.fasta"

wanted = set(Path(accession_file).read_text().splitlines())

records = []
seen = set()

for fasta in fasta_files:
    for record in SeqIO.parse(fasta, "fasta"):
        record_id = record.id.split()[0]

        if record_id in wanted and record_id not in seen:
            records.append(record)
            seen.add(record_id)

SeqIO.write(records, output_file, "fasta")

print(f"Found {len(records)} unique sequences")
print(f"Saved to {output_file}")

missing = wanted - seen
if missing:
    print("Missing accessions:")
    for m in sorted(missing):
        print(m)
