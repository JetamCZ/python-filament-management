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


def cli_loop():
    db = FilamentDb("filament_management.db")

    while True:
        print("\nFilament Management CLI")
        print("1. Add Filament")
        print("2. Add Spool")
        print("to exit write \"exit\"")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_filament(db)
        elif choice == "2":
            create_spool(db)
        elif choice == "exit":
            print("Exiting CLI.")
            break


if __name__ == "__main__":
    cli_loop()
