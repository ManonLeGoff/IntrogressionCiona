# Manon Le Goff - Novembre 2024
# Script to create summary statistic with the average tracts lenght and the frequency in each pop
import os
import re
import pandas as pd
import numpy as np

def analyze_tracts(simu_dir):

    def tracts_pop(at_data):
        at_data = at_data.copy()
        at_data["sample_id"] = at_data["sample"].astype(str)

        tracts_list = []

        for s, sample_data in at_data.groupby("sample_id"):
            sample_data = sample_data.sort_values("left").copy()

            change = sample_data["population"].ne(sample_data["population"].shift())
            sample_data_filtered = sample_data.loc[change].copy()

            sample_data_filtered["right"] = list(sample_data_filtered["left"].iloc[1:]) + [7499939]

            tracts_list.append(
                sample_data_filtered[["sample_id", "left", "right", "population"]]
            )

        return pd.concat(tracts_list, ignore_index=True)

    def calculate_lengths(data):
        results = []

        for s, tracts_sample in data.groupby("sample_id"):
            mask = (
                (tracts_sample["population"] == 1) &
                (tracts_sample["left"] < 3749970) &
                (tracts_sample["right"] > 3749970)
            )

            selected = tracts_sample.loc[mask]
            lengths = selected["right"] - selected["left"]

            if len(lengths) > 0:
                results.append(
                    pd.DataFrame({
                        "sample_id": s,
                        "length": lengths.values
                    })
                )

        if results:
            return pd.concat(results, ignore_index=True)
        else:
            return pd.DataFrame(columns=["sample_id", "length"])

    def freq(df, position=3749970):
        mask = (
            (df["population"] == 1) &
            (df["left"] < position) &
            (df["right"] > position)
        )

        samples_fix = df.loc[mask]
        return len(samples_fix["sample"]) / df["sample"].nunique()

    mean_lengths = []
    labels_pop = []
    generations = []
    simulation_names = []
    frequencies = []

    csv_files = [
        os.path.join(simu_dir, f)
        for f in os.listdir(simu_dir)
        if f.endswith(".csv")
    ]

    for csv_file in csv_files:
        fname = os.path.basename(csv_file)

        match = re.search(r"at_pop(\d+)_generation(\d+)\.csv", fname)
        if match is None:
            continue

        pop = int(match.group(1))
        gen = int(match.group(2))

        at_pop = pd.read_csv(csv_file)

        tracts = tracts_pop(at_pop)
        length_pop = calculate_lengths(tracts)

        mean_length = length_pop["length"].mean() if not length_pop.empty else np.nan
        freq_pop = freq(at_pop)

        mean_lengths.append(mean_length)
        labels_pop.append(pop)
        generations.append(gen)
        simulation_names.append(os.path.basename(simu_dir))
        frequencies.append(freq_pop)

    data_all = pd.DataFrame({
        "Simulation": simulation_names,
        "Population": labels_pop,
        "Génération": generations,
        "Longueur_Moyenne": mean_lengths,
        "Fréquence": frequencies
    })

    return data_all
