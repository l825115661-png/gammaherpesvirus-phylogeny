#!/bin/bash

mkdir -p results/trees

for f in results/alignments/*_aligned.fasta
do
    base=$(basename "$f" _aligned.fasta)

    VeryFastTree -wag -gamma "$f" > results/trees/${base}.tree
done
