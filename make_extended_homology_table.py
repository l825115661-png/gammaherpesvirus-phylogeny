import pandas as pd

input_file = "results/viro3d_high_confidence_structures.csv"
output_file = "results/extended_homology_candidate_table.csv"

df = pd.read_csv(input_file, header=None)

df.columns = [
    "virus",
    "accession",
    "has_structure",
    "structure_count",
    "gene",
    "product",
    "confidence",
    "ptm",
    "extra",
]

patterns = {
    "DNA_polymerase": r"DNA polymerase|BALF5|ORF9",

    "Major_capsid": r"major capsid protein|BcLF1|ORF25",

    "VP23": r"vp23|BDLF1",

    "VP19C": r"VP19C|BORF1",

    "RNR_large": r"large chain|large subunit|BORF2|ORF61",

    "RNR_small": r"small chain|small subunit|BaRF1",

    "Helicase_ATPase": r"ORF44|BSLF1",

    "Helicase_subunitB": r"ORF56|BBLF4",
}

results = []

for group, pattern in patterns.items():
    mask = (
        df["gene"].astype(str).str.contains(pattern, case=False, na=False)
        | df["product"].astype(str).str.contains(pattern, case=False, na=False)
    )

    subset = df.loc[mask].copy()
    subset.insert(0, "homology_group", group)
    results.append(subset)

out = pd.concat(results, ignore_index=True)

out = out[
    [
        "homology_group",
        "virus",
        "accession",
        "gene",
        "product",
        "confidence",
        "ptm",
    ]
]

out.to_csv(output_file, index=False)

print(f"Saved to: {output_file}")
print(out)
