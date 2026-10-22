# Referensi: Salindia Kuliah IF3070 Dasar Inteligensi Artifisial - Beyond Classical Search: Genetic Algorithm (Russell & Norvig, 2010)

import os
import sys
import json
import random
from entities import load_problem_from_dict


def generate_dummy_problem(n_vehicles=10, ship_width=10, ship_length=16, max_capacity=50, seed=None):
    rng = random.Random(seed)

    vehicles = []
    for i in range(n_vehicles):
        w = rng.randint(2, 5)
        l = rng.randint(2, 6)
        # fee dan berat kira-kira sebanding dengan luas kendaraan
        area = w * l
        vehicles.append({
            "id": f"V{i + 1}",
            "width": w,
            "length": l,
            "shipping_fee": area * 4 + rng.randint(-10, 20),
            "weight": max(1, area // 2 + rng.randint(-2, 2)),
            "eta": rng.randint(1, 7)
        })

    return {
        "ship": {
            "width": ship_width,
            "length": ship_length,
            "max_capacity": max_capacity
        },
        "vehicles": vehicles
    }


def save_problem(data, filepath):
    folder = os.path.dirname(filepath)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def load_problem(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return load_problem_from_dict(data)


if __name__ == "__main__":
    # contoh: python data_generator.py 12 ../data/dummy_12.json
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    path = sys.argv[2] if len(sys.argv) > 2 else f"../data/dummy_{n}.json"
    save_problem(generate_dummy_problem(n_vehicles=n, seed=42), path)
    print(f"Dataset tersimpan di {path}")
