from pathlib import Path
from Bio import SeqIO
import requests
import csv
import time

protein_dir = Path("protein")
output_dir = Path("results")
output_dir.mkdir(exist_ok=True)

out_csv = output_dir / "viro3d_structure_summary.csv"

rows = []

for fasta_file in protein_dir.glob("*_proteins.fasta"):
    virus = fasta_file.stem.replace("_proteins", "")
    print(f"Processing {virus}...")

    for record in SeqIO.parse(fasta_file, "fasta"):
        genbank_id = record.id

        url = "https://viro3d.cvr.gla.ac.uk/api/proteins/genbank_id/"
        params = {"qualifier": genbank_id}

        try:
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            rows.append({
                "virus": virus,
                "genbank_id": genbank_id,
                "found": "error",
                "count": "",
                "gene": "",
                "product": "",
                "pLDDT": "",
                "pTM": "",
                "error": str(e)
            })
            continue

        count = data.get("count", 0)
        structures = data.get("protein_structures", [])

        if count > 0 and structures:
            s = structures[0]
            rows.append({
                "virus": virus,
                "genbank_id": genbank_id,
                "found": "yes",
                "count": count,
                "gene": s.get("gene", ""),
                "product": s.get("product", ""),
                "pLDDT": s.get("colabfold_json_pLDDT", ""),
                "pTM": s.get("colabfold_json_pTM", ""),
                "error": ""
            })
        else:
            rows.append({
                "virus": virus,
                "genbank_id": genbank_id,
                "found": "no",
                "count": 0,
                "gene": "",
                "product": "",
                "pLDDT": "",
                "pTM": "",
                "error": ""
            })

        time.sleep(0.1)

with open(out_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "virus", "genbank_id", "found", "count",
        "gene", "product", "pLDDT", "pTM", "error"
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Done. Saved results to {out_csv}")
print(f"Total proteins checked: {len(rows)}")