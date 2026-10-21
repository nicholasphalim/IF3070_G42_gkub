# Referensi: Salindia Kuliah IF3070 Dasar Inteligensi Artifisial - Beyond Classical Search: Genetic Algorithm (Russell & Norvig, 2010)

import random
import time
from state import ShipState


def count_violations(state):
    total_fee = 0
    total_weight = 0
    overlap_count = 0
    out_of_bounds_count = 0

    grid = []
    for r in range(state.ship.length):
        grid.append([0] * state.ship.width)

    for i in range(len(state.vehicles)):
        p = state.placements[i]
        if not p["is_loaded"]:
            continue

        v = state.vehicles[i]
        total_fee += v.shipping_fee
        total_weight += v.weight

        w, l = state.get_vehicle_size(i)
        for dx in range(w):
            for dy in range(l):
                gx = p["x"] + dx
                gy = p["y"] + dy
                if gx < 0 or gx >= state.ship.width or gy < 0 or gy >= state.ship.length:
                    out_of_bounds_count += 1
                else:
                    if grid[gy][gx] >= 1:
                        overlap_count += 1
                    grid[gy][gx] += 1

    excess_weight = max(0, total_weight - state.ship.max_capacity)
    violations = overlap_count + out_of_bounds_count + excess_weight
    return total_fee, violations


def fitness(state):
    # fitness selalu >= 1 supaya proporsi roulette wheel tidak negatif / bagi nol
    total_fee, violations = count_violations(state)
    return total_fee / (1 + violations) + 1


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
    # salah satu dari 3 move: swap, move (termasuk masuk/keluar kapal), rotate
    return child.get_random_neighbor()


def get_best_individual(population):
    best = population[0]
    best_val = best.get_objective_value()
    for ind in population[1:]:
        val = ind.get_objective_value()
        if val > best_val:
            best = ind
            best_val = val
    return best


def run_genetic_algorithm(ship, vehicles, population_size=50, max_iterations=150, mutation_rate=0.1):
    start_time = time.time()

    population = []
    for i in range(population_size):
        population.append(ShipState(ship, vehicles))

    initial_state = get_best_individual(population).copy_state()

    max_obj_history = []
    avg_obj_history = []

    obj_values = [ind.get_objective_value() for ind in population]
    max_obj_history.append(max(obj_values))
    avg_obj_history.append(sum(obj_values) / len(obj_values))

    for iteration in range(max_iterations):
        fitness_values = [fitness(ind) for ind in population]

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

    final_state = get_best_individual(population).copy_state()
    duration = time.time() - start_time

    return {
        "initial_state": initial_state,
        "final_state": final_state,
        "initial_value": initial_state.get_objective_value(),
        "final_value": final_state.get_objective_value(),
        "population_size": population_size,
        "iterations": max_iterations,
        "mutation_rate": mutation_rate,
        "duration": duration,
        "max_obj_history": max_obj_history,
        "avg_obj_history": avg_obj_history
    }
