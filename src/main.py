import os
import sys
import json
import random
from entities import load_problem_from_dict
from state import ShipState
from algo.sim_annealing import run_simulated_annealing
from algo.genetic_algorithm import run_genetic_algorithm
from visualizer import save_sa_plots, save_state_visualization, save_ga_plots, save_state_animation


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


def prompt_for_seeds():
    """Meminta opsi seed kepada pengguna untuk menjamin initial state yang adil dan sama."""
    print("\nOpsi Seed Initial State:")
    print("  [1] Benchmark Standar [42, 100, 2026] (Rekomendasi: Initial State sama persis antar algoritma)")
    print("  [2] Masukkan 3 angka seed sendiri (Custom)")
    print("  [3] Acak baru (Random sepenuhnya)")
    try:
        opt = input("Pilih opsi seed (1/2/3) [Default 1]: ").strip()
    except EOFError:
        opt = "1"

    if opt == "2":
        try:
            raw = input("Masukkan 3 angka seed dipisahkan spasi (contoh: 10 20 30): ").strip()
            nums = [int(x) for x in raw.split() if x.lstrip('-').isdigit()]
            if len(nums) >= 3:
                return nums[:3]
            print("[INFO] Input tidak lengkap, menggunakan benchmark standar [42, 100, 2026].")
            return [42, 100, 2026]
        except Exception:
            return [42, 100, 2026]
    elif opt == "3":
        return None  # akan diacak otomatis
    else:
        return [42, 100, 2026]


def run_hill_climbing_placeholder(ship, vehicles, seeds=None):
    """Menjalankan eksperimen Steepest Ascent Hill-Climbing."""
    try:
        from main_steepest import main as run_steepest_main
        run_steepest_main(seeds=seeds)
    except TypeError:
        from main_steepest import main as run_steepest_main
        run_steepest_main()
    except ImportError:
        try:
            from algo.steepest import run_steepest_ascent_experiment
            run_steepest_ascent_experiment(ship, vehicles, seeds=seeds)
        except (ImportError, TypeError):
            print("\n[INFO] Modul Steepest Ascent tidak ditemukan.")


def run_genetic_algorithm_experiment(ship, vehicles, output_dir="../output", seeds=None):
    """Menjalankan eksperimen Genetic Algorithm sebanyak 3 kali sesuai spesifikasi."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if seeds is None:
        seeds = [random.SystemRandom().randint(0, 10**6) for _ in range(3)]

    population_size = 50
    max_iterations = 150
    mutation_rate = 0.1

    all_results = []

    print("\n" + "=" * 50)
    print("        EKSPERIMEN GENETIC ALGORITHM (3 RUNS)     ")
    print("=" * 50)

    for i in range(3):
        run_num = i + 1
        seed = seeds[i]
        random.seed(seed)
        initial_population = [ShipState(ship, vehicles) for _ in range(population_size)]
        random.seed()

        # Rekam animasi proses iterasi hanya pada Run 1
        record = (run_num == 1)
        result = run_genetic_algorithm(
            initial_population,
            max_iterations=max_iterations,
            mutation_rate=mutation_rate,
            record_history=record
        )
        initial_state = result["initial_state"]
        final_state = result["final_state"]
        best_state = result["best_state"]

        print(f"\n--- Run {run_num} ---")
        print(f"Seed Initial    : {seed}")
        print(f"Initial Value   : {result['initial_value']}")
        print(f"Final Value     : {result['final_value']}")
        if result["best_value"] != result["final_value"]:
            print(f"Best Value      : {result['best_value']} (terbaik selama pencarian)")
        print(f"Valid State?    : {final_state.is_valid()}")
        print(f"Total Generasi  : {result['iterations']}")
        print(f"Ukuran Populasi : {result['population_size']}")
        print(f"Durasi          : {round(result['duration'], 4)} detik")

        # Simpan grafik visualisasi
        metrics_path = os.path.join(output_dir, f"ga_metrics_run_{run_num}.png")
        states_path = os.path.join(output_dir, f"ga_states_run_{run_num}.png")

        save_ga_plots(result, run_num, metrics_path)
        save_state_visualization(initial_state, final_state, run_num, states_path)

        if record and result.get("history"):
            gif_path = os.path.join(output_dir, "ga_live_progress.gif")
            save_state_animation(result["history"], gif_path)

        all_results.append({
            "run": run_num,
            "seed": seed,
            "population_size": population_size,
            "iterations": max_iterations,
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

    print("\nEksperimen Genetic Algorithm selesai.")
    print("Hasil plot, file JSON, dan animasi tersimpan di folder " + output_dir)


def main():
    ship, vehicles = get_default_problem()

    # Jika ada argumen CLI (misal: python main.py 2)
    if len(sys.argv) > 1:
        choice = sys.argv[1].strip()
        # Jika argumen kedua ada seed (misal python main.py 2 42,100,2026)
        if len(sys.argv) > 2:
            try:
                seeds = [int(x) for x in sys.argv[2].split(",") if x.strip().isdigit()]
            except Exception:
                seeds = [42, 100, 2026]
        else:
            seeds = [42, 100, 2026]
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

        if choice in ["1", "hc", "hill-climbing", "2", "sa", "simulated-annealing", "3", "ga", "genetic-algorithm"]:
            seeds = prompt_for_seeds()
        else:
            seeds = None

    if choice in ["1", "hc", "hill-climbing"]:
        run_hill_climbing_placeholder(ship, vehicles, seeds=seeds)
    elif choice in ["2", "sa", "simulated-annealing"]:
        run_simulated_annealing_experiment(ship, vehicles, seeds=seeds)
    elif choice in ["3", "ga", "genetic-algorithm"]:
        run_genetic_algorithm_experiment(ship, vehicles, seeds=seeds)
    elif choice in ["4", "exit", "q"]:
        print("Program selesai. Sampai jumpa!")
    else:
        print(f"Pilihan '{choice}' tidak valid. Silakan jalankan program kembali.")


if __name__ == "__main__":
    main()
