# Referensi: Salindia Kuliah IF3070 Dasar Inteligensi Artifisial - Beyond Classical Search: Genetic Algorithm (Russell & Norvig, 2010)

import os
import json
import random
from state import ShipState
from algo.genetic_algorithm import run_genetic_algorithm
from visualizer import save_state_visualization
from visualizer_ga import save_ga_plot


MUTATION_RATE = 0.1

# Eksperimen 1: populasi sebagai kontrol, iterasi divariasikan
EXP1_POPULATION = 50
EXP1_ITERATIONS = [50, 150, 300]

# Eksperimen 2: iterasi sebagai kontrol, populasi divariasikan
EXP2_ITERATIONS = 150
EXP2_POPULATIONS = [20, 50, 100]


def run_single(ship, vehicles, exp_num, population_size, max_iterations, run_num, seed, output_dir):
    random.seed(seed)
    initial_population = [ShipState(ship, vehicles) for _ in range(population_size)]

    # Reset seed agar proses stokastik GA berjalan wajar
    random.seed()

    result = run_genetic_algorithm(initial_population, max_iterations, MUTATION_RATE)
    initial_state = result["initial_state"]
    final_state = result["final_state"]
    best_state = result["best_state"]

    print(f"\n--- Eksperimen {exp_num} | Populasi {population_size} | Iterasi {max_iterations} | Run {run_num} ---")
    print(f"Seed Initial    : {seed}")
    print(f"Initial Value   : {result['initial_value']}")
    print(f"Final Value     : {result['final_value']}")
    if result["best_value"] != result["final_value"]:
        print(f"Best Value      : {result['best_value']} (terbaik selama pencarian)")
    print(f"Valid State?    : {final_state.is_valid()}")
    print(f"Durasi          : {round(result['duration'], 4)} detik")

    name = f"exp{exp_num}_pop{population_size}_iter{max_iterations}_run{run_num}"
    label = f"Eksperimen {exp_num} - Populasi {population_size}, Iterasi {max_iterations}, Run {run_num}"
    save_ga_plot(result, label, os.path.join(output_dir, f"{name}_plot.png"))
    save_state_visualization(initial_state, final_state, f"{run_num}, Exp {exp_num}, Pop {population_size}, Iter {max_iterations}",
                             os.path.join(output_dir, f"{name}_states.png"))

    return {
        "experiment": exp_num,
        "run": run_num,
        "seed": seed,
        "population_size": population_size,
        "iterations": max_iterations,
        "mutation_rate": MUTATION_RATE,
        "duration_seconds": result["duration"],
        "initial_state": initial_state.to_dict(),
        "final_state": final_state.to_dict(),
        "best_state": best_state.to_dict(),
        "max_obj_history": result["max_obj_history"],
        "avg_obj_history": result["avg_obj_history"]
    }


def get_state_lines(title, state_dict):
    lines = [f"  {title} (value = {state_dict['objective_value']}, valid = {state_dict['is_valid']}, berat = {state_dict['total_weight']})"]
    lines.append("    Di dalam kapal:")
    if len(state_dict["loaded_vehicles"]) == 0:
        lines.append("      Tidak ada")
    for v in state_dict["loaded_vehicles"]:
        lines.append(f"      {v['id']:<4} ({v['x']}, {v['y']}) {v['orientation']:<10} {v['width']}x{v['length']} fee={v['shipping_fee']} weight={v['weight']}")
    outside = [v["id"] for v in state_dict["unloaded_vehicles"]]
    lines.append("    Di luar kapal: " + (", ".join(outside) if len(outside) > 0 else "Tidak ada"))
    return lines


def write_summary(all_results, filepath):
    lines = []
    lines.append("Ringkasan Eksperimen Genetic Algorithm")
    lines.append(f"Mutation rate: {MUTATION_RATE}")
    lines.append("Koordinat (x, y) = sel kiri bawah kendaraan, origin (0, 0) di kiri bawah geladak")
    lines.append("")
    lines.append(f"{'Exp':<4}{'Populasi':<10}{'Iterasi':<9}{'Run':<5}{'Seed':<9}{'Awal':<8}{'Akhir':<8}{'Valid':<7}{'Durasi (s)':<10}")
    lines.append("-" * 70)
    for r in all_results:
        lines.append(f"{r['experiment']:<4}{r['population_size']:<10}{r['iterations']:<9}{r['run']:<5}{r['seed']:<9}"
                     f"{r['initial_state']['objective_value']:<8}{r['final_state']['objective_value']:<8}"
                     f"{str(r['final_state']['is_valid']):<7}{r['duration_seconds']:<10.3f}")

    lines.append("")
    lines.append("Rata-rata per konfigurasi:")
    configs = []
    for r in all_results:
        key = (r["experiment"], r["population_size"], r["iterations"])
        if key not in configs:
            configs.append(key)
    for exp_num, pop, it in configs:
        group = [r for r in all_results if r["experiment"] == exp_num and r["population_size"] == pop and r["iterations"] == it]
        avg_val = sum(r["final_state"]["objective_value"] for r in group) / len(group)
        avg_dur = sum(r["duration_seconds"] for r in group) / len(group)
        lines.append(f"  Exp {exp_num} pop={pop:<4} iter={it:<4} -> rata-rata akhir = {avg_val:.2f}, rata-rata durasi = {avg_dur:.3f}s")

    lines.append("")
    lines.append("Detail state awal dan akhir:")
    for r in all_results:
        lines.append("")
        lines.append(f"Eksperimen {r['experiment']} | Populasi {r['population_size']} | Iterasi {r['iterations']} | Run {r['run']}")
        lines.extend(get_state_lines("State awal", r["initial_state"]))
        lines.extend(get_state_lines("State akhir", r["final_state"]))

    with open(filepath, "w") as f:
        f.write("\n".join(lines) + "\n")


def run_genetic_algorithm_experiment(ship, vehicles, output_dir="../output/ga", seeds=None):
    """Menjalankan 2 skenario eksperimen Genetic Algorithm, masing-masing 3 konfigurasi x 3 run."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if seeds is None:
        seeds = [random.SystemRandom().randint(0, 10**6) for _ in range(3)]

    print("\n" + "=" * 50)
    print("     EKSPERIMEN GENETIC ALGORITHM (18 RUNS)")
    print("=" * 50)

    all_results = []

    for it in EXP1_ITERATIONS:
        for i in range(3):
            all_results.append(run_single(ship, vehicles, 1, EXP1_POPULATION, it, i + 1, seeds[i], output_dir))

    for pop in EXP2_POPULATIONS:
        for i in range(3):
            all_results.append(run_single(ship, vehicles, 2, pop, EXP2_ITERATIONS, i + 1, seeds[i], output_dir))

    with open(os.path.join(output_dir, "ga_results.json"), "w") as f:
        json.dump(all_results, f, indent=4)
    write_summary(all_results, os.path.join(output_dir, "ga_summary.txt"))

    print("\nEksperimen Genetic Algorithm selesai.")
    print("Hasil plot, file JSON, dan ringkasan tersimpan di folder output/ga")
