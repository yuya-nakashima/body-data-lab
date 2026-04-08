# 開発環境ガイド

## このドキュメントの目的

このドキュメントは、Body Data Lab の現在の開発環境を実態ベースで把握するためのガイドです。

- 何が今動くのか
- どう起動するのか
- データがどこへ保存されるのか
- どのディレクトリが何の役割を持つのか
- 現時点で何が未整備なのか

README は入口だけに絞り、このファイルに開発環境の詳細をまとめます。

## 現在の開発環境の全体像

現在このリポジトリで実際に動くアプリは、`app/` 配下の Python/FastAPI 試作です。

想定している将来構成は `api/` `etl/` `db/` `dashboard/` に責務を分ける形ですが、現時点ではその分離はまだ完了していません。`api/` `etl/` `db/` `dashboard/` は主に将来の受け皿であり、今の実装の中心は `app/` です。

現状の挙動は次の通りです。

- FastAPI アプリは `app/main.py` から起動される
- 起動時に SQLite の DB ファイルとテーブルを自動作成する
- API、簡易 UI、正規化・集計・保守系処理が同じ FastAPI アプリに同居している
- Docker 実行を前提にしやすい設定だが、ローカルでも `DB_PATH` を指定すれば起動できる

関連ドキュメント:

- 全体方針: [overview.md](./overview.md)
- `app/` の現状整理: [app_inventory.md](./app_inventory.md)
- プロダクト意図: [design/vision.md](./design/vision.md)

## 起動方法

### Docker での起動

最短手順:

```bash
docker compose up --build
```

`docker-compose.yml` の現在設定:

- サービス名: `app`
- 公開ポート: `8000:8000`
- アプリコード: `./` をコンテナの `/app` に bind mount
- SQLite 保存先: named volume `sqlite_data` を `/app/data` に mount
- `DB_PATH`: `/app/data/body_data_lab.sqlite3`
- 起動コマンド: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

補足:

- `--reload` を使っているため、開発用途向けです
- ソースコードはホスト側の変更が即座に反映されます
- DB は bind mount ではなく Docker volume に保存されるため、SQLite ファイルはワークツリー直下には出ません

### ローカルでの起動

ローカルではプロジェクト直下の `.venv` を使う前提で、`DB_PATH` を明示して起動するのが安全です。

今回確認した実環境:

- 実行 Python: `/Users/webs/workspace/body-data-lab/.venv/bin/python`
- ベース Python: `Python 3.9.6`
- 依存インストール元: `requirements.txt`

補足:

- `Dockerfile` は `python:3.12-slim` ベースです
- 一方で、このマシンでローカルに使えた `python3` は 3.9.6 でした
- そのため、ローカル route import の互換性確保用に `eval_type_backport` を依存へ追加しています
- 将来的にローカル標準を Python 3.12 以上へ揃えられるなら、その時点で再整理して構いません

例:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DB_PATH=./data/body_data_lab.sqlite3 uvicorn app.main:app --reload
```

補足:

- `app/core/config.py` の既定値は `/app/data/body_data_lab.sqlite3` です
- この既定値は Docker 向けなので、ローカル実行時は `DB_PATH=./data/body_data_lab.sqlite3` のように指定する運用を推奨します
- `ensure_db()` が親ディレクトリ作成とテーブル初期化を行うため、`./data` がなくても起動時に作成されます

### ローカルでの最小確認手順

依存インストール後、少なくとも次の確認ができます。

```bash
.venv/bin/python -c "import app.routers.aggregate, app.routers.normalize, app.main; print('imports_ok')"
DB_PATH=./data/body_data_lab.sqlite3 .venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as client:
    print(client.get('/').status_code)
    print(client.get('/docs').status_code)
    print(client.get('/openapi.json').status_code)
PY
```

この確認では以下を見ています。

- route 層 import が通ること
- `app.main` import が通ること
- FastAPI アプリの startup が通ること
- `DB_PATH` に SQLite ファイルが作成されること
- `/docs` と `/openapi.json` が 200 を返すこと

## API / Swagger のアクセス先

アプリ起動後の主な URL:

- Root: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- 簡易 UI: `http://localhost:8000/ui/steps`

Root (`/`) は疎通確認用で、現在の `db_path` も返します。作業前に DB の向き先確認が必要な場合はここを見ると早いです。

## DB とデータファイルの保存場所

### SQLite の保存先

現在の永続データは主に SQLite です。

Docker 実行時:

- コンテナ内パス: `/app/data/body_data_lab.sqlite3`
- 永続化先: Docker named volume `sqlite_data`

ローカル実行時の推奨:

