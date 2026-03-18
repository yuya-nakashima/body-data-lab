# app Inventory

## Summary

`app/` is a Python/FastAPI prototype that currently mixes three concerns in one place:

- API endpoints
- SQLite schema / access
- ETL-like normalization and aggregation jobs exposed as HTTP routes

It is usable as a temporary prototype, but it is not a good long-term home if the repository is moving toward separate `api/`, `etl/`, `db/`, and `dashboard/` directories.

## Current Structure

- `app/main.py`: FastAPI entrypoint and router registration
- `app/core/config.py`: environment-based DB path configuration
- `app/core/db.py`: SQLite connection, schema creation, indexes, and helper hashing
- `app/core/timeutil.py`: timezone/date helpers shared across routes/services
- `app/routers/ingest.py`: raw event ingestion endpoint
- `app/routers/raw.py`: raw event inspection endpoints
- `app/routers/normalize.py`: normalization logic exposed as an HTTP endpoint
- `app/routers/aggregate.py`: daily aggregation and rebuild/dedup operations exposed as HTTP endpoints
- `app/routers/quality.py`: data quality inspection endpoints
- `app/routers/metrics.py`: read API for aggregated daily metrics
- `app/routers/ui.py`: inline HTML dashboard for step data
- `app/services/aggregate_service.py`: aggregation jobs and read-side service functions extracted from `aggregate.py`
- `app/services/normalize_service.py`: normalization jobs and source classification extracted from `normalize.py`

## Current Extraction Status

- `parse_iso8601` was moved into `app/core/timeutil.py`.
- Aggregation helpers and write-heavy processing were moved into `app/services/aggregate_service.py`.
- Normalization helpers and raw-to-measurement conversion were moved into `app/services/normalize_service.py`.
- `app/routers/aggregate.py` now acts as a thin route layer:
  - parameter normalization
  - service call
  - response passthrough
- `app/routers/normalize.py` now acts as a thin route layer:
  - parameter normalization
  - service call
  - response passthrough
- `GET /daily` now reads through the same service layer as the write-heavy routes, which makes later API/ETL separation more mechanical.
- `normalize.py` no longer owns source classification or DB write logic directly, which makes a later move into `etl/` largely mechanical.

## Confirmed Boundaries

### Keep as API

- `app/main.py`
- `app/routers/ingest.py`
- `app/routers/raw.py`
- `app/routers/metrics.py`
- read-only parts of `app/routers/quality.py`
- read-only part of `app/routers/aggregate.py` such as `GET /daily`

These are request/response oriented and are reasonable to keep behind an HTTP API.

### Move toward ETL / batch / admin processing

- `app/routers/normalize.py`
- `POST /aggregate/daily` in `app/routers/aggregate.py`
- `POST /measurements/deduplicate-steps-total` in `app/routers/aggregate.py`
- `POST /aggregate/daily/rebuild-steps-total` in `app/routers/aggregate.py`
- any future write-heavy quality checks or maintenance routines

These are not stable external API contracts. They are data-processing or maintenance operations and should eventually become internal jobs or admin commands.

### Extract as shared foundation

- `app/core/db.py`
- `app/core/config.py`
- reusable parsing / date helpers from `app/routers/aggregate.py` and `app/routers/quality.py`
- `app/core/timeutil.py`

This layer should become the common dependency used by both `api/` and `etl/`.

### Keep provisional

- `app/routers/quality.py`
- `app/routers/ui.py`

`quality.py` mixes diagnostics that could stay as internal API endpoints with logic that may later become reporting helpers. `ui.py` is useful as a prototype, but it should not drive the long-term structure.

## `aggregate.py` Decomposition Plan

