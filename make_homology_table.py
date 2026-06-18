import pandas as pd

input_file = "results/viro3d_high_confidence_structures.csv"
output_file = "results/homology_candidate_table.csv"

df = pd.read_csv(input_file, header=None)

df.columns = [
    "virus",
    "accession",
    "has_structure",
    "structure_count",
    "gene",
    "product",
    "confidence",
    "plddt",
    "extra"
]

patterns = {
    "Major_capsid": r"major capsid|capsid protein|ORF25|BcLF1",
    "RNR_large": r"ribonucleotide|ribonucleoside|ORF61|BORF2",
    "Helicase_primase": r"helicase|primase|ORF44|ORF56|BSLF1|BBLF4",
}

tables = []

for group, pattern in patterns.items():
    subset = df[
        df["gene"].astype(str).str.contains(pattern, case=False, na=False)
        | df["product"].astype(str).str.contains(pattern, case=False, na=False)
    ].copy()

    subset.insert(0, "homology_group", group)
    tables.append(subset)

out = pd.concat(tables, ignore_index=True)

out = out[
    [
        "homology_group",
        "virus",
        "accession",
        "gene",
        "product",
        "confidence",
        "plddt",
    ]
]

out.to_csv(output_file, index=False)

print(f"Saved: {output_file}")
print(out)
