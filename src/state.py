import random

def generate_random_initial_state(ship, list_of_vehicles):
    """
    Membuat kondisi awal acak.
    Sengaja hanya memuat beberapa kendaraan awal agar kapal tidak langsung penuh,
    sehingga Steepest Ascent punya ruang untuk beriterasi secara bertahap.
    """
    # Acak urutan kendaraan
    shuffled_vehicles = list_of_vehicles.copy()
    random.shuffle(shuffled_vehicles)
    
    # Coba masukkan maksimal 3 kendaraan pertama saja di initial state
    count = 0
    for vehicle in shuffled_vehicles:
        if count >= 3:
            break
            
        vehicle.orientation = random.choice(['H', 'V'])
        for _ in range(30):
            rand_row = random.randint(0, ship.length - 1)
            rand_col = random.randint(0, ship.width - 1)
            
            if ship.place_vehicle(vehicle, rand_row, rand_col):
                count += 1
                break