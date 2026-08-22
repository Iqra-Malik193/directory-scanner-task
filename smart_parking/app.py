from flask import Flask, request, jsonify

from facility_manager import FacilityManager


app = Flask(__name__)

# Facility Manager
manager = FacilityManager()


# =====================================================
# HOME / API INFO
# =====================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Smart Parking Lot & EV Charging Station API",
        "status": "running",
        "endpoints": {
            "lots": "/lots",
            "spots": "/spots",
            "vehicles": "/vehicles",
            "check_in": "/check-in",
            "check_out": "/check-out",
            "start_charging": "/charging/start",
            "stop_charging": "/charging/stop",
            "vehicle_status": "/vehicles/<license_plate>/status",
            "vehicle_history": "/vehicles/<license_plate>/history",
            "active_sessions": "/sessions/active",
            "report": "/report"
        }
    })


# =====================================================
# PARKING LOTS
# =====================================================

@app.route("/lots", methods=["GET"])
def get_lots():
    lots = manager.get_all_lots()

    return jsonify([
        lot.to_dict() for lot in lots
    ])


@app.route("/lots", methods=["POST"])
def add_lot():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    try:
        lot = manager.add_parking_lot(
            data["lot_id"],
            data["name"],
            data["location"]
        )

        return jsonify({
            "message": "Parking lot added successfully",
            "lot": lot.to_dict()
        }), 201

    except KeyError as e:
        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =====================================================
# PARKING SPOTS
# =====================================================

@app.route("/spots", methods=["GET"])
def get_spots():
    return jsonify([
        spot.to_dict()
        for spot in manager.parking_spots
    ])


@app.route("/spots", methods=["POST"])
def add_spot():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    try:
        spot = manager.add_parking_spot(
            data["lot_id"],
            data["spot_id"],
            data["spot_type"],
            float(data["hourly_rate"]),
            float(data.get("kwh_rate", 0))
        )

        return jsonify({
            "message": "Parking spot added successfully",
            "spot": spot.to_dict()
        }), 201

    except KeyError as e:
        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =====================================================
# VEHICLES
# =====================================================

@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    return jsonify([
        vehicle.to_dict()
        for vehicle in manager.get_all_vehicles()
    ])


@app.route("/vehicles", methods=["POST"])
def register_vehicle():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    try:
        vehicle = manager.register_vehicle(
            data["license_plate"],
            data["owner_name"],
            data["vehicle_type"],
            data.get("registration_date")
        )

        return jsonify({
            "message": "Vehicle registered successfully",
            "vehicle": vehicle.to_dict()
        }), 201

    except KeyError as e:
        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =====================================================
# VEHICLE CHECK-IN
# =====================================================

@app.route("/check-in", methods=["POST"])
def vehicle_check_in():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    try:
        session = manager.vehicle_check_in(
            data["license_plate"],
            data["lot_id"]
        )

        return jsonify({
            "message": "Vehicle checked in successfully",
            "session": session.to_dict()
        }), 201

    except KeyError as e:
        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =====================================================
# VEHICLE CHECK-OUT
# =====================================================

@app.route("/check-out", methods=["POST"])
def vehicle_check_out():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    try:
        session = manager.vehicle_check_out(
            data["session_id"]
        )

        return jsonify({
            "message": "Vehicle checked out successfully",
            "session": session.to_dict(),
            "parking_fee": session.parking_fee
        })

    except KeyError as e:
        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =====================================================
# EV CHARGING - START
# =====================================================

@app.route("/charging/start", methods=["POST"])
def start_charging():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    try:
        charging = manager.start_charging(
            data["session_id"],
            float(data["start_meter"])
        )

        return jsonify({
            "message": "EV charging started successfully",
            "charging_session": charging.to_dict()
        }), 201

    except KeyError as e:
        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =====================================================
# EV CHARGING - STOP
# =====================================================

@app.route("/charging/stop", methods=["POST"])
def stop_charging():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    try:
        charging = manager.stop_charging(
            data["session_id"],
            float(data["end_meter"])
        )

        return jsonify({
            "message": "EV charging stopped successfully",
            "charging_session": charging.to_dict(),
            "energy_consumed": charging.energy_consumed,
            "energy_cost": charging.energy_cost
        })

    except KeyError as e:
        return jsonify({
            "error": f"Missing field: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =====================================================
# VEHICLE STATUS
# =====================================================

@app.route("/vehicles/<license_plate>/status", methods=["GET"])
def vehicle_status(license_plate):
    try:
        status = manager.vehicle_status(
            license_plate
        )

        return jsonify(status)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 404


# =====================================================
# VEHICLE HISTORY
# =====================================================

@app.route("/vehicles/<license_plate>/history", methods=["GET"])
def vehicle_history(license_plate):
    try:
        history = manager.vehicle_history(
            license_plate
        )

        return jsonify([
            session.to_dict()
            for session in history
        ])

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 404


# =====================================================
# ACTIVE PARKING SESSIONS
# =====================================================

@app.route("/sessions/active", methods=["GET"])
def active_sessions():
    sessions = manager.active_sessions()

    return jsonify([
        session.to_dict()
        for session in sessions
    ])


# =====================================================
# FACILITY REPORT
# =====================================================

@app.route("/report", methods=["GET"])
def facility_report():
    report = manager.generate_report()

    return jsonify({
        "report": report
    })


# =====================================================
# RUN FLASK SERVER
# =====================================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )