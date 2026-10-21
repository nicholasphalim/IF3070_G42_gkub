import os
import sys
import json
import random
from entities import load_problem_from_dict
from state import ShipState
from algo.sim_annealing import run_simulated_annealing
from visualizer import save_sa_plots, save_state_visualization


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


def run_simulated_annealing_experiment(ship, vehicles, output_dir="../output"):
    """Menjalankan eksperimen Simulated Annealing sebanyak 3 kali sesuai spesifikasi."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    seeds = [42, 100, 2026]
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
            stuck_limit=30
        )

        final_state = result["best_state"]

        print(f"\n--- Run {run_num} ---")
        print(f"Initial Value   : {result['initial_value']}")
        print(f"Final Value     : {result['best_value']}")
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
            "duration_seconds": result["duration"],
            "iterations": result["iterations"],
            "stuck_frequency": result["stuck_frequency"],
            "initial_state": initial_state.to_dict(),
            "final_state": final_state.to_dict()
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


def run_genetic_algorithm_placeholder(ship, vehicles):
    """Placeholder untuk modul Genetic Algorithm yang dikembangkan anggota tim."""
    try:
        from experiment_ga import run_genetic_algorithm_experiment
        run_genetic_algorithm_experiment(ship, vehicles)
    except (ImportError, AttributeError):
        print("\n[INFO] Modul Genetic Algorithm (algo/genetic_algorithm.py) sedang dikembangkan oleh anggota tim.")


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
        run_genetic_algorithm_placeholder(ship, vehicles)
    elif choice in ["4", "exit", "q"]:
        print("Program selesai. Sampai jumpa!")
    else:
        print(f"Pilihan '{choice}' tidak valid. Silakan jalankan program kembali.")


if __name__ == "__main__":
    main()
