#!/usr/bin/env python3
"""Rebuild SQLite FTS5 index from all task JSON files."""
import json, sqlite3, os, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent  # repo root, not scripts/
DB_PATH = ROOT / "db" / "index.sqlite"
GOALS_PATH = ROOT / "goals"

DB_PATH.parent.mkdir(exist_ok=True)
conn = sqlite3.connect(str(DB_PATH))
# Clear and rebuild (DROP instead of DELETE — contentless FTS5 doesn't support DELETE)
conn.execute("DROP TABLE IF EXISTS tasks_fts")
conn.execute("CREATE VIRTUAL TABLE tasks_fts USING fts5(id, title, description, status, department, milestone, assignees, labels, content='', tokenize='unicode61')")
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
