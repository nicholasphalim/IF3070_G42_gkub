import os
import sys
import json
import random
from entities import load_problem_from_dict
from state import ShipState
from algo.sim_annealing import run_simulated_annealing
from algo.genetic_algorithm import run_genetic_algorithm
from visualizer import save_sa_plots, save_state_visualization, save_ga_plots


def get_default_problem():
    """Mengembalikan objek ship dan vehicles sesuai spesifikasi kasus uji."""
    problem_data = {
        "ship": {
            "width": 10,
            "length": 16,
            "max_capacity": 50
        },
        "vehicles": [
            {"id": "V1", "width": 3, "length": 4, "shipping_fee": 60, "weight": 6, "eta": 2},
            {"id": "V2", "width": 4, "length": 5, "shipping_fee": 95, "weight": 10, "eta": 1},
            {"id": "V3", "width": 2, "length": 3, "shipping_fee": 35, "weight": 4, "eta": 4},
            {"id": "V4", "width": 3, "length": 6, "shipping_fee": 85, "weight": 9, "eta": 3},
            {"id": "V5", "width": 5, "length": 5, "shipping_fee": 120, "weight": 12, "eta": 1},
            {"id": "V6", "width": 2, "length": 4, "shipping_fee": 45, "weight": 5, "eta": 5},
            {"id": "V7", "width": 3, "length": 3, "shipping_fee": 50, "weight": 5, "eta": 2},
            {"id": "V8", "width": 4, "length": 4, "shipping_fee": 75, "weight": 8, "eta": 3},
            {"id": "V9", "width": 2, "length": 5, "shipping_fee": 55, "weight": 6, "eta": 2},
            {"id": "V10", "width": 3, "length": 5, "shipping_fee": 70, "weight": 7, "eta": 4}
        ]
    }
    return load_problem_from_dict(problem_data)


