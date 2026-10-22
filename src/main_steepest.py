import os
import time
import json
import random
from main import get_default_problem
from state import ShipState
from algo.steepest import run_steepest_ascent
from visualizer import save_state_visualization, save_steepest_plots
def main():
    output_dir = "../output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_results = []
    
    print("\n" + "=" * 50)
    print("      EKSPERIMEN STEEPEST ASCENT (3 RUNS)     ")
    print("=" * 50)

    for run_num in range(1, 4):
        current_seed = int(time.time_ns() % 1000000)
        random.seed(current_seed)

        ship, vehicles = get_default_problem()
        initial_state = ShipState(ship, vehicles)

        result = run_steepest_ascent(
            initial_state=initial_state,
            max_iterations=500,
            num_neighbors=50
        )

        final_state = result["best_state"]

        print(f"\n--- Run {run_num} ---")
        print(f"Seed Initial    : {current_seed}")
        print(f"Nilai Awal      : {result['initial_value']}")
        print(f"Nilai Akhir     : {result['best_value']}")
        print(f"Total Iterasi   : {result['iterations']}")
        print(f"Waktu Eksekusi  : {round(result['duration'], 4)} detik")
        print(f"Status Valid    : {final_state.is_valid()}")

        states_path = os.path.join(output_dir, f"steepest_states_run_{run_num}.png")
        save_state_visualization(initial_state, final_state, run_num, states_path)
        
        metrics_path = os.path.join(output_dir, f"steepest_metrics_run_{run_num}.png")
        save_steepest_plots(result, run_num, metrics_path)

        time.sleep(0.01)
        
    
    json_path = os.path.join(output_dir, "steepest_results.json")
    with open(json_path, "w") as f:
        json.dump(all_results, f, indent=4)
    
    print("\n" + "=" * 50)
    print(f"Eksperimen Steepest Ascent selesai.")
    print(f"Gambar plot dan file 'steepest_results.json' berhasil tersimpan di folder output!")

if __name__ == "__main__":
    main()