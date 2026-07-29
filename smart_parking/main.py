from facility_manager import FacilityManager

manager = FacilityManager()

while True:
    print("\n===== Smart Parking System =====")
    print("1. Add Parking Lot")
    print("2. Show Parking Lots")
    print("3. Register Vehicle")
    print("4. Show Vehicles")
    print("5. Add Parking Spot")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        lot_id = input("Enter Lot ID: ")
        lot_name = input("Enter Lot Name: ")
        capacity = int(input("Enter Capacity: "))
        manager.add_parking_lot(lot_id, lot_name, capacity)

    elif choice == "2":
        manager.show_parking_lots()

    elif choice == "3":
        plate = input("Enter License Plate: ")
        owner = input("Enter Owner Name: ")
        vtype = input("Enter Vehicle Type (CAR/EV): ")
        reg_date = input("Enter Registration Date (YYYY-MM-DD): ")
        manager.register_vehicle(plate, owner, vtype, reg_date)

    elif choice == "4":
        manager.show_vehicles()

    elif choice == "5":
        lot_id = input("Enter Lot ID: ")
        spot_id = input("Enter Spot ID: ")
        spot_type = input("Enter Spot Type (REGULAR/HANDICAPPED/EV): ")
        hourly_rate = float(input("Enter Hourly Rate: "))
        manager.add_parking_spot(lot_id, spot_id, spot_type, hourly_rate)

    elif choice == "6":
        print("Thank you for using Smart Parking System!")
        break

    else:
        print("Invalid Choice! Try Again.")