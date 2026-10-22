import math
import random
import time


def run_simulated_annealing(initial_state, initial_temp=1000.0, cooling_rate=0.995, min_temp=0.01, max_iterations=2000, stuck_limit=50):
    start_time = time.time()

    current_state = initial_state.copy_state()
    current_val = current_state.get_objective_value()

    best_state = current_state.copy_state()
    best_val = current_val

    temp = initial_temp
    iteration = 0

    # Stuck = nilai current ga berubah2 selama stuck_limit iterasi berturut-turut,
    # artinya agen itu stuck di local maximum / flat local maximum (plateau) / shoulder.
    # Sideways move (delta_e == 0) ga diitung sebagai kemajuan juga.
    no_change_counter = 0
    stuck_frequency = 0
    stuck_iterations = []

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

            if current_val > best_val:
                best_state = current_state.copy_state()
                best_val = current_val

        # nilai current berubah (naik, atau turun yg diterima) -> agen tidak stuck
        if accept and delta_e != 0:
            no_change_counter = 0
        else:
            # ditolak atau sideways -> nilai current tetap
            no_change_counter += 1
            # hitung 1x per episode stuck (saat pertama kali mencapai batas)
            if no_change_counter == stuck_limit:
                stuck_frequency += 1
                stuck_iterations.append(iteration)

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
        "stuck_iterations": stuck_iterations,
        "obj_history": obj_history,
        "best_obj_history": best_obj_history,
        "prob_iterations": prob_iterations,
        "prob_history": prob_history
    }