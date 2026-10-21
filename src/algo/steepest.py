import time

def run_steepest_ascent(initial_state, max_iterations=1000, num_neighbors=50):
    start_time = time.time()
    
    current_state = initial_state
    current_value = current_state.get_objective_value()
    
    obj_history = [current_value]
    iterations = 0
    
    print(f"Mulai Steepest Ascent (Initial Value: {current_value})")
    
    for i in range(max_iterations):
        iterations += 1
        best_neighbor = None
        best_neighbor_value = -float('inf')
        
        for _ in range(num_neighbors):
            neighbor = current_state.get_random_neighbor()
            val = neighbor.get_objective_value()
            
            if val > best_neighbor_value:
                best_neighbor = neighbor
                best_neighbor_value = val
                
        if best_neighbor_value > current_value:
            current_state = best_neighbor
            current_value = best_neighbor_value
            obj_history.append(current_value)
        else:
            print(f"Local Optimum tercapai pada iterasi {iterations}.")
            break

    duration = time.time() - start_time
    
    return {
        "initial_value": initial_state.get_objective_value(),
        "best_value": current_value,
        "best_state": current_state,
        "iterations": iterations,
        "duration": duration,
        "obj_history": obj_history
    }