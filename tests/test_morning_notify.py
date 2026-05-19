from __future__ import annotations

from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, call, patch

import pytest

from etl.morning_notify import (
    build_daily_goals_section,
    build_habits_section,
    build_wish_list_section,
    main,
)

JST = timezone(timedelta(hours=9))


# ---------------------------------------------------------------------------
# build_habits_section
# ---------------------------------------------------------------------------

class TestBuildHabitsSection:
    def test_empty_groups(self):
        assert build_habits_section([]) == ""

    def test_unchecked_only_returns_empty(self):
        groups = [
            {"name": "健康", "items": [{"content": "水2L", "done": 0, "count": 0}]}
        ]
        assert build_habits_section(groups) == ""

    def test_checked_shown_unchecked_omitted(self):
        groups = [
            {
                "name": "健康",
                "items": [
                    {"content": "朝のストレッチ", "done": 1, "count": 1},
                    {"content": "水2L", "done": 0, "count": 0},
                ],
            }
        ]
        result = build_habits_section(groups)
        assert "【前日の習慣スタック】" in result
        assert "✓ 朝のストレッチ" in result
        assert "水2L" not in result

    def test_count_shown_when_greater_than_1(self):
        groups = [
            {"name": "運動", "items": [{"content": "腕立て", "done": 1, "count": 3}]}
        ]
        result = build_habits_section(groups)
        assert "✓ 腕立て × 3" in result

    def test_count_not_shown_when_1(self):
        groups = [
            {"name": "運動", "items": [{"content": "腕立て", "done": 1, "count": 1}]}
        ]
        result = build_habits_section(groups)
        assert "× 1" not in result
        assert "✓ 腕立て" in result

    def test_group_with_no_done_items_omitted(self):
        groups = [{"name": "空グループ", "items": []}]
        assert build_habits_section(groups) == ""

    def test_only_done_groups_shown(self):
        groups = [
            {"name": "グループA", "items": [{"content": "A1", "done": 1, "count": 1}]},
            {"name": "グループB", "items": [{"content": "B1", "done": 0, "count": 0}]},
        ]
        result = build_habits_section(groups)
        assert "▷ グループA" in result
        assert "グループB" not in result


# ---------------------------------------------------------------------------
# build_wish_list_section (smoke test — already existed before this change)
# ---------------------------------------------------------------------------

class TestBuildWishListSection:
    def test_empty(self):
        assert build_wish_list_section([]) == ""

    def test_renders_items(self):
        categories = [{"name": "旅行", "items": ["京都", "沖縄"]}]
        result = build_wish_list_section(categories)
        assert "【やりたいことリスト】" in result
        assert "▷ 旅行" in result
        assert "・京都" in result
        assert "・沖縄" in result

    def test_empty_category_shows_placeholder(self):
        categories = [{"name": "未定", "items": []}]
        result = build_wish_list_section(categories)
        assert "（なし）" in result


# ---------------------------------------------------------------------------
# build_daily_goals_section
# ---------------------------------------------------------------------------

class TestBuildDailyGoalsSection:
    def test_empty_returns_empty(self):
        assert build_daily_goals_section([]) == ""

    def test_all_undone_returns_empty(self):
        goals = [{"content": "読書", "done": 0, "count": 0}]
        assert build_daily_goals_section(goals) == ""

    def test_done_goal_shown(self):
        goals = [{"content": "ブログを書く", "done": 1, "count": 1}]
        result = build_daily_goals_section(goals)
        assert "【前日の目標達成】" in result
        assert "✓ ブログを書く" in result

    def test_undone_goal_omitted(self):
        goals = [
            {"content": "ブログを書く", "done": 1, "count": 1},
            {"content": "読書30分", "done": 0, "count": 0},
        ]
        result = build_daily_goals_section(goals)
        assert "✓ ブログを書く" in result
        assert "読書30分" not in result

    def test_count_shown_when_greater_than_1(self):
        goals = [{"content": "体重測定", "done": 1, "count": 3}]
        result = build_daily_goals_section(goals)
        assert "✓ 体重測定 × 3" in result

    def test_count_not_shown_when_1(self):
        goals = [{"content": "体重測定", "done": 1, "count": 1}]
        result = build_daily_goals_section(goals)
        assert "× 1" not in result
        assert "✓ 体重測定" in result

    def test_minimum_goal_shown_when_present(self):
        goals = [{"content": "瞑想30分", "done": 1, "count": 1, "minimum_goal": "1分だけでOK"}]
        result = build_daily_goals_section(goals)
        assert "ミニマム: 1分だけでOK" in result

    def test_minimum_goal_omitted_when_none(self):
        goals = [{"content": "瞑想30分", "done": 1, "count": 1, "minimum_goal": None}]
        result = build_daily_goals_section(goals)
        assert "ミニマム" not in result


