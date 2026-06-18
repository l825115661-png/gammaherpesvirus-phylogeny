#!/bin/bash

mkdir -p results/alignments

for f in results/homology_groups/*_42.fasta
do
    base=$(basename "$f" .fasta)

    mafft --auto "$f" > results/alignments/${base}_aligned.fasta
done
