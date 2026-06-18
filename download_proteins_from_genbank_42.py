import pandas as pd
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import os
import time
import re

Entrez.email = "你的邮箱@example.com"

df = pd.read_excel("data/gammaherpesviruses_all.xlsx.xlsx")

os.makedirs("protein", exist_ok=True)

def clean_virus_name(name):
    name = str(name).split(";")[0].strip()
    name = re.sub(r"[^A-Za-z0-9_]+", "_", name)
    return name

for _, row in df.iterrows():
    virus = clean_virus_name(row["Virus name abbreviation(s)"])
    acc = str(row["Virus GENBANK accession"]).strip()

    outfile = f"protein/{virus}_proteins.fasta"

    if os.path.exists(outfile):
        print(f"Skipping existing: {outfile}")
        continue

    print(f"Downloading GenBank and extracting proteins: {virus} {acc}")

    try:
        handle = Entrez.efetch(
            db="nucleotide",
            id=acc,
            rettype="gb",
            retmode="text"
        )
        record = SeqIO.read(handle, "genbank")
        handle.close()

        proteins = []

        for feature in record.features:
            if feature.type == "CDS" and "translation" in feature.qualifiers:
                protein_seq = feature.qualifiers["translation"][0]
                protein_id = feature.qualifiers.get("protein_id", ["no_protein_id"])[0]
                gene = feature.qualifiers.get("gene", [""])[0]
                product = feature.qualifiers.get("product", ["unknown"])[0]

                header = f"{protein_id} {virus} {gene} {product}"

                proteins.append(
                    SeqRecord(
                        Seq(protein_seq),
                        id=protein_id,
                        description=header
                    )
                )

        SeqIO.write(proteins, outfile, "fasta")
        print(f"Saved {len(proteins)} proteins to {outfile}")

        time.sleep(0.5)

    except Exception as e:
        print(f"FAILED {virus} {acc}: {e}")
