# body-data-lab — Claude Code Instructions

## プロジェクト概要

FastAPI + SQLite によるバックエンド。健康データの取り込み・正規化・集計・振り返り・通知を担う。

## 技術スタック

- Python 3.12 / FastAPI / SQLite（`db/body_data_lab.sqlite3`）
- Docker Compose（`docker-compose.prod.yml` が本番用）
- AWS EC2（t3.micro）+ nginx + Let's Encrypt
- ETL: `etl/` 以下のスクリプトを cron で実行
- LINE Messaging API で毎晩 19:00 JST に通知

## ディレクトリ構成

```
app/
  core/        # DB接続・設定・時刻ユーティリティ
  routers/     # APIエンドポイント（1ファイル1リソース）
  services/    # ビジネスロジック（LINE通知など）
etl/           # cronで実行するスクリプト
db/            # SQLiteファイル
```

## コーディング規則

- Python 3.9 互換を意識（`X | None` は使わず `Optional[X]` または `from __future__ import annotations`）
- DB アクセスは `app/core/db.py` の `get_conn()` を使う
- テーブル追加は `ensure_db()` 内に `CREATE TABLE IF NOT EXISTS` で追記
- 新しいエンドポイントは `app/routers/` に追加し `app/main.py` で `include_router`

## 連携

- **ninja-habits-android** がこの API・WebUI（`/ui/*`）を直接呼び出している。API変更時は Android 側への影響を確認する。

## デプロイ

```bash
# EC2に手動デプロイ
ssh body-data-lab "cd ~/body-data-lab && git pull && docker-compose -f docker-compose.prod.yml up -d --build app"
```

## cron（EC2上 /etc/cron.d/）

- `body-data-lab-morning`: 毎日 10:00 UTC（19:00 JST）→ `etl/morning_notify.py`
- `body-data-lab-etl`: 毎日 21:00 UTC（06:00 JST）→ ETL実行
- docker-compose はフルパス `/usr/local/bin/docker-compose` で指定すること
