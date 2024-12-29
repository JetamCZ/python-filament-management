import sqlite3


class FilamentDb:

    def __init__(self, db_name):
        self.db_name = db_name

    def add_filament(self, manufacturer, filament_type, color_name):
        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO filaments (manufacturer, type, color_name)
            VALUES (?, ?, ?)
        ''', (manufacturer, filament_type, color_name))

        conn.commit()
        conn.close()

        print("Filament added successfully.")

    def add_spool(self, filament_id, code, original_filament_weight, original_spool_weight):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO spools (filament_id, code, original_filament_weight, original_spool_weight)
            VALUES (?, ?, ?, ?)
        ''', (filament_id, code, original_filament_weight, original_spool_weight))

        conn.commit()
        conn.close()

        print("Spool added successfully.")
