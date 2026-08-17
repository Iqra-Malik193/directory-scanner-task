from datetime import datetime
import math


class ParkingSession:

    def __init__(
        self,
        session_id,
        license_plate,
        spot_id,
        lot_id,
        check_in=None
    ):
        self.session_id = session_id
        self.license_plate = license_plate
        self.spot_id = spot_id
        self.lot_id = lot_id

        self.check_in = (
            check_in
            if check_in is not None
            else datetime.now()
        )

        self.check_out = None
        self.parking_fee = 0.0
        self.status = "ACTIVE"

    def end_session(self):
        self.check_out = datetime.now()
        self.status = "COMPLETED"

    def calculate_fee(self, hourly_rate):

        if self.check_out is None:
            return 0.0

        duration_seconds = (
            self.check_out - self.check_in
        ).total_seconds()

        duration_minutes = duration_seconds / 60

        # 10-minute grace period
        if duration_minutes <= 10:
            self.parking_fee = 0.0
            return self.parking_fee

        total_hours = math.ceil(
            duration_seconds / 3600
        )

        # First 24 hours
        if total_hours <= 24:

            fee = (
                total_hours
                * hourly_rate
            )

        else:

            normal_hours = 24

            extra_hours = (
                total_hours - 24
            )

            fee = (
                normal_hours
                * hourly_rate
            )

            fee += (
                extra_hours
                * hourly_rate
                * 1.5
            )

        self.parking_fee = round(
            fee,
            2
        )

        return self.parking_fee

    def to_dict(self):

        return {
            "session_id": self.session_id,
            "license_plate": self.license_plate,
            "spot_id": self.spot_id,
            "lot_id": self.lot_id,
            "check_in": self.check_in.isoformat(),
            "check_out": (
                self.check_out.isoformat()
                if self.check_out
                else None
            ),
            "parking_fee": self.parking_fee,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):

        check_in = datetime.fromisoformat(
            data["check_in"]
        )

        session = cls(
            data["session_id"],
            data["license_plate"],
            data["spot_id"],
            data["lot_id"],
            check_in
        )

        if data.get("check_out"):

            session.check_out = (
                datetime.fromisoformat(
                    data["check_out"]
                )
            )

        session.parking_fee = data.get(
            "parking_fee",
            0.0
        )

        session.status = data.get(
            "status",
            "ACTIVE"
        )

        return session