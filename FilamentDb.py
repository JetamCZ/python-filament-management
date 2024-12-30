import sqlite3


class FilamentDb:

    def __init__(self, db_name):
        self.db_name = db_name

    def add_filament(self, manufacturer, filament_type, color_name, custom_name):
        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO filaments (manufacturer, type, color_name, custom_name)
            VALUES (?, ?, ?, ?)
        ''', (manufacturer, filament_type, color_name, custom_name))

        conn.commit()
        conn.close()

        print("Filament added successfully.")

    def add_spool(self, filament_id, original_filament_weight, original_spool_weight, original_length):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO spools (filament_id, original_filament_weight, original_spool_weight, original_length)
            VALUES (?, ?, ?, ?)
        ''', (filament_id, original_filament_weight, original_spool_weight, original_length))

        conn.commit()
        conn.close()

        print("Spool added successfully.")

    def remove_filament(self, filament_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM filaments WHERE id = ?
        ''', (filament_id,))

        conn.commit()

        conn.close()
        print("Filament removed successfully.")

    def remove_spool(self, spool_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM spools WHERE id = ?
        ''', (spool_id,))

        conn.commit()
        conn.close()

        print("Spool removed successfully.")

    def add_spool_weight(self, spool_id, datetime, weight):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Spool_weight (spool_id, datetime, weight)
            VALUES (?, ?, ?)
        ''', (spool_id, datetime, weight))

        conn.commit()
        conn.close()

        print("Spool weight added successfully.")

    def get_all_spools(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT spools.id, filaments.manufacturer, filaments.type, filaments.color_name, spools.original_filament_weight, spools.original_spool_weight
            FROM spools
            JOIN filaments ON spools.filament_id = filaments.id
        ''')
        rows = cursor.fetchall()
        conn.close()

        return rows

    def get_all_filaments(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM filaments
        ''')

        rows = cursor.fetchall()
        conn.close()

        return rows

    def get_spools_by_filament(self, filament_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT spools.id, filaments.manufacturer, filaments.type, filaments.color_name, spools.original_filament_weight, spools.original_spool_weight
            FROM spools
            JOIN filaments ON filaments.id = spools.filament_id 
            WHERE filament_id = ?
        ''', (filament_id,))

        rows = cursor.fetchall()
        conn.close()

        return rows

