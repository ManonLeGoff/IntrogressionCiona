# Simulation Pipeline – Adaptive Introgression

This repository contains a simulation and analysis pipeline designed to study the relationship between allele frequency and ancestry tract length during adaptive introgression.  
Simulations are performed using SLiM, and analysis in Python and R.


### Main Steps

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

---

## Parallelization

Simulations are parallelized in R using `future_lapply()` to speed up computation.  

---

## Output Data

The main output file produced by the pipeline:

    ./data_all_with_corr.csv






