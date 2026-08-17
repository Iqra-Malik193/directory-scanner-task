class ParkingSpot:

    def __init__(
        self,
        spot_id,
        lot_id,
        spot_type,
        hourly_rate,
        kwh_rate=0
    ):
        self.spot_id = spot_id
        self.lot_id = lot_id
        self.spot_type = spot_type
        self.status = "AVAILABLE"
        self.hourly_rate = hourly_rate
        self.kwh_rate = kwh_rate

    def to_dict(self):
        return {
            "spot_id": self.spot_id,
            "lot_id": self.lot_id,
            "spot_type": self.spot_type,
            "status": self.status,
            "hourly_rate": self.hourly_rate,
            "kwh_rate": self.kwh_rate
        }

    @classmethod
    def from_dict(cls, data):

        spot = cls(
            data["spot_id"],
            data["lot_id"],
            data["spot_type"],
            data["hourly_rate"],
            data.get("kwh_rate", 0)
        )

        spot.status = data.get(
            "status",
            "AVAILABLE"
        )

        return spot