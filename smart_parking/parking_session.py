from datetime import datetime

class ParkingSession:
    def __init__(self, session_id, vehicle, parking_spot):
        self.session_id = session_id
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.check_in = datetime.now()
        self.check_out = None

    def end_session(self):
        self.check_out = datetime.now()

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "vehicle": self.vehicle.license_plate,
            "parking_spot": self.parking_spot.spot_id,
            "check_in": str(self.check_in),
            "check_out": str(self.check_out)
        }