from parking_lot import ParkingLot
from parking_spot import ParkingSpot
from vehicle import Vehicle


class FacilityManager:
    def __init__(self):
        self.parking_lots = []
        self.vehicles = []

    # Add Parking Lot
    def add_parking_lot(self, lot_id, lot_name, capacity):
        lot = ParkingLot(lot_id, lot_name, capacity)
        self.parking_lots.append(lot)
        print("Parking Lot added successfully!")

    # Show Parking Lots
    def show_parking_lots(self):
        if not self.parking_lots:
            print("No Parking Lots Found!")
        else:
            for lot in self.parking_lots:
                print(f"ID: {lot.lot_id}, Name: {lot.lot_name}, Capacity: {lot.capacity}")

    # Register Vehicle
    def register_vehicle(self, license_plate, owner_name, vehicle_type, registration_date):
        vehicle = Vehicle(
            license_plate,
            owner_name,
            vehicle_type,
            registration_date
        )
        self.vehicles.append(vehicle)
        print("Vehicle Registered Successfully!")

    # Show Vehicles
    def show_vehicles(self):
        if not self.vehicles:
            print("No Vehicles Registered!")
        else:
            for vehicle in self.vehicles:
                print(
                    f"Plate: {vehicle.license_plate}, "
                    f"Owner: {vehicle.owner_name}, "
                    f"Type: {vehicle.vehicle_type}"
                )

    # Add Parking Spot
    def add_parking_spot(self, lot_id, spot_id, spot_type, hourly_rate):
        for lot in self.parking_lots:
            if lot.lot_id == lot_id:
                spot = ParkingSpot(spot_id, spot_type, hourly_rate)
                lot.add_spot(spot)
                return
        print("Parking Lot not found!")