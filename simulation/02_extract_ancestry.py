# Manon Le Goff - Juillet 2025
# Script to reconstruct local ancestry from all simulations across all generations

import os
import tskit
import tspop
import numpy as np
import random
import re
import sys

mig = sys.argv[1]
rep = sys.argv[2]

simu_dirname = f"mig{mig}_rep{rep}"

# Choose the model 
#simulations_base_dir = "results/ltr_model/simulations"
#base_output_path = "results/ltr_model/ancestry"

simulations_base_dir = "results/island_model/simulations"
base_output_path = "results/island_model/ancestry"

#simulations_base_dir = "results/local_step_model/simulations"
#base_output_path = "results/local_step_model/ancestry"

#simulations_base_dir = "results/global_model/simulations"
#base_output_path = "results/global_model/ancestry"

# Path to the simulation
simu_path = os.path.join(simulations_base_dir, simu_dirname)
trees_dir = os.path.join(simu_path, "trees")

simu_output_dir = os.path.join(base_output_path, simu_dirname)
os.makedirs(simu_output_dir, exist_ok=True)

# Populations and sample size
subpopulations = [2, 4, 5, 6, 7, 8, 9, 10]
sample_size = 50

# Loop over all trees files
for filename in os.listdir(trees_dir):

	# Extract generation
	match = re.search(r"generation(\d+)\.trees", filename)
	generation = int(match.group(1))

	trees_file_path = os.path.join(trees_dir, filename)
    ts = tskit.load(trees_file_path)

	for subpop in subpopulations:
			# Extract individuals from the subpopulation
			pop_ind = [ind for ind in ts.individuals() if ind.metadata["subpopulation"] == subpop]
			if len(pop_ind) < sample_size:
				continue

			sample_ind = random.sample(pop_ind, sample_size)
			node_ids = []
			for ind in sample_ind:
				node_ids.extend(ind.nodes)

			# Simplification
			ts_pop = ts.simplify(
				node_ids,
				keep_input_roots=True,
			)

			# Ancestry
			pa_pop = tspop.get_pop_ancestry(ts_pop, census_time=generation)
			at_pop = pa_pop.squashed_table

			output_csv = os.path.join(
				simu_output_dir,
				f"at_pop{subpop}_generation{generation}.csv"
			)
			at_pop.to_csv(output_csv, index=False)
			print(f"OK {simu_dirname} - Generation {generation} - Pop {subpop}")
