class Vehicle:
    def __init__(self, id, width, length, shipping_fee, weight, eta):
        self.id = id
        self.width = width
        self.length = length
        self.shipping_fee = shipping_fee
        self.weight = weight
        self.eta = eta


class Ship:
    def __init__(self, width, length, max_capacity):
        self.width = width
        self.length = length
        self.max_capacity = max_capacity


def load_problem_from_dict(data):
    ship_data = data["ship"]
    ship = Ship(ship_data["width"], ship_data["length"], ship_data["max_capacity"])

    vehicles = []
    for v in data["vehicles"]:
        veh = Vehicle(v["id"], v["width"], v["length"], v["shipping_fee"], v["weight"], v["eta"])
        vehicles.append(veh)

    return ship, vehicles