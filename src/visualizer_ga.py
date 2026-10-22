# Referensi: Salindia Kuliah IF3070 Dasar Inteligensi Artifisial - Beyond Classical Search: Genetic Algorithm (Russell & Norvig, 2010)

import matplotlib.pyplot as plt


def save_ga_plot(result, label, filename):
    iterations = list(range(len(result["max_obj_history"])))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(iterations, result["max_obj_history"], label="Max Objective", color="green")
    ax.plot(iterations, result["avg_obj_history"], label="Rata-rata Objective", color="blue", alpha=0.7)
    ax.set_title(f"Genetic Algorithm {label}\nPopulasi = {result['population_size']}, Iterasi = {result['iterations']}, Durasi = {result['duration']:.3f} s")
    ax.set_xlabel("Iterasi (Generasi)")
    ax.set_ylabel("Objective Value")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
