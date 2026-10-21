import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from PIL import Image

COLORS = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'lime', 'pink']
warna_mobil = {}

def clear_output_folder():
    """Mereset isi folder output sebelum running."""
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    if os.path.exists(output_dir):
        for file_name in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

def draw_grid_frame(ship, iteration, current_fee):
    """Menyimpan gambar frame per iterasi."""
    plt.figure(figsize=(6, 6))
    ax = plt.gca()
    
    plt.title(f"Iterasi {iteration} | Total Shipping Fee: {current_fee} Juta", fontsize=11)
    
    ax.set_xlim(0, ship.width)
    ax.set_ylim(0, ship.length)
    ax.set_xticks(range(ship.width + 1))
    ax.set_yticks(range(ship.length + 1))
    ax.grid(True, linestyle='--')
    
    idx_warna = 0
    for vehicle_id, data in ship.placed_vehicles.items():
        if vehicle_id not in warna_mobil:
            warna_mobil[vehicle_id] = COLORS[idx_warna % len(COLORS)]
            idx_warna += 1
            
        v = data['vehicle']
        r = data['r']
        c = data['c']
        
        panjang = v.length if v.orientation == 'H' else v.width
        lebar = v.width if v.orientation == 'H' else v.length
        
        rect = patches.Rectangle((c, r), lebar, panjang, edgecolor='black', facecolor=warna_mobil[vehicle_id])
        ax.add_patch(rect)
        ax.text(c + lebar/2, r + panjang/2, vehicle_id, color='white', weight='bold', ha='center', va='center')

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    nama_file = os.path.join(output_dir, f"iterasi_{iteration}.png")
    plt.savefig(nama_file)
    plt.close()

def create_animation_gif():
    """
    Mengumpulkan seluruh file iterasi_X.png di folder output/
    lalu menggabungkannya menjadi 1 file animasi bergerak 'proses_animasi.gif'.
    """
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    
    # Ambil semua file iterasi_X.png dan urutkan berdasarkan angkanya
    files = [f for f in os.listdir(output_dir) if f.startswith('iterasi_') and f.endswith('.png')]
    files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    images = []
    for file_name in files:
        file_path = os.path.join(output_dir, file_name)
        images.append(Image.open(file_path))
        
    if images:
        gif_path = os.path.join(output_dir, "proses_animasi.gif")
        # Simpan menjadi GIF bergerak (durasi per frame: 800 ms = 0.8 detik)
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=800,
            loop=0
        )
        print("   -> Animasi bergerak berhasil dibuat: 'output/proses_animasi.gif'")

def draw_performance_graph(fee_history):
    """Membuat file grafik evaluasi nilai Objective Function."""
    plt.figure(figsize=(8, 4))
    plt.plot(range(len(fee_history)), fee_history, marker='o', color='b', linestyle='-')
    plt.title("Grafik Evaluasi Objective Function (Steepest Ascent)")
    plt.xlabel("Iterasi")
    plt.ylabel("Total Shipping Fee (Juta)")
    plt.grid(True)
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    nama_file = os.path.join(output_dir, "grafik_evaluasi.png")
    plt.savefig(nama_file)
    plt.close()