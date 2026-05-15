#!/usr/bin/env python3
"""Rebuild SQLite FTS5 index from all task JSON files."""
import json, sqlite3, os, sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "db" / "index.sqlite"
GOALS_PATH = Path(__file__).parent / "goals"

DB_PATH.parent.mkdir(exist_ok=True)
conn = sqlite3.connect(str(DB_PATH))
conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS tasks_fts USING fts5(id, title, description, status, department, milestone, assignees, labels, content='', tokenize='unicode61')")

# Clear and rebuild
conn.execute("DELETE FROM tasks_fts")
for f in GOALS_PATH.rglob("*.json"):
    with open(f) as fh:
        task = json.load(fh)
    conn.execute(
        "INSERT INTO tasks_fts(id, title, description, status, department, milestone, assignees, labels) VALUES(?,?,?,?,?,?,?,?)",
        (task["id"], task["title"], task.get("description",""), task["status"],
         task["department"], task["milestone"],
         " ".join(task.get("assignees", [])),
         " ".join(task.get("labels", [])))
    )
conn.commit()
print(f"Indexed {conn.execute('SELECT count(*) FROM tasks_fts').fetchone()[0]} tasks")
conn.close()
