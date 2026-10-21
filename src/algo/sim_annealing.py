import math
import random
import time


def run_simulated_annealing(initial_state, initial_temp=1000.0, cooling_rate=0.995, min_temp=0.01, max_iterations=2000, stuck_limit=30):
    start_time = time.time()

    current_state = initial_state.copy_state()
    current_val = current_state.get_objective_value()

    best_state = current_state.copy_state()
    best_val = current_val

    temp = initial_temp
    iteration = 0

    rejection_counter = 0
    stuck_frequency = 0

    obj_history = [current_val]
    best_obj_history = [best_val]
    prob_iterations = []
    prob_history = []

    while temp > min_temp and iteration < max_iterations:
        iteration += 1

        neighbor = current_state.get_random_neighbor()
        neighbor_val = neighbor.get_objective_value()

        delta_e = neighbor_val - current_val

        if delta_e > 0:
            accept = True
        elif delta_e == 0:
            accept = True
        else:
            prob = math.exp(delta_e / temp)
            prob_iterations.append(iteration)
            prob_history.append(prob)

            if random.random() < prob:
                accept = True
            else:
                accept = False

        if accept:
            current_state = neighbor
            current_val = neighbor_val
            rejection_counter = 0  #bisa pindah posisi, ga stuck

            if current_val > best_val:
                best_state = current_state.copy_state()
                best_val = current_val
        else:
            #ditolak, ga pindah posisi
            rejection_counter += 1
            if rejection_counter >= stuck_limit:
                stuck_frequency += 1
                rejection_counter = 0

        obj_history.append(current_val)
        best_obj_history.append(best_val)

        # turunkan suhu
        temp = temp * cooling_rate

    duration = time.time() - start_time

    return {
        "initial_state": initial_state,
        "final_state": current_state,
        "best_state": best_state,
        "initial_value": initial_state.get_objective_value(),
        "final_value": current_val,
        "best_value": best_val,
        "duration": duration,
        "iterations": iteration,
        "stuck_frequency": stuck_frequency,
        "obj_history": obj_history,
        "best_obj_history": best_obj_history,
        "prob_iterations": prob_iterations,
        "prob_history": prob_history
    }