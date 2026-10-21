from main import get_default_problem
from experiment_ga import run_genetic_algorithm_experiment


def main():
    ship, vehicles = get_default_problem()
    run_genetic_algorithm_experiment(ship, vehicles)


if __name__ == "__main__":
    main()
