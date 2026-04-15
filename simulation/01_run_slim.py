# Manon Le Goff - Juillet 2025
# Script to run SLiM.

import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import shutil
import time
import sys

#Runs a slim script with the given parameters
def run_slim(slim_script, mig_value, rep):
    try:
        result = subprocess.run(
            ["slim", "-d", f"mig1={mig_value}", "-d", f"rep={rep}", slim_script],
            check=True,
            text=True,
            capture_output=True
        )
        print("SLiM finish")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("SLiM error:")
        print(e.stderr)

#Load allele frequencies
def load_frequencies(file_path):
    columns = ["generation", "population", "frequency"]
    try:
        data = pd.read_csv(file_path, sep="\t", names=columns)
    except FileNotFoundError:
        return pd.DataFrame()
    
    population_mapping = {
        "2": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "10": 8
    }
    data['population'] = data['population'].astype(str).map(population_mapping)
    return data.dropna()

#Plot allele frequencies
def plot_frequencies(data, output_file):
    plt.figure(figsize=(12, 8))
    populations = sorted(data['population'].unique())
    n_pops = len(populations)
    colors = cm.Blues(np.linspace(0.3, 0.9, n_pops))
    
    for pop, color in zip(populations, colors):
        subset = data[data['population'] == pop]
        plt.plot(subset['generation'], subset['frequency'], 
                 marker='o', color=color, label=f'Population {int(pop)}')

    plt.xlabel('Generations', fontsize=12)
    plt.ylabel('Allele Frequency', fontsize=12)
    plt.title('Allele Frequency Over Time', fontsize=14)
    plt.ylim(0, 1)
    plt.legend(title="Populations")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


def mutation_established(data, threshold=0.1):
    return (data['frequency'] >= threshold).any()


#Runs SLiM until mutation established
def run_until_data_exists(slim_script, output_file, mig_value, rep, threshold=0.1):
    while True:
        run_slim(slim_script, mig_value, rep)
        data = load_frequencies(output_file)
        if not data.empty:
            if mutation_established(data, threshold):
                print("Mutation established")
                return data
            else:
                print("not established")
        time.sleep(1)

#Run the simul
def run_simulation(slim_script, base_output_dir, mig_value, rep):
    sim_name = f"mig{mig_value}_rep{rep}"
    print(f"Running {sim_name}")

    simulation_dir = os.path.join(base_output_dir, sim_name)
    os.makedirs(simulation_dir, exist_ok=True)

    local_output_file = os.path.join(simulation_dir, "freq_pop.txt")
    local_tree_dir = os.path.join(simulation_dir, "trees")

    if os.path.exists(local_tree_dir):
        shutil.rmtree(local_tree_dir)
    os.makedirs(local_tree_dir, exist_ok=True)

    if os.path.exists(local_output_file):
        os.remove(local_output_file)

    frequencies_data = run_until_data_exists(slim_script, local_output_file, mig_value, rep)
    plot_frequencies(frequencies_data, os.path.join(simulation_dir, "frequencies.png"))

    print("Simulation OK")

#### Paths ####
# Choose the model 

#slim_script_path = "scripts/ltr_model.slim"
#base_output_dir = "results/ltr_model/simulations"

slim_script_path = "scripts/island_model.slim"
base_output_dir = "results/island_model/simulations"

#slim_script_path = "scripts/local_step_model.slim"
#base_output_dir = "results/local_step_model/simulations"

#slim_script_path = "scripts/global_model.slim"
#base_output_dir = "results/global_model/simulations"

os.makedirs(base_output_dir, exist_ok=True)

if __name__ == "__main__":
    mig_value = float(sys.argv[1])
    rep = int(sys.argv[2])
    run_simulation(slim_script_path, base_output_dir, mig_value, rep)
