import sqlite3

DB_FILE = "central.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS estaciones (
            id TEXT PRIMARY KEY,
            ubicacion TEXT,
            estado TEXT,
            caudal REAL DEFAULT 0.0,
            volumen_total REAL DEFAULT 0.0
        )
    """)
    cur.execute("UPDATE estaciones SET estado = 'DESCONECTADA'")
    conn.commit()
    conn.close()

def registrar_estacion(ws_id, ubicacion):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO estaciones (id, ubicacion, estado) VALUES (?, ?, 'DISPONIBLE')
        ON CONFLICT(id) DO UPDATE SET ubicacion = ?, estado = 'DISPONIBLE'
    """, (ws_id, ubicacion, ubicacion))
    conn.commit()
    conn.close()

def actualizar_estado(ws_id, nuevo_estado):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE estaciones SET estado = ? WHERE id = ?", (nuevo_estado, ws_id))
    conn.commit()
    conn.close()
    
def obtener_estaciones():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, ubicacion, estado, caudal, volumen_total FROM estaciones")
    conn.commit()
    conn.close()
    