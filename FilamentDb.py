import sqlite3


class FilamentDb:
    def add_filament(manufacturer, filament_type, color_name):
        conn = sqlite3.connect("filament_management.db")

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Filament (manufacturer, type, color_name)
            VALUES (?, ?, ?)
        ''', (manufacturer, filament_type, color_name))

        conn.commit()
        conn.close()
        print("Filament added successfully.")
