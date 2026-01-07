# 1. Demultiplex
harpy demultiplex --threads 40 \
  --file Undetermined_L002_R1.fastq.gz \
  --samplesheet samplesheet.txt

# 2. Preflight
harpy preflight fastq \
  --directory ./Demultiplex/Undetermined_S0_L002/ \
  --threads 40

# 3. Alignement
harpy qc \
  --directory ./Demultiplex/Undetermined_S0_L002/ \
  --threads 40 \
  --extra-params '-c'
