from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=9))


def utc_iso_to_jst_day(iso_str: str) -> str:
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return dt.astimezone(JST).date().isoformat()
