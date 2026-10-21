# Referensi: Salindia Kuliah IF3070 Dasar Inteligensi Artifisial - Beyond Classical Search: Genetic Algorithm (Russell & Norvig, 2010)

import os
import json
import random
from algo.genetic_algorithm import run_genetic_algorithm
from visualizer_ga import save_ga_plot, save_ga_state_visualization


SEEDS = [42, 100, 2026]
MUTATION_RATE = 0.1

# Eksperimen 1: populasi sebagai kontrol, iterasi divariasikan
EXP1_POPULATION = 50
EXP1_ITERATIONS = [50, 150, 300]

# Eksperimen 2: iterasi sebagai kontrol, populasi divariasikan
EXP2_ITERATIONS = 150
EXP2_POPULATIONS = [20, 50, 100]


def run_single(ship, vehicles, exp_num, population_size, max_iterations, run_num, output_dir):
    random.seed(SEEDS[run_num - 1])
    result = run_genetic_algorithm(ship, vehicles, population_size, max_iterations, MUTATION_RATE)

    name = f"exp{exp_num}_pop{population_size}_iter{max_iterations}_run{run_num}"
    label = f"Eksperimen {exp_num} - Populasi {population_size}, Iterasi {max_iterations}, Run {run_num}"

    save_ga_plot(result, label, os.path.join(output_dir, f"{name}_plot.png"))
    save_ga_state_visualization(result["initial_state"], result["final_state"], label, os.path.join(output_dir, f"{name}_states.png"))

    print(f"[Exp {exp_num}] pop={population_size:<4} iter={max_iterations:<4} run={run_num} | "
          f"awal={result['initial_value']:<8} akhir={result['final_value']:<6} "
          f"valid={result['final_state'].is_valid()} durasi={result['duration']:.3f}s")

    return {
        "experiment": exp_num,
        "run": run_num,
        "seed": SEEDS[run_num - 1],
        "population_size": population_size,
        "iterations": max_iterations,
        "mutation_rate": MUTATION_RATE,
        "duration_seconds": result["duration"],
        "initial_value": result["initial_value"],
        "final_value": result["final_value"],
        "initial_state": result["initial_state"].to_dict(),
        "final_state": result["final_state"].to_dict(),
        "max_obj_history": result["max_obj_history"],
        "avg_obj_history": result["avg_obj_history"]
    }


def write_summary(all_results, filepath):
    lines = []
    lines.append("Ringkasan Eksperimen Genetic Algorithm")
    lines.append(f"Mutation rate: {MUTATION_RATE}")
    lines.append("")
    lines.append(f"{'Exp':<4}{'Populasi':<10}{'Iterasi':<9}{'Run':<5}{'Awal':<10}{'Akhir':<8}{'Valid':<7}{'Durasi (s)':<10}")
    lines.append("-" * 63)
    for r in all_results:
        lines.append(f"{r['experiment']:<4}{r['population_size']:<10}{r['iterations']:<9}{r['run']:<5}"
                     f"{r['initial_value']:<10}{r['final_value']:<8}{str(r['final_state']['is_valid']):<7}"
                     f"{r['duration_seconds']:<10.3f}")

    lines.append("")
    lines.append("Rata-rata per konfigurasi:")
    configs = []
    for r in all_results:
        key = (r["experiment"], r["population_size"], r["iterations"])
        if key not in configs:
            configs.append(key)
    for exp_num, pop, it in configs:
        group = [r for r in all_results if r["experiment"] == exp_num and r["population_size"] == pop and r["iterations"] == it]
        avg_val = sum(r["final_value"] for r in group) / len(group)
        avg_dur = sum(r["duration_seconds"] for r in group) / len(group)
        lines.append(f"  Exp {exp_num} pop={pop:<4} iter={it:<4} -> rata-rata akhir = {avg_val:.2f}, rata-rata durasi = {avg_dur:.3f}s")

    with open(filepath, "w") as f:
        f.write("\n".join(lines) + "\n")


def run_genetic_algorithm_experiment(ship, vehicles, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "ga")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("\n" + "=" * 50)
    print("     EKSPERIMEN GENETIC ALGORITHM (18 RUNS)")
    print("=" * 50)

    all_results = []

    print(f"\nEksperimen 1: populasi tetap {EXP1_POPULATION}, iterasi {EXP1_ITERATIONS}")
    for it in EXP1_ITERATIONS:
        for run_num in range(1, 4):
            all_results.append(run_single(ship, vehicles, 1, EXP1_POPULATION, it, run_num, output_dir))

    print(f"\nEksperimen 2: iterasi tetap {EXP2_ITERATIONS}, populasi {EXP2_POPULATIONS}")
    for pop in EXP2_POPULATIONS:
        for run_num in range(1, 4):
            all_results.append(run_single(ship, vehicles, 2, pop, EXP2_ITERATIONS, run_num, output_dir))

    with open(os.path.join(output_dir, "ga_results.json"), "w") as f:
        json.dump(all_results, f, indent=4)
    write_summary(all_results, os.path.join(output_dir, "ga_summary.txt"))

    print("\nEksperimen Genetic Algorithm selesai.")
    print(f"Hasil plot, JSON, dan ringkasan tersimpan di {os.path.normpath(output_dir)}")
