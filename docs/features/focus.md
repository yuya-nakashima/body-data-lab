# 集中時間 + 自己評価 機能仕様

---

## 概要

集中の「量」と「質」を同時に可視化する。

- ストップウォッチ形式で集中時間を記録する
- セッションごとに自己評価スコア（1〜5）を付ける
- 日次で合計・最大・平均スコアを集計する

---

## 記録データ

| フィールド | 型 | 説明 |
|---|---|---|
| `start_at` | ISO 8601 | セッション開始時刻 |
| `end_at` | ISO 8601 | セッション終了時刻 |
| `duration_seconds` | INTEGER | 継続時間（秒）。end_at - start_at で自動算出 |
| `score` | INTEGER (1〜5) | 自己評価スコア。省略可（NULL 許容） |

---

## API エンドポイント

### `POST /focus/sessions`

セッションを記録する。

**リクエスト例:**
```json
{
  "start_at": "2026-03-24T09:00:00+09:00",
  "end_at": "2026-03-24T09:45:00+09:00",
  "score": 4
}
```

**レスポンス例:**
```json
{
  "ok": true,
  "id": 1,
  "duration_seconds": 2700
}
```

---

### `GET /focus/sessions?date=YYYY-MM-DD`

指定日のセッション一覧を返す。

**レスポンス例:**
```json
{
  "ok": true,
  "date": "2026-03-24",
  "sessions": [
    {
      "id": 1,
      "start_at": "2026-03-24T09:00:00+09:00",
      "end_at": "2026-03-24T09:45:00+09:00",
      "duration_seconds": 2700,
      "score": 4
    }
  ]
}
```

---

### `GET /focus/daily?date=YYYY-MM-DD`

日次集計を返す。

**レスポンス例:**
```json
{
  "ok": true,
  "date": "2026-03-24",
  "total_seconds": 7200,
  "max_seconds": 3600,
  "avg_score": 3.8,
  "diff_from_yesterday_seconds": 1800,
  "diff_from_7d_avg_seconds": -600,
  "session_count": 3
}
```

| フィールド | 説明 | データ不足時 |
|---|---|---|
| `total_seconds` | 合計集中時間（秒） | `null` |
| `max_seconds` | 最大集中時間（秒） | `null` |
| `avg_score` | スコアの平均（スコアあり分のみ） | `null` |
| `diff_from_yesterday_seconds` | 前日の合計集中時間との差 | `null` |
| `diff_from_7d_avg_seconds` | 過去7日平均との差 | `null` |
| `session_count` | セッション数 | `0` |

---

## 日次サマリー通知への組み込み

以下の形式で既存の通知メールに追加する：

```
--- 集中時間 ---
合計      : 2時間00分
最大      : 1時間00分
平均スコア: 3.8 / 5
前日差分  : +30分
週平均差  : -10分
```

データ不足時は各項目を「未」と表示する。

---

## 実装状況

- [x] `focus_sessions` テーブル（`app/core/db.py`）
- [x] `POST /focus/sessions`（score なし）
- [x] `GET /focus/sessions`
- [x] `GET /focus/daily`
- [ ] `score` カラムの追加
- [ ] 日次サマリー通知への組み込み

---

## 関連ファイル

- `app/routers/focus.py` — エンドポイント実装
- `app/core/db.py` — テーブル定義
- `docs/features/notifications.md` — 通知仕様
