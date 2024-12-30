from models.spool import Spool
from models.filament import Filament
from db.db_controller import FilamentDb
from db.initdb import create_database
from datetime import datetime
from db.export_to_excel import export_to_excel

from config import config as env_config
from utils.validator import input_with_validation
from utils.validator import valid_string
from utils.validator import valid_integer


def create_filament(db: FilamentDb):
    custom_name = input_with_validation("Enter name (any custom name): ", valid_string)
    manufacturer = input_with_validation("Enter manufacturer: ", valid_string)
    filament_type = input_with_validation("Enter type (PLA/PETG/TPU/...): ", valid_string)
    color_name = input_with_validation("Enter color: ", valid_string)

    filament = Filament(
        manufacturer=manufacturer,
        filament_type=filament_type,
        color_name=color_name,
        custom_name=custom_name
    )

    db.add_filament(filament)


def create_spool(db: FilamentDb):
    filament_id = int(input_with_validation("Enter filament ID: ", valid_integer))
    original_filament_weight = int(input_with_validation("Enter original filament only weight (g): ", valid_integer))
    original_spool_weight = int(input_with_validation("Enter original total weight with spool (g): ", valid_integer))
    original_length = float(input_with_validation("Enter original spool length (meters): ", valid_integer))

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
    filament_id = int(input_with_validation("Enter filament ID to remove: ", valid_integer))
    db.remove_filament(filament_id)


def delete_spool(db: FilamentDb):
    spool_id = int(input_with_validation("Enter spool ID to remove: ", valid_integer))
    db.remove_spool(spool_id)


def add_weight(db: FilamentDb):
    spool_id = int(input_with_validation("Enter spool ID: ", valid_integer))

    spool = db.get_spool(spool_id)
    weight = int(input_with_validation("Enter current weight of filament with spool: ", valid_integer))

    if spool is None:
        print("Unknown spool")
        return

    if weight < 0 or weight > spool.original_spool_weight:
        print("Invalid weight")
        return

    db.add_spool_weight(
        spool_id=spool_id,
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        weight=weight
    )

    print(f"New estimated length {spool.calculate_length_by_weight(weight)}m")


def show_all_spools(db: FilamentDb):
    spools = db.get_all_spools()

    print("Spool, Filament")
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
    filament_id = int(input_with_validation("Enter filament ID: ", valid_integer))
    spools = db.get_spools_by_filament(filament_id)

    print("\nSpool")
    print("-" * 70)
    for spool in spools:
        print(spool)


def export(db: FilamentDb):
    spools = db.get_all_spools()
    filaments = db.get_all_filaments()

    export_to_excel("./output.xlsx", spools, filaments)


def cli_loop():
    db = FilamentDb(env_config.db_name)

    while True:
        print("\nFilament Management CLI")
        print("1. Add filament (type)")
        print("2. Remove filament (type)")
        print("3. Add Spool")
        print("4. Remove Spool")
        print("5. Add Spool Weight")
        print("6. Show all filaments (types)")
        print("7. Show all spools")
        print("8. Show spools by filament (type)")
        print("9. Export to xlsx file")
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
            show_all_spools(db)
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
        elif choice == "9":
            export(db)
        elif choice == "exit":
            print("Exiting CLI.")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    create_database(env_config.db_name)
    cli_loop()