| Target | Current role | Future home | Plan |
| --- | --- | --- | --- |
| `_parse_iso8601` | ISO8601 parsing helper | shared foundation | move to a common util module first |
| `_load_source_priority` | load DB-side source priority map | shared foundation or ETL helper | keep internal first, then extract near DB/repository layer |
| `_priority_for` | source priority decision helper | shared foundation or ETL helper | extract together with source priority logic |
| `_build_steps_candidate` | convert measurement row into daily aggregation candidate | ETL | move into ETL aggregation service |
| `_is_steps_candidate_better` | choose better daily candidate | ETL | move into ETL aggregation service |
| `_select_best_existing_steps_daily` | compare new candidate with persisted daily rows | ETL | move into ETL aggregation service |
| `POST /aggregate/daily` | incrementally build `daily_metrics` from `measurements` | ETL / admin | stop treating as public API; keep behavior, later wrap as command/job |
| `POST /measurements/deduplicate-steps-total` | destructive deduplication maintenance | ETL / admin | remove from public API surface later |
| `POST /aggregate/daily/rebuild-steps-total` | destructive rebuild of daily aggregates | ETL / admin | remove from public API surface later |
| `GET /daily` | list daily aggregate rows for inspection | API | keep as read API or merge into `metrics` read endpoints |

## Directory Mapping

| Current path | Future directory | Notes |
| --- | --- | --- |
| `app/main.py` | `api/` | Python API entrypoint while Go API is not introduced yet |
| `app/routers/ingest.py` | `api/routers/` or `api/handlers/` | public write API |
| `app/routers/raw.py` | `api/routers/` or `api/handlers/` | debug/read API |
| `app/routers/metrics.py` | `api/routers/` or `api/handlers/` | read API |
| `app/routers/quality.py` | `api/routers/` plus shared helpers | split read diagnostics from calculation helpers |
| `app/routers/normalize.py` | `etl/jobs/` or `etl/tasks/` | convert HTTP-style handler into callable job |
| `app/routers/aggregate.py` | split across `api/` and `etl/` | route wrappers only; read endpoint stays API, write/rebuild logic moves ETL |
| `app/services/aggregate_service.py` | `etl/` plus shared read service | temporary service layer that can be split mechanically later |
| `app/services/normalize_service.py` | `etl/` | temporary normalization service layer that can move with minimal change |
| `app/core/db.py` | `db/` or `shared/` | schema and connection helpers |
| `app/core/config.py` | `db/` or shared config module | keep environment access centralized |
| `app/core/timeutil.py` | shared foundation | avoid duplicating time parsing/conversion |
| `app/routers/ui.py` | `dashboard/` or retire | prototype only |

## Main Risks

- HTTP routes currently perform destructive or maintenance-style DB operations directly.
- DB schema management lives inside application startup code, so schema evolution is implicit.
- ETL and API responsibilities are tightly coupled to the same SQLite access layer.
- `DB_PATH` defaults to `/app/data/...`, which is Docker-oriented and may be awkward outside the container.
- `app/routers/ui.py` is an embedded prototype UI, not a durable dashboard structure.

## Migration Order

1. Extract pure helper functions without changing routes.
2. Split `aggregate.py` conceptually into read API and ETL/admin operations.
3. Create a shared foundation for DB access, config, and time helpers.
4. Re-home ETL-like route bodies behind callable job functions while keeping temporary API wrappers if needed.
5. Move read-only API handlers after the shared foundation is stable.
6. Decide whether `quality.py` stays as internal API diagnostics or becomes ETL reporting support.

## Safe Execution Strategy

- Keep current import paths working while extracting helper functions.
- Prefer introducing thin wrappers over moving everything at once.
- Extract pure functions first, then move DB-facing logic, then move HTTP route files.
- Treat destructive endpoints as admin-only even before they are physically relocated.
- Do not rework Docker or runtime entrypoints until the Python-side boundaries settle.

## Recommended Next Step

Do not move files yet. First split the code conceptually into:

1. public API handlers
2. ETL / maintenance jobs
3. DB schema and repository helpers

After that, move one slice at a time without changing behavior.
