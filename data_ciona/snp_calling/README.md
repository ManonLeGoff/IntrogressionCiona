The parameter --populations in [`snp_calling.sh`](snp_calling.sh) was used to compare variants within individuals from the same population.
_C. intestinalis_ individuals were differentiate based on their geographical origin. 

After calling we filtered the resulting VCF file to remove low-quality and incorrect variant sites using the parameters **MAF>=0.05** and **F_MISSING<=0.3**.
