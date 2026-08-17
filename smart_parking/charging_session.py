from datetime import datetime


class ChargingSession:

    def __init__(
        self,
        charging_session_id,
        parking_session_id,
        start_meter,
        start_time=None
    ):
        self.charging_session_id = (
            charging_session_id
        )

        self.parking_session_id = (
            parking_session_id
        )

        self.start_time = (
            start_time
            if start_time is not None
            else datetime.now()
        )

        self.end_time = None

        self.start_meter = start_meter
        self.end_meter = None

        self.energy_cost = 0.0

        self.status = "ACTIVE"

    def stop_charging(self, end_meter):

        self.end_meter = end_meter
        self.end_time = datetime.now()
        self.status = "COMPLETED"

    def calculate_cost(self, kwh_rate):

        if self.end_meter is None:

            return 0.0

        energy_used = (
            self.end_meter
            - self.start_meter
        )

        self.energy_cost = round(
            energy_used * kwh_rate,
            2
        )

        return self.energy_cost

    def to_dict(self):

        return {
            "charging_session_id":
                self.charging_session_id,

            "parking_session_id":
                self.parking_session_id,

            "start_time":
                self.start_time.isoformat(),

            "end_time":
                (
                    self.end_time.isoformat()
                    if self.end_time
                    else None
                ),

            "start_meter":
                self.start_meter,

            "end_meter":
                self.end_meter,

            "energy_cost":
                self.energy_cost,

            "status":
                self.status
        }

    @classmethod
    def from_dict(cls, data):

        start_time = datetime.fromisoformat(
            data["start_time"]
        )

        charging = cls(
            data["charging_session_id"],
            data["parking_session_id"],
            data["start_meter"],
            start_time
        )

        if data.get("end_time"):

            charging.end_time = (
                datetime.fromisoformat(
                    data["end_time"]
                )
            )

        charging.end_meter = data.get(
            "end_meter"
        )

        charging.energy_cost = data.get(
            "energy_cost",
            0.0
        )

        charging.status = data.get(
            "status",
            "ACTIVE"
        )

        return charging