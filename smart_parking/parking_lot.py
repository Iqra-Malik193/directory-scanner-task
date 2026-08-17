class ParkingLot:

    def __init__(self, lot_id, name, location):
        self.lot_id = lot_id
        self.name = name
        self.location = location
        self.spot_ids = []

    def add_spot(self, spot_id):
        if spot_id not in self.spot_ids:
            self.spot_ids.append(spot_id)

    def to_dict(self):
        return {
            "lot_id": self.lot_id,
            "name": self.name,
            "location": self.location,
            "spot_ids": self.spot_ids
        }

    @classmethod
    def from_dict(cls, data):
        lot = cls(
            data["lot_id"],
            data["name"],
            data["location"]
        )

        lot.spot_ids = data.get(
            "spot_ids",
            []
        )

        return lot