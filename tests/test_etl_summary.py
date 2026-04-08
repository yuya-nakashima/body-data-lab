"""
etl/main.py の build_summary_message と
app/services/aggregate_service.py の get_daily_summary のテスト。
"""
from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from unittest.mock import patch

import pytest

from etl.main import build_summary_message, _fmt_steps, _fmt_diff


# ---------------------------------------------------------------------------
# _fmt_steps / _fmt_diff（フォーマットヘルパー）
# ---------------------------------------------------------------------------

class TestFmtSteps:
    def test_normal_value(self):
        assert _fmt_steps(8432.0) == "8,432 歩"

    def test_zero(self):
        assert _fmt_steps(0) == "0 歩"

    def test_none_returns_未(self):
        assert _fmt_steps(None) == "未"

    def test_truncates_float(self):
        assert _fmt_steps(8432.9) == "8,432 歩"


class TestFmtDiff:
    def test_positive_has_plus_sign(self):
        assert _fmt_diff(1204.0) == "+1,204 歩"

    def test_negative_has_minus_sign(self):
        assert _fmt_diff(-568.0) == "-568 歩"

    def test_zero_has_plus_sign(self):
        assert _fmt_diff(0) == "+0 歩"

    def test_none_returns_未(self):
        assert _fmt_diff(None) == "未"


# ---------------------------------------------------------------------------
# build_summary_message（メール本文生成）
# ---------------------------------------------------------------------------

class TestBuildSummaryMessage:
    def _make_summary(self, **kwargs) -> dict:
        base = {
            "target_day": "2026-04-07",
            "metric": "steps_total",
            "current_value": 8432.0,
            "prev_value": 7228.0,
            "day_diff": 1204.0,
            "week_avg": 9000.0,
            "week_diff": -568.0,
        }
        base.update(kwargs)
        return base

    def test_contains_target_day(self):
        msg = build_summary_message(self._make_summary())
        assert "2026-04-07" in msg

    def test_contains_current_value(self):
        msg = build_summary_message(self._make_summary())
        assert "8,432 歩" in msg

    def test_contains_positive_day_diff(self):
        msg = build_summary_message(self._make_summary())
        assert "+1,204 歩" in msg

    def test_contains_negative_week_diff(self):
        msg = build_summary_message(self._make_summary())
        assert "-568 歩" in msg

    def test_all_未_when_no_current_value(self):
        summary = self._make_summary(
            current_value=None,
            prev_value=None,
            day_diff=None,
            week_avg=None,
            week_diff=None,
        )
        msg = build_summary_message(summary)
        # 当日値・前日差分・週平均差 の3行すべてに「未」が含まれる
        lines = msg.splitlines()
        未_lines = [l for l in lines if "未" in l]
        assert len(未_lines) == 3

    def test_week_diff_未_when_week_data_insufficient(self):
        summary = self._make_summary(week_avg=None, week_diff=None)
        msg = build_summary_message(summary)
        assert "週平均差  : 未" in msg

    def test_day_diff_未_when_prev_missing(self):
        summary = self._make_summary(prev_value=None, day_diff=None)
        msg = build_summary_message(summary)
        assert "前日差分  : 未" in msg

    def test_contains_jst_timestamp(self):
        msg = build_summary_message(self._make_summary())
        assert "JST" in msg

    def test_subject_format(self):
        """etl/main.py の main() で生成するサブジェクトの形式確認"""
        target_day = "2026-04-07"
        expected_subject = f"[Body Data Lab] 日次サマリー {target_day}"
        assert expected_subject == "[Body Data Lab] 日次サマリー 2026-04-07"


# ---------------------------------------------------------------------------
# get_daily_summary（DB アクセスあり・インメモリ SQLite でテスト）
# ---------------------------------------------------------------------------

