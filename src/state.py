import copy
import random

class ShipState:
    def __init__(self, ship, vehicles, placements=None):
        self.ship = ship
        self.vehicles = vehicles

        if placements is None:
            self.placements = self.generate_random_placements()
        else:
            self.placements = placements

    def generate_random_placements(self):
        placements = []
        for v in self.vehicles:
            is_loaded = random.choice([True, False])
            orientation = random.choice(["Horizontal", "Vertical"])

            if orientation == "Horizontal":
                eff_w = v.width
                eff_l = v.length
            else:
                eff_w = v.length
                eff_l = v.width

            max_x = max(0, self.ship.width - eff_w)
            max_y = max(0, self.ship.length - eff_l)

            x = random.randint(0, max_x)
            y = random.randint(0, max_y)

            placements.append({
                "is_loaded": is_loaded,
                "x": x,
                "y": y,
                "orientation": orientation
            })
        return placements

    def copy_state(self):
        new_placements = copy.deepcopy(self.placements)
        return ShipState(self.ship, self.vehicles, new_placements)

    def get_vehicle_size(self, index):
        v = self.vehicles[index]
        ori = self.placements[index]["orientation"]
        if ori == "Horizontal":
            return v.width, v.length
        else:
            return v.length, v.width

    def get_objective_value(self):
        total_fee = 0
        total_weight = 0
        overlap_count = 0
        out_of_bounds_count = 0

        grid = []
        for r in range(self.ship.length):
            row = [0] * self.ship.width
            grid.append(row)

        for i in range(len(self.vehicles)):
            p = self.placements[i]
            if not p["is_loaded"]:
                continue

            v = self.vehicles[i]
            total_fee += v.shipping_fee
            total_weight += v.weight

            w, l = self.get_vehicle_size(i)

            for dx in range(w):
                for dy in range(l):
                    gx = p["x"] + dx
                    gy = p["y"] + dy

                    if gx < 0 or gx >= self.ship.width or gy < 0 or gy >= self.ship.length:
                        out_of_bounds_count += 1
                    else:
                        if grid[gy][gx] >= 1:
                            overlap_count += 1
                        grid[gy][gx] += 1

        excess_weight = 0
        if total_weight > self.ship.max_capacity:
            excess_weight = total_weight - self.ship.max_capacity

        penalty = (overlap_count * 500) + (out_of_bounds_count * 500) + (excess_weight * 200)
        return total_fee - penalty

    def is_valid(self):
        total_weight = 0
        grid = []
        for r in range(self.ship.length):
            grid.append([0] * self.ship.width)

        for i in range(len(self.vehicles)):
            p = self.placements[i]
            if not p["is_loaded"]:
                continue

            v = self.vehicles[i]
            total_weight += v.weight
            if total_weight > self.ship.max_capacity:
                return False

            w, l = self.get_vehicle_size(i)
            for dx in range(w):
                for dy in range(l):
                    gx = p["x"] + dx
                    gy = p["y"] + dy
                    if gx < 0 or gx >= self.ship.width or gy < 0 or gy >= self.ship.length:
                        return False
                    if grid[gy][gx] >= 1:
                        return False
                    grid[gy][gx] += 1
        return True

    def get_random_neighbor(self):
        neighbor = self.copy_state()
        n = len(neighbor.placements)
        if n == 0:
            return neighbor

        move_type = random.choice(["swap", "move", "rotate"])

        if move_type == "swap" and n >= 2:
            idx1, idx2 = random.sample(range(n), 2)
            p1 = neighbor.placements[idx1]
            p2 = neighbor.placements[idx2]

            p1["is_loaded"], p2["is_loaded"] = p2["is_loaded"], p1["is_loaded"]
            p1["x"], p2["x"] = p2["x"], p1["x"]
            p1["y"], p2["y"] = p2["y"], p1["y"]

        elif move_type == "rotate":
            idx = random.randint(0, n - 1)
            if neighbor.placements[idx]["orientation"] == "Horizontal":
                neighbor.placements[idx]["orientation"] = "Vertical"
            else:
                neighbor.placements[idx]["orientation"] = "Horizontal"

        else:
            idx = random.randint(0, n - 1)
            w, l = neighbor.get_vehicle_size(idx)

            max_x = max(0, self.ship.width - w)
            max_y = max(0, self.ship.length - l)

            neighbor.placements[idx]["x"] = random.randint(0, max_x)
            neighbor.placements[idx]["y"] = random.randint(0, max_y)

            if random.random() < 0.25:
                neighbor.placements[idx]["is_loaded"] = not neighbor.placements[idx]["is_loaded"]
            else:
                neighbor.placements[idx]["is_loaded"] = True

        return neighbor

    def to_dict(self):
        loaded = []
        unloaded = []
        total_weight = 0

        for i in range(len(self.vehicles)):
            v = self.vehicles[i]
            p = self.placements[i]
            info = {
                "id": v.id,
                "width": v.width,
                "length": v.length,
                "orientation": p["orientation"],
                "x": p["x"] if p["is_loaded"] else None,
                "y": p["y"] if p["is_loaded"] else None,
                "shipping_fee": v.shipping_fee,
                "weight": v.weight,
                "eta": v.eta
            }
            if p["is_loaded"]:
                loaded.append(info)
                total_weight += v.weight
            else:
                unloaded.append(info)

        return {
            "objective_value": self.get_objective_value(),
            "is_valid": self.is_valid(),
            "total_weight": total_weight,
            "loaded_vehicles": loaded,
            "unloaded_vehicles": unloaded
        }