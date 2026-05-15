CREATE TABLE IF NOT EXISTS daily_goals (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    content    TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS daily_goal_completions (
    goal_id INTEGER NOT NULL REFERENCES daily_goals(id) ON DELETE CASCADE,
    day     TEXT NOT NULL,
    done    INTEGER NOT NULL DEFAULT 0,
    count   INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (goal_id, day)
);

CREATE INDEX IF NOT EXISTS idx_daily_goal_completions_day ON daily_goal_completions(day);
