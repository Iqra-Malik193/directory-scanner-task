from facility_manager import FacilityManager


def main():

    manager = FacilityManager()

    while True:

        print("\n================================")
        print("   SMART PARKING SYSTEM")
        print("================================")

        print("1. Add Parking Lot")
        print("2. View Parking Lots")
        print("3. Add Parking Spot")
        print("4. View Parking Spots")
        print("5. Register Vehicle")
        print("6. View Vehicles")
        print("7. Vehicle Check-In")
        print("8. Vehicle Check-Out")
        print("9. Start EV Charging")
        print("10. Stop EV Charging")
        print("11. Vehicle Status")
        print("12. Active Sessions")
        print("13. Vehicle History")
        print("14. Update Parking Spot")
        print("15. Delete Parking Spot")
        print("16. Generate Facility Report")
        print("17. Exit")

        choice = input("\nEnter your choice: ").strip()

        # ==========================================
        # ADD PARKING LOT
        # ==========================================

        if choice == "1":

            try:
                lot_id = input("Enter Lot ID: ").strip()
                name = input("Enter Lot Name: ").strip()
                location = input("Enter Location: ").strip()

                manager.add_parking_lot(
                    lot_id,
                    name,
                    location
                )

                print("Parking Lot added successfully!")

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # VIEW PARKING LOTS
        # ==========================================

        elif choice == "2":

            lots = manager.get_all_lots()

            if not lots:
                print("No parking lots found.")

            else:

                print("\n----- PARKING LOTS -----")

                for lot in lots:

                    print(
                        f"ID: {lot.lot_id} | "
                        f"Name: {lot.name} | "
                        f"Location: {lot.location} | "
                        f"Spots: {len(lot.spot_ids)}"
                    )

        # ==========================================
        # ADD PARKING SPOT
        # ==========================================

        elif choice == "3":

            try:

                lot_id = input(
                    "Enter Lot ID: "
                ).strip()

                spot_id = input(
                    "Enter Spot ID: "
                ).strip()

                spot_type = input(
                    "Enter Spot Type "
                    "(REGULAR/HANDICAPPED/EV): "
                ).strip().upper()

                hourly_rate = float(
                    input("Enter Hourly Rate: ")
                )

                if spot_type == "EV":

                    kwh_rate = float(
                        input("Enter kWh Rate: ")
                    )

                else:

                    kwh_rate = 0

                manager.add_parking_spot(
                    lot_id,
                    spot_id,
                    spot_type,
                    hourly_rate,
                    kwh_rate
                )

                print(
                    "Parking Spot added successfully!"
                )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # VIEW PARKING SPOTS
        # ==========================================

        elif choice == "4":

            if not manager.parking_spots:

                print("No parking spots found.")

            else:

                print("\n----- PARKING SPOTS -----")

                for spot in manager.parking_spots:

                    print(
                        f"ID: {spot.spot_id} | "
                        f"Lot: {spot.lot_id} | "
                        f"Type: {spot.spot_type} | "
                        f"Status: {spot.status} | "
                        f"Hourly Rate: Rs. {spot.hourly_rate} | "
                        f"kWh Rate: Rs. {spot.kwh_rate}"
                    )

        # ==========================================
        # REGISTER VEHICLE
        # ==========================================

        elif choice == "5":

            try:

                plate = input(
                    "Enter License Plate: "
                ).strip()

                owner = input(
                    "Enter Owner Name: "
                ).strip()

                vehicle_type = input(
                    "Enter Vehicle Type "
                    "(CAR/MOTORCYCLE/EV_CAR): "
                ).strip().upper()

                registration_date = input(
                    "Enter Registration Date "
                    "(YYYY-MM-DD) "
                    "or press Enter for today: "
                ).strip()

                if registration_date == "":
                    registration_date = None

                manager.register_vehicle(
                    plate,
                    owner,
                    vehicle_type,
                    registration_date
                )

                print(
                    "Vehicle registered successfully!"
                )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # VIEW VEHICLES
        # ==========================================

        elif choice == "6":

            vehicles = manager.get_all_vehicles()

            if not vehicles:

                print("No vehicles registered.")

            else:

                print("\n----- VEHICLES -----")

                for vehicle in vehicles:

                    print(
                        f"Plate: {vehicle.license_plate} | "
                        f"Owner: {vehicle.owner_name} | "
                        f"Type: {vehicle.vehicle_type} | "
                        f"Registered: "
                        f"{vehicle.registration_date}"
                    )

        # ==========================================
        # VEHICLE CHECK-IN
        # ==========================================

        elif choice == "7":

            try:

                plate = input(
                    "Enter License Plate: "
                ).strip()

                lot_id = input(
                    "Enter Lot ID: "
                ).strip()

                session = manager.vehicle_check_in(
                    plate,
                    lot_id
                )

                print(
                    "\nVehicle Checked-In Successfully!"
                )

                print(
                    "Session ID:",
                    session.session_id
                )

                print(
                    "Spot ID:",
                    session.spot_id
                )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # VEHICLE CHECK-OUT
        # ==========================================

        elif choice == "8":

            try:

                session_id = input(
                    "Enter Session ID: "
                ).strip()

                session = manager.vehicle_check_out(
                    session_id
                )

                print(
                    "\nVehicle Checked-Out Successfully!"
                )

                print(
                    "Session ID:",
                    session.session_id
                )

                print(
                    "Parking Fee: Rs.",
                    session.parking_fee
                )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # START EV CHARGING
        # ==========================================

        elif choice == "9":

            try:

                session_id = input(
                    "Enter Parking Session ID: "
                ).strip()

                start_meter = float(
                    input(
                        "Enter Start Meter Reading (kWh): "
                    )
                )

                charging = manager.start_charging(
                    session_id,
                    start_meter
                )

                print(
                    "\nCharging Started Successfully!"
                )

                print(
                    "Charging Session ID:",
                    charging.charging_session_id
                )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # STOP EV CHARGING
        # ==========================================

        elif choice == "10":

            try:

                session_id = input(
                    "Enter Parking Session ID: "
                ).strip()

                end_meter = float(
                    input(
                        "Enter End Meter Reading (kWh): "
                    )
                )

                charging = manager.stop_charging(
                    session_id,
                    end_meter
                )

                print(
                    "\nCharging Stopped Successfully!"
                )

                print(
                    "Energy Cost: Rs.",
                    charging.energy_cost
                )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # VEHICLE STATUS
        # ==========================================

        elif choice == "11":

            try:

                plate = input(
                    "Enter License Plate: "
                ).strip()

                status = manager.vehicle_status(
                    plate
                )

                print("\n----- VEHICLE STATUS -----")

                for key, value in status.items():

                    print(
                        f"{key}: {value}"
                    )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # ACTIVE SESSIONS
        # ==========================================

        elif choice == "12":

            sessions = manager.active_sessions()

            if not sessions:

                print("No active sessions.")

            else:

                print(
                    "\n----- ACTIVE SESSIONS -----"
                )

                for session in sessions:

                    print(
                        f"Session: {session.session_id} | "
                        f"Vehicle: {session.license_plate} | "
                        f"Lot: {session.lot_id} | "
                        f"Spot: {session.spot_id}"
                    )

        # ==========================================
        # VEHICLE HISTORY
        # ==========================================

        elif choice == "13":

            try:

                plate = input(
                    "Enter License Plate: "
                ).strip()

                history = manager.vehicle_history(
                    plate
                )

                if not history:

                    print("No session history found.")

                else:

                    print(
                        "\n----- SESSION HISTORY -----"
                    )

                    for session in history:

                        print(
                            f"Session: "
                            f"{session.session_id} | "
                            f"Lot: {session.lot_id} | "
                            f"Spot: {session.spot_id} | "
                            f"Status: {session.status} | "
                            f"Fee: Rs. "
                            f"{session.parking_fee}"
                        )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # UPDATE PARKING SPOT
        # ==========================================

        elif choice == "14":

            try:

                spot_id = input(
                    "Enter Spot ID: "
                ).strip()

                print(
                    "\nLeave a field empty "
                    "if you don't want to change it."
                )

                spot_type = input(
                    "New Spot Type "
                    "(REGULAR/HANDICAPPED/EV): "
                ).strip()

                hourly_rate_input = input(
                    "New Hourly Rate: "
                ).strip()

                kwh_rate_input = input(
                    "New kWh Rate: "
                ).strip()

                status = input(
                    "New Status "
                    "(AVAILABLE/OCCUPIED/OUT_OF_SERVICE): "
                ).strip()

                spot_type = (
                    spot_type
                    if spot_type
                    else None
                )

                hourly_rate = (
                    float(hourly_rate_input)
                    if hourly_rate_input
                    else None
                )

                kwh_rate = (
                    float(kwh_rate_input)
                    if kwh_rate_input
                    else None
                )

                status = (
                    status
                    if status
                    else None
                )

                manager.update_spot(
                    spot_id,
                    spot_type,
                    hourly_rate,
                    kwh_rate,
                    status
                )

                print(
                    "Parking Spot updated successfully!"
                )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # DELETE PARKING SPOT
        # ==========================================

        elif choice == "15":

            try:

                spot_id = input(
                    "Enter Spot ID: "
                ).strip()

                manager.delete_spot(
                    spot_id
                )

                print(
                    "Parking Spot deleted successfully!"
                )

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # GENERATE REPORT
        # ==========================================

        elif choice == "16":

            try:

                report = manager.generate_report()

                print(
                    "\nFacility report generated successfully!"
                )

                print(
                    "Saved as: facility_report.txt"
                )

                print("\n" + report)

            except Exception as e:
                print("Error:", e)

        # ==========================================
        # EXIT
        # ==========================================

        elif choice == "17":

            print(
                "\nThank you for using "
                "Smart Parking System!"
            )

            break

        else:

            print(
                "Invalid choice! Please try again."
            )


if __name__ == "__main__":
    main()