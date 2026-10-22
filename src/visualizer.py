import matplotlib.pyplot as plt
import matplotlib.patches as patches

def save_sa_plots(result, run_number, filename):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    iterations = list(range(len(result["obj_history"])))

    # Grafik 1: Objective Function terhadap iterasi
    ax1.plot(iterations, result["obj_history"], label="Current Value", color="blue", alpha=0.6)
    ax1.plot(iterations, result["best_obj_history"], label="Best Value", color="orange", linestyle="--")
    # tandai iterasi saat stuck terdeteksi
    for k, it in enumerate(result.get("stuck_iterations", [])):
        ax1.axvline(it, color="gray", linestyle=":", alpha=0.8, label="Stuck terdeteksi" if k == 0 else None)
    ax1.set_title(f"Simulated Annealing Run {run_number} - Objective Value vs Iterations")
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Objective Value")
    ax1.legend()
    ax1.grid(True)

    # Grafik 2: e^(delta_E / T) terhadap iterasi (hanya untuk tetangga yang lebih buruk delta_E <= 0 sesuai materi kuliah)
    if result["prob_iterations"]:
        ax2.scatter(result["prob_iterations"], result["prob_history"], s=6, color="red", alpha=0.5, label=r"$e^{\Delta E / T}$ ($\Delta E \leq 0$)")
    ax2.set_title(f"Simulated Annealing Run {run_number} - Plot $e^{{\\Delta E / T}}$ vs Iterations")
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel(r"Probability $e^{\Delta E / T}$")
    ax2.set_ylim(-0.05, 1.05)
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def save_state_visualization(initial_state, final_state, run_number, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    colors = ["skyblue", "salmon", "lightgreen", "gold", "plum", "orange", "pink", "lightgray", "cyan", "khaki"]

    states = [(ax1, initial_state, "Initial State"), (ax2, final_state, "Final State")]

    for ax, state, title in states:
        ship = state.ship
        ax.set_xlim(0, ship.width)
        ax.set_ylim(0, ship.length)
        ax.set_aspect("equal")

        ax.set_xticks(range(ship.width + 1))
        ax.set_yticks(range(ship.length + 1))
        ax.grid(True, color="black", linewidth=0.5)

        unloaded_ids = []
        for i in range(len(state.vehicles)):
            v = state.vehicles[i]
            p = state.placements[i]

            if not p["is_loaded"]:
                unloaded_ids.append(v.id)
                continue

            w, l = state.get_vehicle_size(i)
            color = colors[i % len(colors)]

            rect = patches.Rectangle((p["x"], p["y"]), w, l, edgecolor="black", facecolor=color, alpha=0.8)
            ax.add_patch(rect)
            ax.text(p["x"] + w / 2, p["y"] + l / 2, v.id, ha="center", va="center", fontsize=9, fontweight="bold")

        val = state.get_objective_value()
        valid_text = "Valid" if state.is_valid() else "Tidak Valid"
        ax.set_title(f"{title} (Run {run_number})\nValue: {val} ({valid_text})")

        outside_str = ", ".join(unloaded_ids) if len(unloaded_ids) > 0 else "Tidak ada"
        ax.set_xlabel(f"Kendaraan di luar kapal: {outside_str}")

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    
def save_steepest_plots(result, run_number, filename):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Ambil obj_history sesuai dengan return dictionary dari algo/steepest.py
    history_data = result.get("obj_history", [])
    iterations = list(range(len(history_data)))

    ax.plot(iterations, history_data, label="Objective Value", color="green", linewidth=2)
    ax.set_title(f"Steepest Ascent Run {run_number} - Objective Value vs Iterations")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Objective Value")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()