def _insert_daily(conn: sqlite3.Connection, day: str, value: float) -> None:
    conn.execute(
        """
        INSERT INTO daily_metrics (day, source, metric, value, unit, updated_at)
        VALUES (?, 'health_connect', 'steps_total', ?, 'count', '2026-04-08T00:00:00+00:00')
        ON CONFLICT(day, source, metric) DO UPDATE SET value = excluded.value
        """,
        (day, value),
    )
    conn.commit()


@pytest.fixture()
def tmp_db(tmp_path, monkeypatch):
    """一時ファイル DB を用意し、DB_PATH をパッチして ensure_db() を実行する。"""
    db_file = str(tmp_path / "test.sqlite3")
    monkeypatch.setattr("app.core.db.DB_PATH", db_file)
    monkeypatch.setattr("app.core.config.DB_PATH", db_file)

    from app.core.db import ensure_db
    ensure_db()

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


class TestGetDailySummary:
    def test_all_data_present_calculates_correctly(self, tmp_db):
        today = date(2026, 4, 8)
        target = today - timedelta(days=1)  # 2026-04-07

        # 7 日分のデータを挿入
        for i in range(7):
            day = (target - timedelta(days=i)).isoformat()
            _insert_daily(tmp_db, day, 8000.0 + i * 100)

        # prev_day (2026-04-06) の値は 8100
        # target_day (2026-04-07) の値は 8000
        # week_avg = (8000 + 8100 + 8200 + 8300 + 8400 + 8500 + 8600) / 7 = 8300

        with patch("app.services.aggregate_service.get_conn", return_value=tmp_db):
            from app.services.aggregate_service import get_daily_summary
            result = get_daily_summary(target_day=target.isoformat())

        assert result["current_value"] == pytest.approx(8000.0)
        assert result["prev_value"] == pytest.approx(8100.0)
        assert result["day_diff"] == pytest.approx(-100.0)
        assert result["week_avg"] == pytest.approx(8300.0)
        assert result["week_diff"] == pytest.approx(-300.0)

    def test_no_data_returns_none_values(self, tmp_db):
        with patch("app.services.aggregate_service.get_conn", return_value=tmp_db):
            from app.services.aggregate_service import get_daily_summary
            result = get_daily_summary(target_day="2026-04-07")

        assert result["current_value"] is None
        assert result["prev_value"] is None
        assert result["day_diff"] is None
        assert result["week_avg"] is None
        assert result["week_diff"] is None

    def test_week_diff_none_when_fewer_than_7_days(self, tmp_db):
        target = "2026-04-07"
        prev = "2026-04-06"
        _insert_daily(tmp_db, target, 8000.0)
        _insert_daily(tmp_db, prev, 7500.0)
        # 7日分揃っていないので week_avg は None

        with patch("app.services.aggregate_service.get_conn", return_value=tmp_db):
            from app.services.aggregate_service import get_daily_summary
            result = get_daily_summary(target_day=target)

        assert result["current_value"] == pytest.approx(8000.0)
        assert result["day_diff"] == pytest.approx(500.0)
        assert result["week_avg"] is None
        assert result["week_diff"] is None

    def test_day_diff_none_when_prev_missing(self, tmp_db):
        target = "2026-04-07"
        _insert_daily(tmp_db, target, 8000.0)
        # 前日データなし

        with patch("app.services.aggregate_service.get_conn", return_value=tmp_db):
            from app.services.aggregate_service import get_daily_summary
            result = get_daily_summary(target_day=target)

        assert result["current_value"] == pytest.approx(8000.0)
        assert result["prev_value"] is None
        assert result["day_diff"] is None

    def test_default_target_day_is_yesterday(self, tmp_db, monkeypatch):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        _insert_daily(tmp_db, yesterday, 5000.0)

        with patch("app.services.aggregate_service.get_conn", return_value=tmp_db):
            from app.services.aggregate_service import get_daily_summary
            result = get_daily_summary()  # target_day 未指定

        assert result["target_day"] == yesterday
        assert result["current_value"] == pytest.approx(5000.0)