# ---------------------------------------------------------------------------
# main() — LINE + mail both called with same message
# ---------------------------------------------------------------------------

SAMPLE_REFLECTION = {
    "day": "2026-05-13",
    "want_to_do": "読書",
    "anxiety": "",
    "unconscious_desire": "",
    "free_text": "良い一日だった",
}

SAMPLE_HABITS = [
    {
        "name": "健康",
        "items": [
            {"content": "ストレッチ", "done": 1, "count": 1},
            {"content": "散歩", "done": 0, "count": 0},
        ],
    }
]

SAMPLE_WISHES = [{"name": "旅行", "items": ["京都"]}]

SAMPLE_GOALS = [
    {"content": "ブログを書く", "done": 1, "count": 1, "minimum_goal": "タイトルだけ考える"},
    {"content": "読書30分", "done": 0, "count": 0, "minimum_goal": None},
]


@pytest.fixture()
def mock_db(monkeypatch):
    monkeypatch.setattr("etl.morning_notify.fetch_reflection", lambda d: SAMPLE_REFLECTION)
    monkeypatch.setattr("etl.morning_notify.fetch_habits", lambda d: SAMPLE_HABITS)
    monkeypatch.setattr("etl.morning_notify.fetch_wish_list", lambda: SAMPLE_WISHES)
    monkeypatch.setattr("etl.morning_notify.fetch_daily_goals", lambda d: SAMPLE_GOALS)