def run_simulated_annealing_experiment(ship, vehicles, output_dir="../output", seeds=None):
    """Menjalankan eksperimen Simulated Annealing sebanyak 3 kali sesuai spesifikasi.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if seeds is None:
        seeds = [random.SystemRandom().randint(0, 10**6) for _ in range(3)]
    all_results = []

    print("\n" + "=" * 50)
    print("      EKSPERIMEN SIMULATED ANNEALING (3 RUNS)     ")
    print("=" * 50)

    for i in range(3):
        run_num = i + 1
        random.seed(seeds[i])
        initial_state = ShipState(ship, vehicles)

        # Reset seed agar proses transisi stokastik SA berjalan wajar
        random.seed()

        result = run_simulated_annealing(
            initial_state=initial_state,
            initial_temp=1000.0,
            cooling_rate=0.995,
            min_temp=0.01,
            max_iterations=2000,
            stuck_limit=50
        )

        final_state = result["final_state"]
        best_state = result["best_state"]

        print(f"\n--- Run {run_num} ---")
        print(f"Seed Initial    : {seeds[i]}")
        print(f"Initial Value   : {result['initial_value']}")
        print(f"Final Value     : {result['final_value']}")
        if result['best_value'] != result['final_value']:
            print(f"Best Value      : {result['best_value']} (elitism)")
        print(f"Valid State?    : {final_state.is_valid()}")
        print(f"Total Iterasi   : {result['iterations']}")
        print(f"Frekuensi Stuck : {result['stuck_frequency']} kali")
        print(f"Durasi          : {round(result['duration'], 4)} detik")

        # Simpan grafik visualisasi
        metrics_path = os.path.join(output_dir, f"sa_metrics_run_{run_num}.png")
        states_path = os.path.join(output_dir, f"sa_states_run_{run_num}.png")

        save_sa_plots(result, run_num, metrics_path)
        save_state_visualization(initial_state, final_state, run_num, states_path)

        all_results.append({
            "run": run_num,
            "seed": seeds[i],
            "duration_seconds": result["duration"],
            "iterations": result["iterations"],
            "stuck_frequency": result["stuck_frequency"],
            "stuck_iterations": result["stuck_iterations"],
            "initial_state": initial_state.to_dict(),
            "final_state": final_state.to_dict(),
            "best_state": best_state.to_dict()
        })

    # Simpan ringkasan hasil ke JSON
    json_path = os.path.join(output_dir, "sa_results.json")
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=4)

    print("\nEksperimen Simulated Annealing selesai.")
    print(f"Hasil plot dan file JSON tersimpan di folder output")


def run_hill_climbing_placeholder(ship, vehicles):
    """Placeholder untuk modul Hill-Climbing yang dikembangkan anggota tim."""
    try:
        from algo.hill_climbing import run_hill_climbing_experiment
        run_hill_climbing_experiment(ship, vehicles)
    except (ImportError, AttributeError):
        print("\n[INFO] Modul Hill-Climbing (algo/hill_climbing.py) sedang dikembangkan oleh anggota tim.")


def _write_ga_summary(all_results, filepath, mutation_rate):
    lines = []
    lines.append("Ringkasan Eksperimen Genetic Algorithm")
    lines.append(f"Mutation rate: {mutation_rate}")
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
        for label_st, state_dict in [("State awal", r["initial_state"]), ("State akhir", r["final_state"])]:
            lines.append(f"  {label_st} (value = {state_dict['objective_value']}, valid = {state_dict['is_valid']}, berat = {state_dict['total_weight']})")
            lines.append("    Di dalam kapal:")
            if len(state_dict["loaded_vehicles"]) == 0:
                lines.append("      Tidak ada")
            for v in state_dict["loaded_vehicles"]:
                lines.append(f"      {v['id']:<4} ({v['x']}, {v['y']}) {v['orientation']:<10} {v['width']}x{v['length']} fee={v['shipping_fee']} weight={v['weight']}")
            outside = [v["id"] for v in state_dict["unloaded_vehicles"]]
            lines.append("    Di luar kapal: " + (", ".join(outside) if len(outside) > 0 else "Tidak ada"))

    with open(filepath, "w") as f:
        f.write("\n".join(lines) + "\n")


def run_genetic_algorithm_experiment(ship, vehicles, output_dir="../output/ga", seeds=None):
    """Menjalankan eksperimen Genetic Algorithm (18 runs: 2 skenario) sesuai spesifikasi."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if seeds is None:
        seeds = [random.SystemRandom().randint(0, 10**6) for _ in range(3)]

    mutation_rate = 0.1
    exp1_pop = 50
    exp1_iters = [50, 150, 300]
    exp2_iter = 150
    exp2_pops = [20, 50, 100]

    all_results = []

    print("\n" + "=" * 50)
    print("     EKSPERIMEN GENETIC ALGORITHM (18 RUNS)       ")
    print("=" * 50)

    configs = []
    for it in exp1_iters:
        configs.append((1, exp1_pop, it))
    for pop in exp2_pops:
        configs.append((2, pop, exp2_iter))

    for exp_num, pop_size, max_iters in configs:
        for i in range(3):
            run_num = i + 1
            seed = seeds[i]
            random.seed(seed)
            initial_population = [ShipState(ship, vehicles) for _ in range(pop_size)]
            random.seed()

            result = run_genetic_algorithm(initial_population, max_iters, mutation_rate)
            initial_state = result["initial_state"]
            final_state = result["final_state"]
            best_state = result["best_state"]

            print(f"\n--- Eksperimen {exp_num} | Populasi {pop_size} | Iterasi {max_iters} | Run {run_num} ---")
            print(f"Seed Initial    : {seed}")
            print(f"Initial Value   : {result['initial_value']}")
            print(f"Final Value     : {result['final_value']}")
            if result["best_value"] != result["final_value"]:
                print(f"Best Value      : {result['best_value']} (terbaik selama pencarian)")
            print(f"Valid State?    : {final_state.is_valid()}")
            print(f"Durasi          : {round(result['duration'], 4)} detik")

            name = f"exp{exp_num}_pop{pop_size}_iter{max_iters}_run{run_num}"
            label = f"Eksperimen {exp_num} - Populasi {pop_size}, Iterasi {max_iters}, Run {run_num}"
            plot_path = os.path.join(output_dir, f"{name}_plot.png")
            states_path = os.path.join(output_dir, f"{name}_states.png")

            save_ga_plots(result, label, plot_path)
            save_state_visualization(initial_state, final_state, f"{run_num}, Exp {exp_num}, Pop {pop_size}, Iter {max_iters}", states_path)

            all_results.append({
                "experiment": exp_num,
                "run": run_num,
                "seed": seed,
                "population_size": pop_size,
                "iterations": max_iters,
                "mutation_rate": mutation_rate,
                "duration_seconds": result["duration"],
                "initial_state": initial_state.to_dict(),
                "final_state": final_state.to_dict(),
                "best_state": best_state.to_dict(),
                "max_obj_history": result["max_obj_history"],
                "avg_obj_history": result["avg_obj_history"]
            })

    json_path = os.path.join(output_dir, "ga_results.json")
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=4)

    summary_path = os.path.join(output_dir, "ga_summary.txt")
    _write_ga_summary(all_results, summary_path, mutation_rate)

    print("\nEksperimen Genetic Algorithm selesai.")
    print("Hasil plot, file JSON, dan ringkasan tersimpan di folder " + output_dir)


def main():
    ship, vehicles = get_default_problem()

    # Jika ada argumen CLI (misal: python main.py 2)
    if len(sys.argv) > 1:
        choice = sys.argv[1].strip()
    else:
        print("\n" + "=" * 52)
        print("   TUGAS BESAR 1 IF3070 DASAR AI - LOCAL SEARCH (G42)  ")
        print("=" * 52)
        print("Pilih algoritma yang ingin dijalankan:")
        print("  [1] Hill-Climbing")
        print("  [2] Simulated Annealing")
        print("  [3] Genetic Algorithm")
        print("  [4] Keluar")
        print("-" * 52)
        try:
            choice = input("Masukkan pilihan Anda (1/2/3/4): ").strip()
        except EOFError:
            choice = "2"

    if choice in ["1", "hc", "hill-climbing"]:
        run_hill_climbing_placeholder(ship, vehicles)
    elif choice in ["2", "sa", "simulated-annealing"]:
        run_simulated_annealing_experiment(ship, vehicles)
    elif choice in ["3", "ga", "genetic-algorithm"]:
        run_genetic_algorithm_experiment(ship, vehicles)
    elif choice in ["4", "exit", "q"]:
        print("Program selesai. Sampai jumpa!")
    else:
        print(f"Pilihan '{choice}' tidak valid. Silakan jalankan program kembali.")


if __name__ == "__main__":
    main()
