import json
import os
import tempfile
from datetime import datetime

from parking_lot import ParkingLot
from parking_spot import ParkingSpot
from vehicle import Vehicle
from parking_session import ParkingSession
from charging_session import ChargingSession

from exceptions import (
    DuplicateLotError,
    DuplicateSpotError,
    DuplicateVehicleError,
    LotNotFoundError,
    SpotNotFoundError,
    VehicleNotFoundError,
    VehicleAlreadyCheckedInError,
    NoAvailableSpotError,
    IncompatibleSpotError,
    SessionNotFoundError,
    SessionAlreadyCompletedError,
    InvalidRateError,
    SpotOccupiedError,
    ChargingSessionAlreadyActiveError,
    ChargingSessionNotActiveError,
    InvalidChargingMeterError,
    InvalidSpotTypeError,
    InvalidVehicleTypeError,
    InvalidStatusError,
)


class FacilityManager:

    def __init__(self):
        self.parking_lots = []
        self.parking_spots = []
        self.vehicles = []
        self.parking_sessions = []
        self.charging_sessions = []

        self.data_folder = "data"

        self.lots_file = os.path.join(
            self.data_folder, "lots.json"
        )
        self.spots_file = os.path.join(
            self.data_folder, "spots.json"
        )
        self.vehicles_file = os.path.join(
            self.data_folder, "vehicles.json"
        )
        self.parking_sessions_file = os.path.join(
            self.data_folder, "parking_sessions.json"
        )
        self.charging_sessions_file = os.path.join(
            self.data_folder, "charging_sessions.json"
        )

        self._create_data_folder()
        self.load_all_data()

    # =====================================================
    # JSON / FILE STORAGE
    # =====================================================

    def _create_data_folder(self):
        os.makedirs(self.data_folder, exist_ok=True)

    def _atomic_write(self, filename, data):
        directory = os.path.dirname(filename)

        if directory:
            os.makedirs(directory, exist_ok=True)

        fd, temp_file = tempfile.mkstemp(
            dir=directory or ".",
            text=True
        )

        try:
            with os.fdopen(fd, "w") as file:
                json.dump(
                    data,
                    file,
                    indent=4
                )

            os.replace(temp_file, filename)

        except Exception:
            if os.path.exists(temp_file):
                os.remove(temp_file)

            raise

    def _read_json(self, filename):

        if not os.path.exists(filename):
            return []

        try:
            with open(filename, "r") as file:
                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except (json.JSONDecodeError, OSError):
            return []

    def save_all_data(self):

        self._atomic_write(
            self.lots_file,
            [
                lot.to_dict()
                for lot in self.parking_lots
            ]
        )

        self._atomic_write(
            self.spots_file,
            [
                spot.to_dict()
                for spot in self.parking_spots
            ]
        )

        self._atomic_write(
            self.vehicles_file,
            [
                vehicle.to_dict()
                for vehicle in self.vehicles
            ]
        )

        self._atomic_write(
            self.parking_sessions_file,
            [
                session.to_dict()
                for session in self.parking_sessions
            ]
        )

        self._atomic_write(
            self.charging_sessions_file,
            [
                session.to_dict()
                for session in self.charging_sessions
            ]
        )

    def load_all_data(self):

        lots_data = self._read_json(
            self.lots_file
        )

        self.parking_lots = [
            ParkingLot.from_dict(data)
            for data in lots_data
        ]

        spots_data = self._read_json(
            self.spots_file
        )

        self.parking_spots = [
            ParkingSpot.from_dict(data)
            for data in spots_data
        ]

        vehicles_data = self._read_json(
            self.vehicles_file
        )

        self.vehicles = [
            Vehicle.from_dict(data)
            for data in vehicles_data
        ]

        sessions_data = self._read_json(
            self.parking_sessions_file
        )

        self.parking_sessions = [
            ParkingSession.from_dict(data)
            for data in sessions_data
        ]

        charging_data = self._read_json(
            self.charging_sessions_file
        )

        self.charging_sessions = [
            ChargingSession.from_dict(data)
            for data in charging_data
        ]

    # =====================================================
    # PARKING LOT
    # =====================================================

    def add_parking_lot(
        self,
        lot_id,
        name,
        location
    ):

        for lot in self.parking_lots:
            if lot.lot_id == lot_id:
                raise DuplicateLotError(
                    f"Lot ID '{lot_id}' already exists."
                )

        lot = ParkingLot(
            lot_id,
            name,
            location
        )

        self.parking_lots.append(lot)

        self.save_all_data()

        return lot

    def get_lot(self, lot_id):

        for lot in self.parking_lots:
            if lot.lot_id == lot_id:
                return lot

        raise LotNotFoundError(
            f"Parking lot '{lot_id}' not found."
        )

    def get_all_lots(self):
        return self.parking_lots

    # =====================================================
    # PARKING SPOT
    # =====================================================

    def add_parking_spot(
        self,
        lot_id,
        spot_id,
        spot_type,
        hourly_rate,
        kwh_rate=0
    ):

        spot_type = spot_type.upper()

        if spot_type not in [
            "REGULAR",
            "HANDICAPPED",
            "EV"
        ]:
            raise InvalidSpotTypeError(
                "Spot type must be REGULAR, "
                "HANDICAPPED or EV."
            )

        if hourly_rate <= 0:
            raise InvalidRateError(
                "Hourly rate must be greater than zero."
            )

        if spot_type == "EV" and kwh_rate <= 0:
            raise InvalidRateError(
                "EV spot must have a positive kWh rate."
            )

        if spot_type != "EV":
            kwh_rate = 0

        lot = self.get_lot(lot_id)

        for spot in self.parking_spots:
            if spot.spot_id == spot_id:
                raise DuplicateSpotError(
                    f"Spot ID '{spot_id}' already exists."
                )

        spot = ParkingSpot(
            spot_id,
            lot_id,
            spot_type,
            hourly_rate,
            kwh_rate
        )

        self.parking_spots.append(spot)

        lot.add_spot(spot_id)

        self.save_all_data()

        return spot

    def get_spot(self, spot_id):

        for spot in self.parking_spots:
            if spot.spot_id == spot_id:
                return spot

        raise SpotNotFoundError(
            f"Parking spot '{spot_id}' not found."
        )

    def update_spot(
        self,
        spot_id,
        spot_type=None,
        hourly_rate=None,
        kwh_rate=None,
        status=None
    ):

        spot = self.get_spot(spot_id)

        if hourly_rate is not None:

            if hourly_rate <= 0:
                raise InvalidRateError(
                    "Hourly rate must be greater than zero."
                )

            spot.hourly_rate = hourly_rate

        if spot_type is not None:

            spot_type = spot_type.upper()

            if spot_type not in [
                "REGULAR",
                "HANDICAPPED",
                "EV"
            ]:
                raise InvalidSpotTypeError(
                    "Invalid spot type."
                )

            spot.spot_type = spot_type

        if kwh_rate is not None:

            if kwh_rate <= 0:
                raise InvalidRateError(
                    "kWh rate must be greater than zero."
                )

            spot.kwh_rate = kwh_rate

        if status is not None:

            status = status.upper()

            if status not in [
                "AVAILABLE",
                "OCCUPIED",
                "OUT_OF_SERVICE"
            ]:
                raise InvalidStatusError(
                    "Invalid spot status."
                )

            spot.status = status

        self.save_all_data()

        return spot

    def delete_spot(self, spot_id):

        spot = self.get_spot(spot_id)

        if spot.status == "OCCUPIED":
            raise SpotOccupiedError(
                "Cannot delete an occupied spot."
            )

        self.parking_spots.remove(spot)

        lot = self.get_lot(spot.lot_id)

        if spot_id in lot.spot_ids:
            lot.spot_ids.remove(spot_id)

        self.save_all_data()

    # =====================================================
    # VEHICLE
    # =====================================================

    def register_vehicle(
        self,
        license_plate,
        owner_name,
        vehicle_type,
        registration_date=None
    ):

        vehicle_type = vehicle_type.upper()

        if vehicle_type not in [
            "CAR",
            "MOTORCYCLE",
            "EV_CAR"
        ]:
            raise InvalidVehicleTypeError(
                "Vehicle type must be CAR, "
                "MOTORCYCLE or EV_CAR."
            )

        for vehicle in self.vehicles:

            if (
                vehicle.license_plate.upper()
                == license_plate.upper()
            ):
                raise DuplicateVehicleError(
                    f"License plate '{license_plate}' "
                    "already exists."
                )

        if registration_date is None:
            registration_date = (
                datetime.now()
                .date()
                .isoformat()
            )

        vehicle = Vehicle(
            license_plate.upper(),
            owner_name,
            vehicle_type,
            registration_date
        )

        self.vehicles.append(vehicle)

        self.save_all_data()

        return vehicle

    def get_vehicle(self, license_plate):

        for vehicle in self.vehicles:

            if (
                vehicle.license_plate.upper()
                == license_plate.upper()
            ):
                return vehicle

        raise VehicleNotFoundError(
            f"Vehicle '{license_plate}' not found."
        )

    def get_all_vehicles(self):
        return self.vehicles

    # =====================================================
    # VEHICLE CHECK-IN
    # =====================================================

    def vehicle_check_in(
        self,
        license_plate,
        lot_id
    ):

        vehicle = self.get_vehicle(
            license_plate
        )

        for session in self.parking_sessions:

            if (
                session.license_plate.upper()
                == vehicle.license_plate.upper()
                and session.status == "ACTIVE"
            ):
                raise VehicleAlreadyCheckedInError(
                    f"Vehicle '{license_plate}' "
                    "is already checked in."
                )

        self.get_lot(lot_id)

        compatible_spot = None

        for spot in self.parking_spots:

            if spot.lot_id != lot_id:
                continue

            if spot.status != "AVAILABLE":
                continue

            if vehicle.vehicle_type == "EV_CAR":

                if spot.spot_type == "EV":
                    compatible_spot = spot
                    break

            else:

                if spot.spot_type in [
                    "REGULAR",
                    "HANDICAPPED"
                ]:
                    compatible_spot = spot
                    break

        if compatible_spot is None:
            raise NoAvailableSpotError(
                "No compatible available spot "
                "is available in this lot."
            )

        session_id = (
            f"S{len(self.parking_sessions) + 1:04d}"
        )

        session = ParkingSession(
            session_id,
            vehicle.license_plate,
            compatible_spot.spot_id,
            compatible_spot.lot_id
        )

        self.parking_sessions.append(session)

        compatible_spot.status = "OCCUPIED"

        self.save_all_data()

        return session

    # =====================================================
    # VEHICLE CHECK-OUT
    # =====================================================

    def vehicle_check_out(self, session_id):

        session = None

        for item in self.parking_sessions:

            if item.session_id == session_id:
                session = item
                break

        if session is None:
            raise SessionNotFoundError(
                f"Session '{session_id}' not found."
            )

        if session.status == "COMPLETED":
            raise SessionAlreadyCompletedError(
                "This session has already been completed."
            )

        for charging in self.charging_sessions:

            if (
                charging.parking_session_id
                == session.session_id
                and charging.status == "ACTIVE"
            ):
                raise ChargingSessionAlreadyActiveError(
                    "Stop the active charging session "
                    "before checking out."
                )

        spot = self.get_spot(
            session.spot_id
        )

        session.end_session()

        fee = session.calculate_fee(
            spot.hourly_rate
        )

        spot.status = "AVAILABLE"

        self.save_all_data()

        return session

    # =====================================================
    # EV CHARGING
    # =====================================================

    def start_charging(
        self,
        session_id,
        start_meter
    ):

        if start_meter < 0:
            raise InvalidChargingMeterError(
                "Start meter cannot be negative."
            )

        session = None

        for item in self.parking_sessions:

            if item.session_id == session_id:
                session = item
                break

        if session is None:
            raise SessionNotFoundError(
                "Parking session not found."
            )

        if session.status != "ACTIVE":
            raise SessionAlreadyCompletedError(
                "Cannot start charging on a "
                "completed parking session."
            )

        spot = self.get_spot(
            session.spot_id
        )

        if spot.spot_type != "EV":
            raise IncompatibleSpotError(
                "Charging is only available "
                "on EV spots."
            )

        for charging in self.charging_sessions:

            if (
                charging.parking_session_id
                == session_id
                and charging.status == "ACTIVE"
            ):
                raise ChargingSessionAlreadyActiveError(
                    "Charging session is already active."
                )

        charging_id = (
            f"C{len(self.charging_sessions) + 1:04d}"
        )

        charging = ChargingSession(
            charging_id,
            session_id,
            start_meter
        )

        self.charging_sessions.append(charging)

        self.save_all_data()

        return charging

    def stop_charging(
        self,
        session_id,
        end_meter
    ):

        if end_meter < 0:
            raise InvalidChargingMeterError(
                "End meter cannot be negative."
            )

        charging = None

        for item in self.charging_sessions:

            if (
                item.parking_session_id
                == session_id
                and item.status == "ACTIVE"
            ):
                charging = item
                break

        if charging is None:
            raise ChargingSessionNotActiveError(
                "No active charging session found."
            )

        if end_meter < charging.start_meter:
            raise InvalidChargingMeterError(
                "End meter cannot be less "
                "than start meter."
            )

        session = None

        for item in self.parking_sessions:

            if item.session_id == session_id:
                session = item
                break

        if session is None:
            raise SessionNotFoundError(
                "Parking session not found."
            )

        spot = self.get_spot(
            session.spot_id
        )

        charging.stop_charging(end_meter)

        charging.calculate_cost(
            spot.kwh_rate
        )

        self.save_all_data()

        return charging

    # =====================================================
    # VEHICLE STATUS
    # =====================================================

    def vehicle_status(self, license_plate):

        vehicle = self.get_vehicle(
            license_plate
        )

        for session in self.parking_sessions:

            if (
                session.license_plate.upper()
                == vehicle.license_plate.upper()
                and session.status == "ACTIVE"
            ):

                return {
                    "license_plate":
                        vehicle.license_plate,
                    "owner_name":
                        vehicle.owner_name,
                    "vehicle_type":
                        vehicle.vehicle_type,
                    "status":
                        "PARKED",
                    "session_id":
                        session.session_id,
                    "lot_id":
                        session.lot_id,
                    "spot_id":
                        session.spot_id
                }

        return {
            "license_plate":
                vehicle.license_plate,
            "owner_name":
                vehicle.owner_name,
            "vehicle_type":
                vehicle.vehicle_type,
            "status":
                "NOT_PARKED"
        }

    # =====================================================
    # ACTIVE SESSIONS
    # =====================================================

    def active_sessions(self):

        return [
            session
            for session in self.parking_sessions
            if session.status == "ACTIVE"
        ]

    # =====================================================
    # VEHICLE HISTORY
    # =====================================================

    def vehicle_history(self, license_plate):

        vehicle = self.get_vehicle(
            license_plate
        )

        return [
            session
            for session in self.parking_sessions
            if (
                session.license_plate.upper()
                == vehicle.license_plate.upper()
            )
        ]

    # =====================================================
    # FACILITY REPORT
    # =====================================================

    def generate_report(self):

        total_lots = len(
            self.parking_lots
        )

        total_spots = len(
            self.parking_spots
        )

        spot_types = {
            "REGULAR": 0,
            "HANDICAPPED": 0,
            "EV": 0
        }

        spot_status = {
            "AVAILABLE": 0,
            "OCCUPIED": 0,
            "OUT_OF_SERVICE": 0
        }

        for spot in self.parking_spots:

            if spot.spot_type in spot_types:
                spot_types[
                    spot.spot_type
                ] += 1

            if spot.status in spot_status:
                spot_status[
                    spot.status
                ] += 1

        parking_revenue = sum(
            session.parking_fee
            for session in self.parking_sessions
        )

        charging_revenue = sum(
            charging.energy_cost
            for charging in self.charging_sessions
        )

        completed_sessions = [
            session
            for session in self.parking_sessions
            if session.status == "COMPLETED"
        ]

        total_duration = 0

        for session in completed_sessions:

            if session.check_out:

                duration = (
                    session.check_out
                    - session.check_in
                )

                total_duration += (
                    duration.total_seconds()
                    / 3600
                )

        if completed_sessions:

            average_duration = (
                total_duration
                / len(completed_sessions)
            )

        else:
            average_duration = 0

        lot_session_count = {}

        for session in self.parking_sessions:

            lot_session_count[
                session.lot_id
            ] = (
                lot_session_count.get(
                    session.lot_id,
                    0
                ) + 1
            )

        if lot_session_count:

            busiest_lot = max(
                lot_session_count,
                key=lot_session_count.get
            )

        else:
            busiest_lot = "N/A"

        vehicle_spending = {}

        for session in self.parking_sessions:

            plate = session.license_plate

            vehicle_spending[plate] = (
                vehicle_spending.get(
                    plate,
                    0
                )
                + session.parking_fee
            )

        for charging in self.charging_sessions:

            for session in self.parking_sessions:

                if (
                    session.session_id
                    == charging.parking_session_id
                ):

                    plate = session.license_plate

                    vehicle_spending[plate] = (
                        vehicle_spending.get(
                            plate,
                            0
                        )
                        + charging.energy_cost
                    )

        top_vehicles = sorted(
            vehicle_spending.items(),
            key=lambda item: item[1],
            reverse=True
        )[:3]

        active_sessions_count = len(
            self.active_sessions()
        )

        active_charging_count = len([
            charging
            for charging in self.charging_sessions
            if charging.status == "ACTIVE"
        ])

        timestamp = datetime.now().isoformat()

        report = f"""
SMART PARKING FACILITY REPORT
=============================

Generated At: {timestamp}

Total Lots: {total_lots}
Total Spots: {total_spots}

SPOT BREAKDOWN BY TYPE
----------------------
REGULAR: {spot_types["REGULAR"]}
HANDICAPPED: {spot_types["HANDICAPPED"]}
EV: {spot_types["EV"]}

SPOT BREAKDOWN BY STATUS
------------------------
AVAILABLE: {spot_status["AVAILABLE"]}
OCCUPIED: {spot_status["OCCUPIED"]}
OUT_OF_SERVICE: {spot_status["OUT_OF_SERVICE"]}

REVENUE
-------
Parking Revenue: Rs. {parking_revenue:.2f}
Charging Revenue: Rs. {charging_revenue:.2f}
Total Revenue: Rs. {
    parking_revenue + charging_revenue
:.2f}

Average Session Duration:
{average_duration:.2f} hours

Busiest Lot:
{busiest_lot}

TOP THREE VEHICLES BY SPENDING
------------------------------
"""

        if top_vehicles:

            for index, (plate, amount) in enumerate(
                top_vehicles,
                start=1
            ):

                report += (
                    f"{index}. {plate} - "
                    f"Rs. {amount:.2f}\n"
                )

        else:

            report += (
                "No spending data available.\n"
            )

        report += f"""
Currently Active Sessions:
{active_sessions_count}

Currently Active Charging Sessions:
{active_charging_count}
"""

        with open(
            "facility_report.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report)

        return report