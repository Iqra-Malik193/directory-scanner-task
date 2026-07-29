from datetime import datetime

class ChargingSession:
    def __init__(self, session_id, vehicle):
        self.session_id = session_id
        self.vehicle = vehicle
        self.start_time = datetime.now()
        self.end_time = None

    def stop_charging(self):
        self.end_time = datetime.now()

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "vehicle": self.vehicle.license_plate,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time)
        }