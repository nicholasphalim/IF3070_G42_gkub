# Referensi: Salindia Kuliah IF3070 Dasar Inteligensi Artifisial - Beyond Classical Search: Genetic Algorithm (Russell & Norvig, 2010)

import random
import time
from state import ShipState


def get_fitness_values(population):
    # objective bisa negatif karena penalti, jadi dibatasi minimal 1
    # supaya proporsi roulette wheel tidak negatif / bagi nol
    return [max(ind.get_objective_value(), 0) + 1 for ind in population]


def random_selection(population, fitness_values):
    # roulette wheel: P_i = F_i / sum(F)
    total = sum(fitness_values)
    pick = random.uniform(0, total)
    current = 0
    for i in range(len(population)):
        current += fitness_values[i]
        if current >= pick:
            return population[i]
    return population[-1]


def reproduce(x, y):
    # single-point crossover, c dipilih dari 1 sampai N-1
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
    # salah satu dari 3 move: swap, move, rotate
    return child.get_random_neighbor()


def get_best_individual(population):
    # state valid diutamakan, lalu dibandingkan objective value-nya
    best = population[0]
    for ind in population[1:]:
        if (ind.is_valid(), ind.get_objective_value()) > (best.is_valid(), best.get_objective_value()):
            best = ind
    return best


def run_genetic_algorithm(initial_population, max_iterations=150, mutation_rate=0.1):
    start_time = time.time()

    population = [ind.copy_state() for ind in initial_population]
    population_size = len(population)

    initial_state = get_best_individual(population).copy_state()
    best_state = initial_state.copy_state()

    max_obj_history = []
    avg_obj_history = []

    obj_values = [ind.get_objective_value() for ind in population]
    max_obj_history.append(max(obj_values))
    avg_obj_history.append(sum(obj_values) / len(obj_values))

    for iteration in range(max_iterations):
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
        max_obj_history.append(max(obj_values))
        avg_obj_history.append(sum(obj_values) / len(obj_values))

        generation_best = get_best_individual(population)
        if get_best_individual([best_state, generation_best]) is generation_best:
            best_state = generation_best.copy_state()

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
        "avg_obj_history": avg_obj_history
    }
