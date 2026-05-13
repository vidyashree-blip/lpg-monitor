import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("lpg_monitor.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ppm       REAL,
            weight_kg REAL,
            status    TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database ready.")

def save_reading(ppm, weight_kg, status):
    conn = sqlite3.connect("lpg_monitor.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO readings (timestamp, ppm, weight_kg, status)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().isoformat(), ppm, weight_kg, status))
    conn.commit()
    conn.close()

def get_last_7_days():
    conn = sqlite3.connect("lpg_monitor.db")
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, weight_kg FROM readings
        WHERE timestamp >= datetime('now', '-7 days')
        ORDER BY timestamp ASC
    """)
    data = c.fetchall()
    conn.close()
    return data

def get_today_readings():
    conn = sqlite3.connect("lpg_monitor.db")
    c = conn.cursor()
    today = datetime.now().date().isoformat()
    c.execute("""
        SELECT MAX(weight_kg), MIN(weight_kg) FROM readings
        WHERE DATE(timestamp) = ?
    """, (today,))
    result = c.fetchone()
    conn.close()
    return result