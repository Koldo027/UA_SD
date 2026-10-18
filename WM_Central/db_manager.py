import sqlite3

DB_PATH = "central.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watering_stations (
            id TEXT PRIMARY KEY,
            location TEXT,
            status TEXT,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def registrar_o_actualizar_ws(ws_id, location, status="DISPONIBLE"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM watering_stations WHERE id = ?", (ws_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            "INSERT INTO watering_stations (id, location, status) VALUES (?, ?, ?)",
            (ws_id, location, status)
        )
    else:
        cursor.execute(
            "UPDATE watering_stations SET location = ?, status = ?, last_seen = CURRENT_TIMESTAMP WHERE id = ?",
            (location, status, ws_id)
        )
    conn.commit()
    conn.close()