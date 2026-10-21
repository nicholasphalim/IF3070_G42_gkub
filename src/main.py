from models import Vehicle, Ship
from initial import generate_random_initial_state
from visualize import draw_grid_frame, clear_output_folder
from steepest import run_steepest_ascent

def main():
    print("=== PROGRAM OPTIMASI PARKIR KAPAL (STEEPEST ASCENT) ===")
    
    clear_output_folder()
    
    # Kapal 10x10, Beban Maksimal: 100 Ton
    kapal = Ship(10, 10, 100)
    
    # Daftar kendaraan mengantre (beragam berat dan tarif)
    daftar_kendaraan = [
        Vehicle("Mobil-A", 2, 3, 50, 15, 1),
        Vehicle("Mobil-B", 2, 3, 40, 10, 2),
        Vehicle("Truk-C", 3, 4, 120, 35, 1),
        Vehicle("Truk-D", 3, 4, 110, 30, 3),
        Vehicle("Minibus", 2, 4, 60, 20, 1),
        Vehicle("Fuso-E", 4, 4, 160, 40, 2),
        Vehicle("PickUp-F", 2, 2, 30, 10, 1),
        Vehicle("Truk-G", 3, 3, 90, 25, 2)
    ]
    
    print("\n1. Mengacak kondisi awal (Initial State)...")
    generate_random_initial_state(kapal, daftar_kendaraan)
    
    keuntungan_awal = kapal.get_total_fee()
    print(f"   Shipping Fee Awal: {keuntungan_awal} Juta")
    
    draw_grid_frame(kapal, iteration=0, current_fee=keuntungan_awal)
    
    print("\n2. Memulai algoritma Steepest Ascent...")
    run_steepest_ascent(kapal, daftar_kendaraan)
    print("\nSelesai! Silakan cek folder 'output/'")

if __name__ == "__main__":
    main()