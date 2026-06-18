import pandas as pd

df = pd.read_csv("results/viro3d_structure_summary.csv")

print("Total proteins checked:", len(df))
print("Proteins with Viro3D hit:", (df["found"] == "yes").sum())
print("Proteins without Viro3D hit:", (df["found"] != "yes").sum())

by_virus = (
    df.groupby("virus")
    .agg(
        total_proteins=("genbank_id", "count"),
        structures_found=("found", lambda x: (x == "yes").sum()),
        mean_pLDDT=("pLDDT", "mean"),
        mean_pTM=("pTM", "mean"),
    )
    .reset_index()
)

by_virus["coverage_percent"] = (
    by_virus["structures_found"] / by_virus["total_proteins"] * 100
).round(1)

by_virus.to_csv("results/viro3d_by_virus_summary.csv", index=False)

high_conf = df[
    (df["found"] == "yes")
    & (df["pLDDT"] >= 70)
    & (df["pTM"] >= 0.5)
]

high_conf.to_csv("results/viro3d_high_confidence_structures.csv", index=False)

print("\nSummary by virus:")
print(by_virus)

print("\nHigh-confidence structures:", len(high_conf))
