from FilamentDb import FilamentDb


def create_filament(db: FilamentDb):
    manufacturer = input("Enter manufacturer: ")
    filament_type = input("Enter type: ")
    color_name = input("Enter color name: ")

    db.add_filament(manufacturer=manufacturer, filament_type=filament_type, color_name=color_name)


def create_spool(db: FilamentDb):
    filament_id = int(input("Enter filament ID: "))
    code = input("Enter spool code: ")
    original_filament_weight = int(input("Enter original filament weight: "))
    original_spool_weight = int(input("Enter original spool weight: "))
    original_length = float(input("Enter original spool length: "))
    db.add_spool(filament_id, code, original_filament_weight, original_spool_weight, original_length)


def delete_filament(db: FilamentDb):
    filament_id = int(input("Enter filament ID to remove: "))
    db.remove_filament(filament_id)


def delete_spool(db: FilamentDb):
    spool_id = int(input("Enter spool ID to remove: "))
    db.remove_spool(spool_id)


def add_weight(db: FilamentDb):
    spool_id = int(input("Enter spool ID: "))
    datetime = input("Enter datetime (YYYY-MM-DD HH:MM:SS): ")
    weight = int(input("Enter weight: "))
    db.add_spool_weight(spool_id, datetime, weight)


def cli_loop():
    db = FilamentDb("filament_management.db")

    while True:
        print("\nFilament Management CLI")
        print("1. Add Filament")
        print("2. Remove Filament")
        print("3. Add Spool")
        print("4. Remove Spool")
        print("5. Add Spool Weight")
        print("to exit write \"exit\"")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_filament(db)
        elif choice == "2":
            delete_filament(db)
        elif choice == "3":
            create_spool(db)
        elif choice == "4":
            delete_spool(db)
        elif choice == "5":
            add_weight(db)
        elif choice == "exit":
            print("Exiting CLI.")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    cli_loop()
