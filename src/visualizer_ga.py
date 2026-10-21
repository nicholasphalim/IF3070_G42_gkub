# Referensi: Salindia Kuliah IF3070 Dasar Inteligensi Artifisial - Beyond Classical Search: Genetic Algorithm (Russell & Norvig, 2010)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


COLORS = ["skyblue", "salmon", "lightgreen", "gold", "plum", "orange", "pink", "lightgray", "cyan", "khaki"]


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


def get_state_text(state):
    lines = ["Di dalam kapal:"]
    outside = []
    for i in range(len(state.vehicles)):
        v = state.vehicles[i]
        p = state.placements[i]
        if p["is_loaded"]:
            w, l = state.get_vehicle_size(i)
            lines.append(f"  {v.id} ({w}x{l}) ({p['x']},{p['y']}) {p['orientation']}, fee={v.shipping_fee}, w={v.weight}")
        else:
            outside.append(v.id)
    if len(lines) == 1:
        lines.append("  Tidak ada")

    lines.append("")
    lines.append("Di luar kapal:")
    lines.append("  " + (", ".join(outside) if len(outside) > 0 else "Tidak ada"))

    info = state.to_dict()
    lines.append("")
    lines.append(f"Total berat: {info['total_weight']} / {state.ship.max_capacity}")
    lines.append(f"Objective  : {info['objective_value']}")
    return "\n".join(lines)


def draw_deck(ax, state, title):
    ship = state.ship
    ax.set_xlim(0, ship.width)
    ax.set_ylim(0, ship.length)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_xticks(range(ship.width + 1))
    ax.set_yticks(range(ship.length + 1))
    ax.tick_params(labelsize=7)
    ax.grid(True, color="black", linewidth=0.5)

    for i in range(len(state.vehicles)):
        p = state.placements[i]
        if not p["is_loaded"]:
            continue
        w, l = state.get_vehicle_size(i)
        rect = patches.Rectangle((p["x"], p["y"]), w, l, edgecolor="black", facecolor=COLORS[i % len(COLORS)], alpha=0.6)
        ax.add_patch(rect)
        ax.text(p["x"] + w / 2, p["y"] + l / 2, state.vehicles[i].id, ha="center", va="center", fontsize=9, fontweight="bold")

    valid_text = "Valid" if state.is_valid() else "Tidak Valid"
    ax.set_title(f"{title}\nValue: {state.get_objective_value()} ({valid_text})", fontsize=10)


def save_ga_state_visualization(initial_state, final_state, label, filename):
    fig, axes = plt.subplots(1, 4, figsize=(18, 7.5), gridspec_kw={"width_ratios": [1, 1.1, 1, 1.1]})

    pairs = [(initial_state, "State Awal"), (final_state, "State Akhir")]
    for k in range(2):
        state, title = pairs[k]
        draw_deck(axes[k * 2], state, title)
        text_ax = axes[k * 2 + 1]
        text_ax.axis("off")
        text_ax.text(0, 1, get_state_text(state), va="top", ha="left", fontsize=8, family="monospace")

    fig.suptitle(f"Genetic Algorithm {label}", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(filename)
    plt.close()
