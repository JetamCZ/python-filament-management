import sqlite3

from models.spool import Spool
from models.spool import spool_from_db
from models.filament import Filament


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
            SELECT spools.*, filaments.*, last_weight.weight
            FROM spools
            JOIN filaments ON spools.filament_id = filaments.id
            LEFT JOIN (
                SELECT *
                FROM spools_weights
                    WHERE
                    (spool_id, datetime) IN (
                        SELECT
                            spool_id,
                            MAX(datetime) AS max_datetime
                        FROM
                            spools_weights
                        GROUP BY
                            spool_id
                    )
            ) AS last_weight ON spools.id = last_weight.spool_id;
        ''')
        rows = cursor.fetchall()
        conn.close()

        return [
            spool_from_db(row)
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
            SELECT spools.*, filaments.*,last_weight.weight  FROM spools
            JOIN filaments ON filaments.id = spools.filament_id  
                        LEFT JOIN (
                SELECT *
                FROM spools_weights
                    WHERE
                    (spool_id, datetime) IN (
                        SELECT
                            spool_id,
                            MAX(datetime) AS max_datetime
                        FROM
                            spools_weights
                        GROUP BY
                            spool_id
                    )
            ) AS last_weight ON spools.id = last_weight.spool_id
            WHERE spools.id = ?
        ''', (spool_id,))

        row = cursor.fetchone()
        conn.close()

        return spool_from_db(row)

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
            SELECT spools.*, filaments.*, last_weight.weight
            FROM spools
            JOIN filaments ON filaments.id = spools.filament_id 
            LEFT JOIN (
                SELECT *
                FROM spools_weights
                    WHERE
                    (spool_id, datetime) IN (
                        SELECT
                            spool_id,
                            MAX(datetime) AS max_datetime
                        FROM
                            spools_weights
                        GROUP BY
                            spool_id
                    )
            ) AS last_weight ON spools.id = last_weight.spool_id
            WHERE filament_id = ?
        ''', (filament_id,))

        rows = cursor.fetchall()
        conn.close()

        return [
            spool_from_db(row)
            for row in rows
        ]

