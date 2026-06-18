#!/bin/bash

mmseqs easy-cluster \
all_gammaherpes_proteins.fasta \
gamma_clusters_rerun \
tmp_mmseqs

echo "MMseqs2 clustering finished."
