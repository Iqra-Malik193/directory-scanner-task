class ParkingLot:
    def __init__(self, lot_id, lot_name, capacity):
        self.lot_id = lot_id
        self.lot_name = lot_name
        self.capacity = capacity
        self.spots = []

    def add_spot(self, spot):
        if len(self.spots) < self.capacity:
            self.spots.append(spot)
            print("Parking spot added successfully!")
        else:
            print("Parking lot is full!")

    def show_spots(self):
        if not self.spots:
            print("No parking spots available.")
        else:
            for spot in self.spots:
                print(
                    f"ID: {spot.spot_id}, "
                    f"Type: {spot.spot_type}, "
                    f"Status: {spot.status}, "
                    f"Rate: {spot.hourly_rate}"
                )