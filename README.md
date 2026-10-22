# Tugas Besar 1 IF3070 Dasar Inteligensi Artifisial (Semester II 2025/2026)

## Optimasi Penempatan Kendaraan Kapal Kargo PT Owen Intim Line — Kelompok 42 (G42)

---

### Deskripsi Persoalan

Repositori ini berisi implementasi sistem pendukung keputusan berbasis **Local Search** untuk memecahkan persoalan optimasi penataan penempatan muatan kendaraan pada geladak kapal kargo PT Owen Intim Line.

Geladak kapal serta tiap kendaraan direpresentasikan sebagai grid 2 dimensi berkoordinat bilangan bulat. Suatu kendaraan dapat berorientasi horizontal maupun vertikal, dan tidak semua kendaraan wajib dimuat ke atas kapal (dapat berada di luar kapal).

**Tujuan (Objective Function):**

- Memaksimalkan total tarif pengiriman (`ShippingFee`) dari seluruh kendaraan yang berhasil dimuat di atas kapal.

**Batasan (Constraints):**

1. **No Overlapping**: Tidak boleh ada sel grid geladak kapal yang ditempati oleh lebih dari satu kendaraan.
2. **Within Boundaries**: Seluruh sel grid kendaraan yang dimuat harus berada di dalam batas dimensi geladak kapal.
3. **Max Capacity**: Total berat (`Weight`) seluruh kendaraan yang dimuat tidak boleh melebihi kapasitas beban maksimum kapal (`MaxCapacity`).

Algoritma yang diimplementasikan:

- **Steepest Ascent Hill Climbing**
- **Simulated Annealing**
- **Genetic Algorithm**

---

### Struktur Folder

```
IF3070_G42_gkub/
├── docs/                      # Dokumen laporan Tugas Besar
├── output/                    # Hasil eksekusi algoritma
├── src/                       # Seluruh source code Python
│   ├── algo/
│   │   ├── genetic_algorithm.py   # Implementasi Genetic Algorithm
│   │   ├── steepest.py            # Implementasi Steepest Ascent Hill Climbing
│   │   └── sim_annealing.py       # Implementasi Simulated Annealing
│   ├── data_generator.py          # Generator data uji dummy (kapal & kendaraan)
│   ├── entities.py                # Definisi entitas Vehicle, Ship, dan loader dataset
│   ├── main.py                    # Program utama dan runner seluruh eksperimen
│   ├── main_ga.py                 # Runner langsung untuk Genetic Algorithm
│   ├── main_sa.py                 # Runner langsung untuk Simulated Annealing
│   ├── main_steepest.py           # Runner langsung untuk Steepest Ascent Hill Climbing
│   ├── state.py                   # Representasi ShipState bersama
│   └── visualizer.py              # Visualisasi grid kapal dan grafik metrik
├── .gitignore
└── README.md
```

---

### Kebutuhan & Cara Setup

Program dibangun menggunakan bahasa Python (versi 3.10 ke atas) dan membutuhkan pustaka `matplotlib` untuk visualisasi grafik dan grid geladak kapal.

**Instalasi dependensi:**

```bash
pip install matplotlib
```

---

### Cara Menjalankan Program

Masuk terlebih dahulu ke dalam folder `src/`:

```bash
cd src
```

#### 1. Melalui Menu Interaktif Program Utama

Jalankan program utama:

```bash
python main.py
```

Pilih opsi algoritma yang ingin dijalankan:

- `1` : Hill-Climbing / Steepest Ascent
- `2` : Simulated Annealing
- `3` : Genetic Algorithm
- `4` : Keluar

Anda juga dapat langsung menyertakan argumen nomor pilihan:

```bash
python main.py 2   # Menjalankan Simulated Annealing
python main.py 3   # Menjalankan Genetic Algorithm
```

#### 2. Melalui Skrip Khusus Tiap Algoritma

Tersedia runner langsung untuk masing-masing algoritma:

- **Simulated Annealing**:
  ```bash
  python main_sa.py
  ```
- **Genetic Algorithm**:
  ```bash
  python main_ga.py
  ```

Hasil pengujian berupa gambar visualisasi grid geladak kapal, grafik konvergensi, file log JSON, dan ringkasan teks akan otomatis disimpan ke dalam folder `output/`.

---

### Pembagian Tugas Kelompok 42

|   NIM    |          Nama              | Pembagian Tugas                                                           |
| :------: | :-------------------------:| :------------------------------------------------------------------------ |
| 18224098 | Nicholas Putra Halim       | Implementasi Simulated Annealing, eksperimen SA, visualisasi SA & laporan |
| 18224038 | Brandon Zeko Alexander     | Implementasi Steepest Ascent Hill Climbing, eksperimen HC & laporan       |
| 18224118 | Christian Wilfredo Pakpahan| Implementasi Genetic Algorithm, eksperimen GA, visualisasi GA & laporan   |
