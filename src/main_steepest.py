from main import get_default_problem
from state import ShipState
from algo.steepest import run_steepest_ascent

def main():
    ship, vehicles = get_default_problem()
    
    initial_state = ShipState(ship, vehicles)
    
    result = run_steepest_ascent(
        initial_state=initial_state, 
        max_iterations=500, 
        num_neighbors=50
    )
    
    print("\n--- HASIL EKSKUSI STEEPEST ASCENT ---")
    print(f"Nilai Awal    : {result['initial_value']}")
    print(f"Nilai Akhir   : {result['best_value']}")
    print(f"Total Iterasi : {result['iterations']}")
    print(f"Waktu Eksekusi: {round(result['duration'], 4)} detik")
    print(f"Status Valid  : {result['best_state'].is_valid()}")

if __name__ == "__main__":
    main()