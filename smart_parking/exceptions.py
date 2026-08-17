class ParkingSystemError(Exception):
    """Base exception for Smart Parking System."""
    pass


# ==============================
# DUPLICATE ERRORS
# ==============================

class DuplicateLotError(ParkingSystemError):
    pass


class DuplicateSpotError(ParkingSystemError):
    pass


class DuplicateVehicleError(ParkingSystemError):
    pass


# ==============================
# NOT FOUND ERRORS
# ==============================

class LotNotFoundError(ParkingSystemError):
    pass


class SpotNotFoundError(ParkingSystemError):
    pass


class VehicleNotFoundError(ParkingSystemError):
    pass


class SessionNotFoundError(ParkingSystemError):
    pass


# ==============================
# VEHICLE ERRORS
# ==============================

class VehicleAlreadyCheckedInError(
    ParkingSystemError
):
    pass


class NoAvailableSpotError(
    ParkingSystemError
):
    pass


class IncompatibleSpotError(
    ParkingSystemError
):
    pass


class InvalidVehicleTypeError(
    ParkingSystemError
):
    pass


# ==============================
# SESSION ERRORS
# ==============================

class SessionAlreadyCompletedError(
    ParkingSystemError
):
    pass


# ==============================
# SPOT ERRORS
# ==============================

class SpotOccupiedError(
    ParkingSystemError
):
    pass


class InvalidSpotTypeError(
    ParkingSystemError
):
    pass


class InvalidStatusError(
    ParkingSystemError
):
    pass


class InvalidRateError(
    ParkingSystemError
):
    pass


# ==============================
# CHARGING ERRORS
# ==============================

class ChargingSessionAlreadyActiveError(
    ParkingSystemError
):
    pass


class ChargingSessionNotActiveError(
    ParkingSystemError
):
    pass


class InvalidChargingMeterError(
    ParkingSystemError
):
    pass