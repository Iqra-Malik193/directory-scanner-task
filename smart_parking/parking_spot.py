class ParkingSpot:
    def __init__(self, spot_id, spot_type, hourly_rate):
        self.spot_id = spot_id
        self.spot_type = spot_type      # REGULAR, HANDICAPPED, EV
        self.status = "AVAILABLE"
        self.hourly_rate = hourly_rate

    def to_dict(self):
        return {
            "spot_id": self.spot_id,
            "spot_type": self.spot_type,
            "status": self.status,
            "hourly_rate": self.hourly_rate
        }