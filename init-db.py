import sqlite3

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Filament (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manufacturer VARCHAR(255),
            type VARCHAR(128),
            color_name VARCHAR(64)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Spool (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filament_id INTEGER,
            code VARCHAR(64),
            original_filament_weight INTEGER,
            original_spool_weight INTEGER,
            FOREIGN KEY (filament_id) REFERENCES Filament (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Spool_weight (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spool_id INTEGER,
            datetime DATETIME,
            weight INTEGER,
            FOREIGN KEY (spool_id) REFERENCES Spool (id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    database_file = "filament_management.db"

    create_database(database_file)
    print(f"Database '{database_file}' with tables created successfully.")
