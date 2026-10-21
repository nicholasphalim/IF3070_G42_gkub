class Vehicle:
    def __init__(self, vehicle_id, length, width, fee, weight, eta):
        self.id = vehicle_id
        self.length = length   
        self.width = width     
        self.fee = fee         
        self.weight = weight   
        self.eta = eta         
        self.orientation = 'H' 

class Ship:
    def __init__(self, grid_length, grid_width, max_capacity):
        self.length = grid_length
        self.width = grid_width
        self.max_capacity = max_capacity
        self.current_weight = 0
        self.grid = [[None for _ in range(grid_width)] for _ in range(grid_length)]
        self.placed_vehicles = {}

    def is_safe_to_place(self, vehicle, start_row, start_col):
        if self.current_weight + vehicle.weight > self.max_capacity:
            return False
            
        v_length = vehicle.length if vehicle.orientation == 'H' else vehicle.width
        v_width = vehicle.width if vehicle.orientation == 'H' else vehicle.length

        if start_row + v_length > self.length or start_col + v_width > self.width:
            return False

        for r in range(start_row, start_row + v_length):
            for c in range(start_col, start_col + v_width):
                if self.grid[r][c] is not None:
                    return False
        return True

    def place_vehicle(self, vehicle, start_row, start_col):
        if not self.is_safe_to_place(vehicle, start_row, start_col):
            return False
            
        v_length = vehicle.length if vehicle.orientation == 'H' else vehicle.width
        v_width = vehicle.width if vehicle.orientation == 'H' else vehicle.length

        for r in range(start_row, start_row + v_length):
            for c in range(start_col, start_col + v_width):
                self.grid[r][c] = vehicle.id
                
        self.current_weight += vehicle.weight
        self.placed_vehicles[vehicle.id] = {'vehicle': vehicle, 'r': start_row, 'c': start_col}
        return True

    def get_total_fee(self):
        return sum(data['vehicle'].fee for data in self.placed_vehicles.values())