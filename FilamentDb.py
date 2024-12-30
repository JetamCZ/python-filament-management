import sqlite3


class Filament:
    def __init__(self, id=None, manufacturer=None, filament_type=None, color_name=None, custom_name=None):
        self.id = id
        self.manufacturer = manufacturer
        self.type = filament_type
        self.color_name = color_name
        self.custom_name = custom_name

    def __repr__(self):
        return f"Filament(id={self.id}, manufacturer='{self.manufacturer}', type='{self.type}', color_name='{self.color_name}')"


class Spool:
    def __init__(self, id=None, filament=Filament, original_filament_weight=None, original_spool_weight=None,
                 original_length=None):
        self.id = id
        self.filament = filament
        self.original_filament_weight = original_filament_weight
        self.original_spool_weight = original_spool_weight
        self.original_length = original_length

    def __repr__(self):
        return (f"Spool(id={self.id}, filament_id={self.filament.id}, original_length='{self.original_length}', "
                f"original_filament_weight={self.original_filament_weight}, original_spool_weight={self.original_spool_weight})")


class FilamentDb:

    def __init__(self, db_name):
        self.db_name = db_name

    def add_filament(self, filament: Filament):
        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO filaments (manufacturer, type, color_name, custom_name)
            VALUES (?, ?, ?, ?)
        ''', (filament.manufacturer, filament.type, filament.color_name, filament.custom_name))

        conn.commit()
        conn.close()

        print("Filament added successfully.")

    def add_spool(self, spool: Spool):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO spools (filament_id, original_filament_weight, original_spool_weight, original_length)
            VALUES (?, ?, ?, ?)
        ''', (
            spool.filament.id,
            spool.original_filament_weight,
            spool.original_spool_weight,
            spool.original_length
        ))

        conn.commit()
        conn.close()

        print("Spool added successfully.")

    def remove_filament(self, filament_id):
        spools = self.get_spools_by_filament(filament_id)

        if len(spools) > 0:
            print("Cannot remove a filament. Remove all filament spools first.")
            return False

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
            DELETE FROM spools_weights WHERE id = ?
        ''', (spool_id,))

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
            INSERT INTO spools_weights (spool_id, datetime, weight)
            VALUES (?, ?, ?)
        ''', (spool_id, datetime, weight))

        conn.commit()
        conn.close()

        print("Spool weight added successfully.")

    def get_all_spools(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT spools.*, filaments.*
            FROM spools
            JOIN filaments ON spools.filament_id = filaments.id
        ''')
        rows = cursor.fetchall()
        conn.close()

        return [
            Spool(
                id=row[0],
                original_filament_weight=row[2],
                original_spool_weight=row[3],
                original_length=row[4],
                filament=Filament(
                    id=row[5],
                    manufacturer=row[6],
                    filament_type=row[7],
                    color_name=row[8],
                    custom_name=row[9]
                )
            )
            for row in rows
        ]

    def get_filament(self, filament_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM filaments WHERE id = ?
        ''', (filament_id,))

        row = cursor.fetchone()
        conn.close()

        return Filament(
            id=row[0],
            manufacturer=row[1],
            filament_type=row[2],
            color_name=row[3],
            custom_name=row[4]
        )

    def get_spool(self, spool_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM spools
            JOIN filaments ON filaments.id = spools.filament_id  
            WHERE spools.id = ?
        ''', (spool_id,))

        row = cursor.fetchone()
        conn.close()

        return self._transform_row_to_spool(row)

    def get_all_filaments(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM filaments
        ''')

        rows = cursor.fetchall()
        conn.close()

        return [
            Filament(
                id=row[0],
                manufacturer=row[1],
                filament_type=row[2],
                color_name=row[3],
                custom_name=row[4]
            )
            for row in rows
        ]

    def get_spools_by_filament(self, filament_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT spools.*, filaments.*
            FROM spools
            JOIN filaments ON filaments.id = spools.filament_id 
            WHERE filament_id = ?
        ''', (filament_id,))

        rows = cursor.fetchall()
        conn.close()

        return [
            self._transform_row_to_spool(row)
            for row in rows
        ]

    def _transform_row_to_spool(self, row):
        return Spool(
            id=row[0],
            original_filament_weight=row[2],
            original_spool_weight=row[3],
            original_length=row[4],
            filament=Filament(
                id=row[5],
                manufacturer=row[6],
                filament_type=row[7],
                color_name=row[8],
                custom_name=row[9]
            )
        )
