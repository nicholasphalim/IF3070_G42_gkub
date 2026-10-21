"""Shortcut script khusus untuk menjalankan eksperimen Simulated Annealing."""
from main import get_default_problem, run_simulated_annealing_experiment


def main():
    ship, vehicles = get_default_problem()
    run_simulated_annealing_experiment(ship, vehicles, output_dir="../output")


if __name__ == "__main__":
    main()