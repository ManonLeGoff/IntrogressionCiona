# Haplotagging pipeline

This repository contains a bioinformatics pipeline to analyse **haplotagging sequencing data**, following the **Harpy pipeline** (P. Dimens, 2025).

---

## Pipeline overview

1. **Data check**
   - Demultiplexing
   - Preflight checks
   - Quality control  
   → [`data_check.sh`](data_check.sh)

2. **Read alignment**
   - Alignment to reference genome using BWA  
   → [`align/align.sh`](align/align.sh)

3. **Singleton removal**
   - Removal of singletons (reads present alone on a molecule)
   - Snakemake rule  
   → [`align/singletons.sh`](align/singletons.sh)

4. **Variant calling**
   - SNP calling using `harpy snp mpileup`  
   → [`snp_calling/snp_calling.sh`](snp_calling/snp_calling.sh)

5. **Phasing**
   - Variant filtering
   - Phasing with hapcut2 and Shapeit4  
   → [`phasing.sh`](phasing.sh)

---

## Requirements
> All commands were executed in a Conda environment.
Main tools used in this pipeline:
- `harpy`
- `samtools`
- `bcftools`
- `bwa`
- `shapeit4`

---

## Notes
- Singleton removal rule was adapted by **B. Penaud** from the original Harpy implementation.

---

## Citation

If you use this pipeline, please cite:
- **Harpy** (P. Dimens, 2025)
