# lab-scheduler-DB

Git-based task database for [lab-scheduler](https://github.com/BruceBest/lab-scheduler).

## Architecture

```
goals/                          # Source of truth (human-readable JSON)
  {department}/                 # e.g. management, engineering
    {milestone}/                # e.g. 2026-Q2
      {task-slug}.json          # Task file
      done/                     # Completed tasks
  backlog/                      # Unassigned tasks

db/index.sqlite                 # SQLite FTS5 search index (gitignored)
```

## Task Lifecycle

1. **Create**: Write JSON → `git add` → `git commit`
2. **Move**: `git mv` between folders (status change)
3. **Update**: Edit JSON fields → commit
4. **Search**: SQLite FTS5 full-text index

## Schema

See `schemas/task.schema.json`.

## CI

- JSON schema validation on push
- FTS5 index rebuild hook
