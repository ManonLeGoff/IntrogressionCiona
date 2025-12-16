# Simulation Pipeline – Adaptive Introgression

This repository contains a simulation and analysis pipeline designed to study the relationship between allele frequency and ancestry tract length during adaptive introgression.  
Simulations are performed using SLiM, with downstream processing and analysis in Python and R.

---

## Overview

The pipeline:
1. Simulates adaptive introgression under different migration rates.
2. Extracts ancestry tracts carrying a beneficial allele.
3. Computes correlations between allele frequency and mean tract length.
4. Summarizes results across replicates and produces visualizations.

To limit storage usage, only final summary tables are retained; intermediate ancestry files are deleted.

---

## Pipeline Structure

### Main Steps

For each migration rate and for 10 replicates, the following scripts are executed:

1. **01_run_slim.py**  
   Runs SLiM simulations of adaptive introgression under a specified migration rate.

2. **02_extract_ancestry.py**  
   Extracts ancestry information for:
   - 50 individuals
   - 8 populations
   - Every 20 generations

3. **03_analyze_tracts.R**  
   - Computes mean ancestry tract lengths carrying the beneficial allele  
   - Associates tract lengths with allele frequencies in the population

Only the final table containing correlations is kept.

---

## Parallelization

Simulations are parallelized in R using `future_lapply()` to speed up computation.  
Each migration rate and replicate is run independently and later combined into a single dataset.

---

## Output Data

The main output file produced by the pipeline:

    ./data_all_with_corr.csv

### Data Structure

| Column | Description |
|------|-------------|
| Simulation | Simulation identifier (migration rate + replicate) |
| Population | Population ID |
| Génération | Generation |
| Longueur_Moyenne | Mean tract length carrying the beneficial allele |
| Fréquence | Allele frequency |
| mig | Migration rate |
| rep | Replicate number |

---

## Summary Statistics

For selected generations (740, 760, 780, 800, 820, 840, 860), correlations are computed between:

- Allele frequency  
- Mean ancestry tract length

Correlation tests:

- Pearson correlation  
- One-sided test (alternative = "greater")

Correlations are only computed when:

- More than 7 populations are available  
- Allele frequency is not fixed (> 0.9 in all populations)

---

## Visualization

### Heatmap of Significant Correlations

A heatmap shows the proportion of significant correlations (p < 0.05) across:

- Migration rates  
- Generations

Color scale:

- Blue: low proportion  
- Red: high proportion  
- Grey: insufficient data

### Example Scatter Plot

For a given migration rate and generation:

- Allele frequency vs. mean tract length  
- Points colored by population  
- Linear regressions drawn per replicate

---

## Repository Organization (Suggested)

    .
    ├── scripts/
    │   ├── 01_run_slim.py
    │   ├── 02_extract_ancestry.py
    │   └── 03_analyze_tracts.R
    ├── results/
    │   └── global_model/
    │       └── data_all_with_corr.csv
    ├── figures/
    ├── run_pipeline.R
    └── README.md

---

## Requirements

- SLiM  
- Python 3  
- R (≥ 4.0)

R packages:
- reticulate  
- ggplot2  
- dplyr  
- tidyr  
- future.apply

---



