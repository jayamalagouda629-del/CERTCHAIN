"""FEATURE 6: Audit log (SQLite). Stores NO student PII: only hash, verdict, time."""
import sqlite3
from datetime import datetime, timezone
from . import config

def _conn():
    config.DB_PATH.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(config.DB_PATH)
    c.execute("""CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, kind TEXT, verdict TEXT,
        cert_hash TEXT, usn TEXT, detail TEXT)""")
    return c

def log(kind: str, verdict: str, cert_hash: str = "", usn: str = "", detail: str = ""):
    with _conn() as c:
        c.execute("INSERT INTO events(ts,kind,verdict,cert_hash,usn,detail) VALUES(?,?,?,?,?,?)",
                  (datetime.now(timezone.utc).isoformat(timespec="seconds"), kind, verdict, cert_hash, usn, detail))

def all_events():
    import pandas as pd
    with _conn() as c:
        return pd.read_sql_query("SELECT * FROM events ORDER BY id DESC", c)
