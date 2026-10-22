# Referensi: Salindia Kuliah IF3070 Dasar Inteligensi Artifisial - Beyond Classical Search: Genetic Algorithm (Russell & Norvig, 2010)

import random
import time
from state import ShipState


def get_fitness_values(population):
    obj_values = [ind.get_objective_value() for ind in population]
    min_val = min(obj_values)
    if min_val < 0:
        return [val - min_val + 1 for val in obj_values]
    else:
        return [val + 1 for val in obj_values]


def random_selection(population, fitness_values):
    total = sum(fitness_values)
    pick = random.uniform(0, total)
    current = 0
    for i in range(len(population)):
        current += fitness_values[i]
        if current >= pick:
            return population[i]
    return population[-1]


def reproduce(x, y):
    n = len(x.placements)
    if n < 2:
        return x.copy_state()

    c = random.randint(1, n - 1)
    child_placements = []
    for p in x.placements[:c]:
        child_placements.append(dict(p))
    for p in y.placements[c:]:
        child_placements.append(dict(p))

    return ShipState(x.ship, x.vehicles, child_placements)


def mutate(child):
    return child.get_random_neighbor()


def get_best_individual(population):
    best_ind = population[0]
    best_val = best_ind.get_objective_value()

    for i in range(1, len(population)):
        curr_ind = population[i]
        curr_val = curr_ind.get_objective_value()
        if curr_val > best_val:
            best_ind = curr_ind
            best_val = curr_val

    return best_ind


def run_genetic_algorithm(initial_population, max_iterations=150, mutation_rate=0.1, record_history=False):
    start_time = time.time()

    population = [ind.copy_state() for ind in initial_population]
    population_size = len(population)

    initial_state = get_best_individual(population).copy_state()
    best_state = initial_state.copy_state()
    best_val = best_state.get_objective_value()

    max_obj_history = []
    avg_obj_history = []
    history = []

    if record_history:
        history.append({"iteration": 0, "state": initial_state.copy_state()})

    obj_values = [ind.get_objective_value() for ind in population]
    max_obj_history.append(max(obj_values))
    avg_obj_history.append(sum(obj_values) / len(obj_values))

    sample_step = max(1, max_iterations // 40)

    for iteration in range(1, max_iterations + 1):
        fitness_values = get_fitness_values(population)

        new_population = []
        for i in range(population_size):
            x = random_selection(population, fitness_values)
            y = random_selection(population, fitness_values)
            child = reproduce(x, y)

            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)

        population = new_population

        obj_values = [ind.get_objective_value() for ind in population]
        curr_max = max(obj_values)
        max_obj_history.append(curr_max)
        avg_obj_history.append(sum(obj_values) / len(obj_values))

        found_better = False
        if curr_max > best_val:
            current_best = get_best_individual(population)
            best_state = current_best.copy_state()
            best_val = best_state.get_objective_value()
            found_better = True

        if record_history and (found_better or iteration % sample_step == 0 or iteration == max_iterations):
            history.append({"iteration": iteration, "state": best_state.copy_state()})

    final_state = get_best_individual(population).copy_state()
    duration = time.time() - start_time

    return {
        "initial_state": initial_state,
        "final_state": final_state,
        "best_state": best_state,
        "initial_value": initial_state.get_objective_value(),
        "final_value": final_state.get_objective_value(),
        "best_value": best_state.get_objective_value(),
        "population_size": population_size,
        "iterations": max_iterations,
        "mutation_rate": mutation_rate,
        "duration": duration,
        "max_obj_history": max_obj_history,
        "avg_obj_history": avg_obj_history,
        "history": history
    }
