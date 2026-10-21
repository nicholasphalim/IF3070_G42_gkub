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
    ship_data = data.get("ship", data.get("Ship", {}))
    if "Dimensions" in ship_data:
        dim = ship_data["Dimensions"]
        ship_w = dim.get("w", dim.get("width"))
        ship_l = dim.get("l", dim.get("length"))
    else:
        ship_w = ship_data.get("width", ship_data.get("w"))
        ship_l = ship_data.get("length", ship_data.get("l"))

    max_cap = ship_data.get("max_capacity", ship_data.get("MaxCapacity", ship_data.get("maxCapacity", 0)))
    ship = Ship(ship_w, ship_l, max_cap)

    vehicles = []
    veh_list = data.get("vehicles", data.get("Vehicles", []))
    for v in veh_list:
        v_id = v.get("id", v.get("ID", ""))
        if "Dimensions" in v:
            dim = v["Dimensions"]
            vw = dim.get("w", dim.get("width"))
            vl = dim.get("l", dim.get("length"))
        else:
            vw = v.get("width", v.get("w"))
            vl = v.get("length", v.get("l"))

        fee = v.get("shipping_fee", v.get("ShippingFee", v.get("shippingFee", 0)))
        weight = v.get("weight", v.get("Weight", 0))
        eta = v.get("eta", v.get("ETA", 0))

        veh = Vehicle(v_id, vw, vl, fee, weight, eta)
        vehicles.append(veh)

    return ship, vehicles