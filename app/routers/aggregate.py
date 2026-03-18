from fastapi import APIRouter

from app.services.aggregate_service import (
    aggregate_daily_metrics,
    deduplicate_steps_total_measurements_job,
    list_daily_metrics,
    rebuild_steps_total_daily_metrics,
)

router = APIRouter(tags=["aggregate"])


@router.post("/aggregate/daily")
def aggregate_daily(
    metric: str = "steps_total",
    source: str | None = None,
    limit: int = 500,
    since_measurement_id: int = 0,
):
    limit = max(1, min(limit, 5000))
    since_measurement_id = max(0, since_measurement_id)
    return aggregate_daily_metrics(
        metric=metric,
        source=source,
        limit=limit,
        since_measurement_id=since_measurement_id,
    )


@router.post("/measurements/deduplicate-steps-total")
def deduplicate_steps_total_measurements():
    return deduplicate_steps_total_measurements_job()


@router.post("/aggregate/daily/rebuild-steps-total")
def rebuild_steps_total_daily(limit: int = 5000):
    limit = max(1, min(limit, 5000))
    return rebuild_steps_total_daily_metrics(limit=limit)


@router.get("/daily")
def list_daily(day: str | None = None, metric: str | None = None, limit: int = 50):
    limit = max(1, min(limit, 500))
    return list_daily_metrics(day=day, metric=metric, limit=limit)
