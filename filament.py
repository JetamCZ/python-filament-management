from FilamentDb import FilamentDb
from initdb import create_database


def create_filament(db: FilamentDb):
    custom_name = input("Enter name (any custom name): ")
    manufacturer = input("Enter manufacturer: ")
    filament_type = input("Enter type (PLA/PETG/TPU/...): ")
    color_name = input("Enter color: ")

    db.add_filament(
        custom_name=custom_name,
        manufacturer=manufacturer,
        filament_type=filament_type,
        color_name=color_name
    )


def create_spool(db: FilamentDb):
    filament_id = int(input("Enter filament ID: "))
    original_filament_weight = int(input("Enter original filament only weight (g): "))
    original_spool_weight = int(input("Enter original total weight with spool (g): "))
    original_length = float(input("Enter original spool length (meters): "))
    db.add_spool(filament_id, original_filament_weight, original_spool_weight, original_length)


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


def show_all_spools(db: FilamentDb):
    rows = db.get_all_spools()

    print("ID | Manufacturer | Type | Color | Filament Weight | Spool Weight")
    print("-" * 70)
    for row in rows:
        print(" | ".join(map(str, row)))


def show_all_filaments(db: FilamentDb):
    rows = db.get_all_filaments()

    print("ID | Manufacturer | Type | Color")
    print("-" * 70)
    for row in rows:
        print(" | ".join(map(str, row)))


def show_spools_by_filament(db: FilamentDb):
    filament_id = int(input("Enter filament ID: "))
    rows = db.get_spools_by_filament(filament_id)

    print("ID | Manufacturer | Type | Color | Filament Weight | Spool Weight")
    for row in rows:
        print(" | ".join(map(str, row)))


def cli_loop():
    db = FilamentDb("filament_management.db")

    while True:
        print("\nFilament Management CLI")
        print("1. Add Filament (type)")
        print("2. Remove Filament (type)")
        print("3. Add Spool")
        print("4. Remove Spool")
        print("5. Add Spool Weight")
        print("6. Show all filaments (types)")
        print("7. Show all spools")
        print("8. Show spools by filament (type)")
        print("\nto exit write \"exit\"")

        choice = input("\nEnter your choice: ")

        print("\n")

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
        elif choice == "6":
            show_all_filaments(db)
        elif choice == "7":
            show_all_spools(db)
        elif choice == "8":
            show_spools_by_filament(db)
        elif choice == "exit":
            print("Exiting CLI.")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    create_database("filament_management.db")
    cli_loop()
