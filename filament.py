from FilamentDb import FilamentDb

def create_filament():
    manufacturer = input("Enter manufacturer: ")
    filament_type = input("Enter type: ")
    color_name = input("Enter color name: ")

    db.add_filament(manufacturer=manufacturer, filament_type=filament_type, color_name=color_name)


if __name__ == "__main__":
    db = FilamentDb("filament_management.db")
    create_filament()