class TestMain:
    def test_section_order(self, mock_db):
        with patch("etl.morning_notify.send_line") as mock_line, \
             patch("etl.morning_notify.send_mail"):
            main()

        msg = mock_line.call_args[0][0]
        pos_goals = msg.index("前日の目標達成")
        pos_habits = msg.index("前日の習慣スタック")
        pos_reflection = msg.index("振り返り")
        pos_wishes = msg.index("やりたいことリスト")
        assert pos_goals < pos_habits < pos_reflection < pos_wishes

    def test_sends_line_and_mail_with_same_message(self, mock_db):
        with patch("etl.morning_notify.send_line") as mock_line, \
             patch("etl.morning_notify.send_mail") as mock_mail:
            main()

        mock_line.assert_called_once()
        mock_mail.assert_called_once()

        line_msg = mock_line.call_args[0][0]
        mail_body = mock_mail.call_args[1]["body"]
        assert line_msg == mail_body

    def test_mail_subject_contains_yesterday(self, mock_db):
        with patch("etl.morning_notify.send_line"), \
             patch("etl.morning_notify.send_mail") as mock_mail:
            main()

        subject = mock_mail.call_args[1]["subject"]
        assert subject.startswith("[Body Data Lab] 振り返り ")

    def test_message_contains_reflection(self, mock_db):
        with patch("etl.morning_notify.send_line") as mock_line, \
             patch("etl.morning_notify.send_mail"):
            main()

        msg = mock_line.call_args[0][0]
        assert "振り返り" in msg
        assert "読書" in msg
        assert "良い一日だった" in msg

    def test_message_contains_goals(self, mock_db):
        with patch("etl.morning_notify.send_line") as mock_line, \
             patch("etl.morning_notify.send_mail"):
            main()

        msg = mock_line.call_args[0][0]
        assert "前日の目標達成" in msg
        assert "✓ ブログを書く" in msg
        assert "読書30分" not in msg

    def test_message_contains_habits(self, mock_db):
        with patch("etl.morning_notify.send_line") as mock_line, \
             patch("etl.morning_notify.send_mail"):
            main()

        msg = mock_line.call_args[0][0]
        assert "前日の習慣スタック" in msg
        assert "✓ ストレッチ" in msg
        assert "散歩" not in msg

    def test_message_contains_wish_list(self, mock_db):
        with patch("etl.morning_notify.send_line") as mock_line, \
             patch("etl.morning_notify.send_mail"):
            main()

        msg = mock_line.call_args[0][0]
        assert "やりたいことリスト" in msg
        assert "京都" in msg

    def test_no_habits_omits_section(self, monkeypatch):
        monkeypatch.setattr("etl.morning_notify.fetch_reflection", lambda d: SAMPLE_REFLECTION)
        monkeypatch.setattr("etl.morning_notify.fetch_habits", lambda d: [])
        monkeypatch.setattr("etl.morning_notify.fetch_wish_list", lambda: SAMPLE_WISHES)
        monkeypatch.setattr("etl.morning_notify.fetch_daily_goals", lambda d: [])

        with patch("etl.morning_notify.send_line") as mock_line, \
             patch("etl.morning_notify.send_mail"):
            main()

        msg = mock_line.call_args[0][0]
        assert "前日の習慣スタック" not in msg

    def test_no_wish_list_omits_section(self, monkeypatch):
        monkeypatch.setattr("etl.morning_notify.fetch_reflection", lambda d: SAMPLE_REFLECTION)
        monkeypatch.setattr("etl.morning_notify.fetch_habits", lambda d: SAMPLE_HABITS)
        monkeypatch.setattr("etl.morning_notify.fetch_wish_list", lambda: [])
        monkeypatch.setattr("etl.morning_notify.fetch_daily_goals", lambda d: [])

        with patch("etl.morning_notify.send_line") as mock_line, \
             patch("etl.morning_notify.send_mail"):
            main()

        msg = mock_line.call_args[0][0]
        assert "やりたいことリスト" not in msg

    def test_line_failure_does_not_suppress_exception(self, mock_db):
        with patch("etl.morning_notify.send_line", side_effect=RuntimeError("LINE down")), \
             patch("etl.morning_notify.send_mail") as mock_mail:
            with pytest.raises(RuntimeError, match="LINE down"):
                main()

        mock_mail.assert_not_called()

    def test_mail_failure_does_not_suppress_exception(self, mock_db):
        with patch("etl.morning_notify.send_line"), \
             patch("etl.morning_notify.send_mail", side_effect=RuntimeError("SMTP down")):
            with pytest.raises(RuntimeError, match="SMTP down"):
                main()

    def test_uses_jst_date_not_utc(self, monkeypatch):
        # UTC 15:30 = JST 翌日 00:30。UTC基準だと yesterday がずれる。
        # JST基準なら正しく JST 日付が使われることを確認する。
        jst_now = datetime(2026, 5, 14, 0, 30, tzinfo=JST)  # JST 2026-05-14 00:30
        monkeypatch.setattr("etl.morning_notify.datetime", _MockDatetime(jst_now))

        captured = {}

        def fake_fetch_reflection(d):
            captured["yesterday"] = d
            return SAMPLE_REFLECTION

        def fake_fetch_habits(d):
            captured["habits_day"] = d
            return []

        def fake_fetch_daily_goals(d):
            captured["goals_day"] = d
            return []

        monkeypatch.setattr("etl.morning_notify.fetch_reflection", fake_fetch_reflection)
        monkeypatch.setattr("etl.morning_notify.fetch_habits", fake_fetch_habits)
        monkeypatch.setattr("etl.morning_notify.fetch_daily_goals", fake_fetch_daily_goals)
        monkeypatch.setattr("etl.morning_notify.fetch_wish_list", lambda: [])

        with patch("etl.morning_notify.send_line"), patch("etl.morning_notify.send_mail"):
            main()

        assert captured["yesterday"] == "2026-05-13"
        assert captured["habits_day"] == "2026-05-13"
        assert captured["goals_day"] == "2026-05-13"


class _MockDatetime:
    """datetime.now(tz) を差し替えるための最小スタブ。"""

    def __init__(self, fixed: datetime):
        self._fixed = fixed

    def now(self, tz=None):
        if tz is not None:
            return self._fixed.astimezone(tz)
        return self._fixed
