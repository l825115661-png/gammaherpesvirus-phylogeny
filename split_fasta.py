from pathlib import Path
from Bio import SeqIO

input_dir = Path("protein")

for fasta_file in input_dir.glob("*_proteins.fasta"):

    virus_name = fasta_file.stem.replace("_proteins", "")

    output_dir = input_dir / virus_name
    output_dir.mkdir(exist_ok=True)

    count = 0

    for record in SeqIO.parse(fasta_file, "fasta"):

        protein_id = record.id.split()[0]

        output_file = output_dir / f"{protein_id}.fasta"

        SeqIO.write(record, output_file, "fasta")

        count += 1

    print(f"{virus_name}: {count} proteins")