CREATE TABLE IF NOT EXISTS raw_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    received_at TEXT NOT NULL,
    source      TEXT,
    metric      TEXT,
    payload_json TEXT NOT NULL,
    hash        TEXT NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_raw_events_received_at ON raw_events(received_at);
CREATE INDEX IF NOT EXISTS idx_raw_events_source ON raw_events(source);
CREATE INDEX IF NOT EXISTS idx_raw_events_metric ON raw_events(metric);

CREATE TABLE IF NOT EXISTS measurements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_event_id    INTEGER NOT NULL,
    source          TEXT NOT NULL,
    source_type     TEXT,
    source_detail   TEXT,
    metric          TEXT NOT NULL,
    ts_start        TEXT,
    ts_end          TEXT,
    value           REAL,
    unit            TEXT,
    quality_flag    INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL,
    UNIQUE(raw_event_id, metric, ts_start, ts_end)
);

CREATE INDEX IF NOT EXISTS idx_measurements_ts_start ON measurements(ts_start);
CREATE INDEX IF NOT EXISTS idx_measurements_metric ON measurements(metric);
CREATE INDEX IF NOT EXISTS idx_measurements_source ON measurements(source);
CREATE INDEX IF NOT EXISTS idx_measurements_raw_event_id ON measurements(raw_event_id);
CREATE INDEX IF NOT EXISTS idx_measurements_source_type ON measurements(source_type);
CREATE UNIQUE INDEX IF NOT EXISTS uq_measurements_source_range
    ON measurements(source_type, source, metric, ts_start, ts_end);

CREATE TABLE IF NOT EXISTS source_priority (
    source_type TEXT PRIMARY KEY,
    priority    INTEGER NOT NULL
);

INSERT OR REPLACE INTO source_priority (source_type, priority) VALUES ('watch', 1);
INSERT OR REPLACE INTO source_priority (source_type, priority) VALUES ('phone', 2);
INSERT OR REPLACE INTO source_priority (source_type, priority) VALUES ('other', 3);

CREATE TABLE IF NOT EXISTS daily_metrics (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    day                         TEXT NOT NULL,
    source                      TEXT NOT NULL,
    metric                      TEXT NOT NULL,
    value                       REAL,
    unit                        TEXT,
    derived_from_measurement_id INTEGER,
    derived_ts_end              TEXT,
    updated_at                  TEXT NOT NULL,
    UNIQUE(day, source, metric)
);

CREATE INDEX IF NOT EXISTS idx_daily_metrics_day ON daily_metrics(day);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_metric ON daily_metrics(metric);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_source ON daily_metrics(source);

CREATE TABLE IF NOT EXISTS focus_sessions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    start_at         TEXT NOT NULL,
    end_at           TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL,
    created_at       TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_focus_sessions_start_at ON focus_sessions(start_at);

CREATE TABLE IF NOT EXISTS reflections (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at        TEXT NOT NULL,
    day                TEXT NOT NULL,
    want_to_do         TEXT,
    anxiety            TEXT,
    unconscious_desire TEXT,
    free_text          TEXT,
    created_at         TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_reflections_day ON reflections(day);

CREATE TABLE IF NOT EXISTS habit_groups (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    sort_order    INTEGER NOT NULL DEFAULT 0,
    woop_wish     TEXT,
    woop_outcome  TEXT,
    woop_obstacle TEXT,
    woop_plan     TEXT,
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS habit_group_items (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id   INTEGER NOT NULL REFERENCES habit_groups(id) ON DELETE CASCADE,
    content    TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_habit_group_items_group_id ON habit_group_items(group_id);

CREATE TABLE IF NOT EXISTS habit_completions (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL REFERENCES habit_group_items(id) ON DELETE CASCADE,
    day     TEXT NOT NULL,
    done    INTEGER NOT NULL DEFAULT 0,
    count   INTEGER NOT NULL DEFAULT 0,
    UNIQUE(item_id, day)
);

CREATE INDEX IF NOT EXISTS idx_habit_completions_day ON habit_completions(day);

CREATE TABLE IF NOT EXISTS wish_categories (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wish_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES wish_categories(id) ON DELETE CASCADE,
    content     TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_wish_items_category_id ON wish_items(category_id);