- 推奨パス: `./data/body_data_lab.sqlite3`
- 実際の保存先は `DB_PATH` の値で決まる

### SQLite に入る主な内容

起動時に以下のテーブルが自動作成されます。

- `raw_events`: 取り込んだ生イベント
- `measurements`: 正規化後の計測データ
- `daily_metrics`: 日次集計データ
- `source_priority`: 集計時の優先順位マスタ

### `db/` ディレクトリとの関係

`db/` は将来的にスキーマ管理や初期データ配置の責務を持たせる想定ですが、現時点では主な DB 初期化ロジックは `app/core/db.py` にあります。つまり、現状の DB 管理は「`db/` ディレクトリ中心」ではなく「アプリ起動時のコード中心」です。

## ディレクトリごとの役割

現時点で重要なディレクトリは次の通りです。

- `app/`: 現在の実動アプリ本体
- `app/core/`: 設定、SQLite 接続、スキーマ初期化、共通ユーティリティ
- `app/routers/`: FastAPI の各エンドポイント
- `app/services/`: ルーターから切り出し始めたサービス層
- `data/`: ローカル実行時に SQLite を置く候補ディレクトリ
- `docs/`: 開発・設計ドキュメント
- `docs/design/`: プロダクト設計・要件・分析設計
- `api/`: 将来の API 分離先として確保された場所
- `etl/`: 将来の ETL / バッチ分離先として確保された場所
- `db/`: 将来の DB 管理資産置き場として確保された場所
- `dashboard/`: 将来のダッシュボード分離先として確保された場所

現時点では、`api/` `etl/` `db/` `dashboard/` はまだ骨組み段階です。新しく作業する際は「今どこが実動で、どこが将来の置き場か」を混同しないことが重要です。

## 現在の状態

このプロジェクトは試作段階です。

現在は以下の特徴があります。

- Python/FastAPI で最小限の開発環境を先に動かしている
- 将来的には責務分離や構成整理を想定している
- 一部の集計・正規化・保守操作が HTTP エンドポイントとして暫定公開されている
- 本格運用よりも、データモデル確認と開発の土台づくりを優先している

特に README の将来像と実装の現在地は一致していない部分があるため、実装作業時は README の短い説明だけで判断せず、このファイルと `docs/app_inventory.md` を確認してください。

## 未整備な点 / 今後の課題

現時点の主な課題:

- `DB_PATH` の既定値が Docker 寄りで、ローカル実行時にそのままだと分かりにくい
- スキーマ管理がアプリ起動コードに埋め込まれており、マイグレーション運用がない
- API と ETL / 保守処理の責務分離がまだ不十分
- `api/` `etl/` `db/` `dashboard/` の将来構成と、現在の `app/` 実装の間にギャップがある
- 起動手順は最低限あるが、開発フロー全体はまだ整理途中
- テスト、CI、運用前提、データ投入サンプルの整備はこれから

今後やると良い整理:

- ローカル実行向けの標準 `DB_PATH` 方針を決める
- DB スキーマ管理を `db/` 側へ寄せる
- ETL / 保守系処理を HTTP ルーターから切り離す
- 将来構成に合わせて `app/` から責務を段階的に移す

## AI に作業依頼するときに useful な前提情報

AI に次の作業を依頼する際は、少なくとも次を前提として共有すると進めやすいです。

- 現在の実動エントリポイントは `app/main.py`
- 実行コマンドは `uvicorn app.main:app --reload` 系
- 現在の本体は Go ではなく Python/FastAPI 試作
- DB は SQLite で、保存先は `DB_PATH` で切り替わる
- Docker 実行時は Docker volume、ローカル実行時は `./data/` 配下運用が分かりやすい
- `api/` `etl/` `db/` `dashboard/` は将来構成のための場所で、実装の中心ではない
- `docs/app_inventory.md` は `app/` の責務分解を考えるときの一次資料
- `docs/overview.md` と `docs/design/vision.md` はプロジェクトの方向性確認に有効

AI 向けの依頼文で明示するとよい項目:

- Docker で確認してほしいのか、ローカル実行前提なのか
- `DB_PATH` をどこに向ける想定か
- `app/` を維持したまま整理したいのか、将来構成へ寄せる準備をしたいのか
- 挙動変更を避けたいのか、試作コードの責務整理まで許容するのか

## 関連ファイル

- [README.md](../README.md)
- [overview.md](./overview.md)
- [app_inventory.md](./app_inventory.md)
- [Dockerfile](../Dockerfile)
- [docker-compose.yml](../docker-compose.yml)
- [requirements.txt](../requirements.txt)
- [app/core/config.py](../app/core/config.py)
