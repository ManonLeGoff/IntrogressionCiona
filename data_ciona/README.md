# Haplotagging pipeline

This repository contains a bioinformatics pipeline to analyse **haplotagging sequencing data**, following the **Harpy pipeline** (P. Dimens, 2025).

---

## Pipeline overview

1. **Data check**
   - Demultiplexing
      → [`data_check/demultiplex.sh`](data_check/demultiplex.sh)
   - Preflight checks
      → [`data_check/preflight.sh`](data_check/preflight.sh)
   - Quality control
      → [`data_check/qc.sh`](data_check/qc.sh) 

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

----

# Introgression time and selection inference 

- Introgression time (T) and selection coefficient were calculated using Deterministic Adaptive Introgression Model (DAIM). All script are available in https://github.com/vlshchur/DAIM. 

---

## Build DAIM grid
- Rscript build_daim_grid.R
→ [`DAIM/build_daim_grid.sh`](DAIM/build_daim_grid.sh)

---

## T and s inference
- Rscript infer_daim_T_s_surface.R
→ [`DAIM/infer_daim_T_s_surface.sh`](DAIM/infer_daim_T_s_surface.sh)

---

## Citation

If you use this pipeline, please cite:
[https://github.com/vlshchur/DAIM](https://academic.oup.com/g3journal/article/10/10/3663/6053540)




