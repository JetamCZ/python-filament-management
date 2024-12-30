from models.spool import Spool
from db.db_controller import FilamentDb
from db.initdb import create_database
from datetime import datetime

from config import config as env_config

def create_filament(db: FilamentDb):
    custom_name = input("Enter name (any custom name): ")
    manufacturer = input("Enter manufacturer: ")
    filament_type = input("Enter type (PLA/PETG/TPU/...): ")
    color_name = input("Enter color: ")

    filament = Filament(
        manufacturer=manufacturer,
        filament_type=filament_type,
        color_name=color_name,
        custom_name=custom_name
    )

    db.add_filament(filament)


def create_spool(db: FilamentDb):
    filament_id = int(input("Enter filament ID: "))
    original_filament_weight = int(input("Enter original filament only weight (g): "))
    original_spool_weight = int(input("Enter original total weight with spool (g): "))
    original_length = float(input("Enter original spool length (meters): "))

    filament = db.get_filament(filament_id)

    if filament is None:
        print("Unknown filament")
        return

    spool = Spool(
        filament=filament,
        original_filament_weight=original_filament_weight,
        original_spool_weight=original_spool_weight,
        original_length=original_length
    )

    db.add_spool(spool)


def delete_filament(db: FilamentDb):
    filament_id = int(input("Enter filament ID to remove: "))
    db.remove_filament(filament_id)


def delete_spool(db: FilamentDb):
    spool_id = int(input("Enter spool ID to remove: "))
    db.remove_spool(spool_id)


def add_weight(db: FilamentDb):
    spool_id = int(input("Enter spool ID: "))

    spool = db.get_spool(spool_id)
    weight = int(input("Enter current weight of filament with spool: "))

    if spool is None:
        print("Unknown spool")
        return

    db.add_spool_weight(
        spool_id=spool_id,
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        weight=weight
    )

    print(f"New estimated length ${spool.calculate_length_by_weight(weight)}m")

def show_all_spools(db: FilamentDb):
    spools = db.get_all_spools()

    print("Spool, Filament.py")
    print("-" * 70)
    for spool in spools:
        print(spool)
        print(spool.filament)
        print("-" * 3)


def show_all_filaments(db: FilamentDb):
    filaments = db.get_all_filaments()

    print("Filaments")
    print("-" * 70)
    for filament in filaments:
        print(filament)


def show_spools_by_filament(db: FilamentDb):
    filament_id = int(input("Enter filament ID: "))
    spools = db.get_spools_by_filament(filament_id)

    print("Spool")
    for spool in spools:
        print(spool)


def cli_loop():
    db = FilamentDb(env_config.db_name)

    while True:
        print("\nFilament.py Management CLI")
        print("1. Add Filament.py (type)")
        print("2. Remove Filament.py (type)")
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
            show_all_filaments(db)
            delete_filament(db)
        elif choice == "3":
            show_all_filaments(db)
            create_spool(db)
        elif choice == "4":
            delete_spool(db)
        elif choice == "5":
            show_all_spools(db)
            add_weight(db)
        elif choice == "6":
            show_all_filaments(db)
        elif choice == "7":
            show_all_spools(db)
        elif choice == "8":
            show_all_filaments(db)
            show_spools_by_filament(db)
        elif choice == "exit":
            print("Exiting CLI.")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    create_database(env_config.db_name)
    cli_loop()
