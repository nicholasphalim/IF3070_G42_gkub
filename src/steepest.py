import copy
from visualize import draw_grid_frame, draw_performance_graph, create_animation_gif

def remove_vehicle_from_ship(ship, vehicle_id):
    """Menghapus 1 kendaraan dari grid kapal."""
    if vehicle_id in ship.placed_vehicles:
        data = ship.placed_vehicles[vehicle_id]
        v = data['vehicle']
        r_start, c_start = data['r'], data['c']
        
        v_length = v.length if v.orientation == 'H' else v.width
        v_width = v.width if v.orientation == 'H' else v.length
        
        for r in range(r_start, r_start + v_length):
            for c in range(c_start, c_start + v_width):
                ship.grid[r][c] = None
                
        ship.current_weight -= v.weight
        del ship.placed_vehicles[vehicle_id]

def get_best_neighbor(current_ship, list_of_vehicles):
    """Mencari 1 tetangga terbaik (Steepest Ascent)."""
    best_ship = current_ship
    best_fee = current_ship.get_total_fee()
    ada_yang_lebih_baik = False

    parked_ids = list(current_ship.placed_vehicles.keys())
    unparked_vehicles = [v for v in list_of_vehicles if v.id not in parked_ids]

    # AKSI 1: Masukkan kendaraan dari antrean luar ke ruang kosong
    for v_luar in unparked_vehicles:
        for orientasi in ['H', 'V']:
            for r in range(current_ship.length):
                for c in range(current_ship.width):
                    kapal_uji = copy.deepcopy(current_ship)
                    v_copy = copy.deepcopy(v_luar)
                    v_copy.orientation = orientasi
                    
                    if kapal_uji.place_vehicle(v_copy, r, c):
                        untung = kapal_uji.get_total_fee()
                        if untung > best_fee:
                            best_fee = untung
                            best_ship = kapal_uji
                            ada_yang_lebih_baik = True

    # AKSI 2: Jika tidak bisa nambah langsung, SWAP dengan kendaraan di dalam
    if not ada_yang_lebih_baik:
        for vid in parked_ids:
            for v_luar in unparked_vehicles:
                for orientasi in ['H', 'V']:
                    for r in range(current_ship.length):
                        for c in range(current_ship.width):
                            kapal_uji = copy.deepcopy(current_ship)
                            remove_vehicle_from_ship(kapal_uji, vid)
                            
                            v_copy = copy.deepcopy(v_luar)
                            v_copy.orientation = orientasi
                            if kapal_uji.place_vehicle(v_copy, r, c):
                                untung = kapal_uji.get_total_fee()
                                if untung > best_fee:
                                    best_fee = untung
                                    best_ship = kapal_uji
                                    ada_yang_lebih_baik = True

    return best_ship, ada_yang_lebih_baik, best_fee

def run_steepest_ascent(initial_ship, list_of_vehicles):
    """Menjalankan algoritma Steepest Ascent dan menyimpan luaran visualisasi."""
    kapal_sekarang = initial_ship
    iterasi = 1
    fee_history = [kapal_sekarang.get_total_fee()]
    
    while True:
        kapal_baru, nemu_lebih_baik, untung_baru = get_best_neighbor(kapal_sekarang, list_of_vehicles)
        
        if not nemu_lebih_baik:
            print(f"\nPencarian Selesai! Berhenti di iterasi {iterasi-1} (Local Optimum).")
            break
            
        kapal_sekarang = kapal_baru
        fee_history.append(untung_baru)
        
        draw_grid_frame(kapal_sekarang, iterasi, untung_baru)
        print(f"Iterasi {iterasi}: Shipping Fee naik -> {untung_baru} Juta")
        iterasi += 1

    # Membuat file GIF animasi dan grafik evaluasi
    create_animation_gif()
    draw_performance_graph(fee_history)
    
    return kapal_sekarang