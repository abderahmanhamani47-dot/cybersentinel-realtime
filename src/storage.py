import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "cybersentinel.db"

def connect():
    return sqlite3.connect(DB)

def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ip TEXT NOT NULL,
                type TEXT NOT NULL,
                severity TEXT NOT NULL,
                score INTEGER NOT NULL,
                evidence TEXT NOT NULL
            )
        """)
        conn.commit()

def save_alert(alert):
    with connect() as conn:
        conn.execute(
            """INSERT INTO alerts
               (timestamp, ip, type, severity, score, evidence)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                alert["timestamp"], alert["ip"], alert["type"],
                alert["severity"], alert["score"], alert["evidence"]
            ),
        )
        conn.commit()

def get_alerts():
    with connect() as conn:
        rows = conn.execute(
            """SELECT id, timestamp, ip, type, severity, score, evidence
               FROM alerts ORDER BY id DESC LIMIT 100"""
        ).fetchall()

    return [
        {
            "id": r[0], "timestamp": r[1], "ip": r[2], "type": r[3],
            "severity": r[4], "score": r[5], "evidence": r[6]
        }
        for r in rows
    ]

def get_stats():
    with connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
        critical = conn.execute(
            "SELECT COUNT(*) FROM alerts WHERE severity='CRITICAL'"
        ).fetchone()[0]
        high = conn.execute(
            "SELECT COUNT(*) FROM alerts WHERE severity='HIGH'"
        ).fetchone()[0]
        medium = conn.execute(
            "SELECT COUNT(*) FROM alerts WHERE severity='MEDIUM'"
        ).fetchone()[0]
        low = conn.execute(
            "SELECT COUNT(*) FROM alerts WHERE severity='LOW'"
        ).fetchone()[0]
    return {
        "total": total,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
    }
