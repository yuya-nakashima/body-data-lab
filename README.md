# Body Data Lab

Body Data Lab は、身体データの収集・保存・加工・可視化を試作するための開発用ワークスペースです。

現在の実動環境は `app/` 配下の Python/FastAPI 試作です。`api/` `etl/` `db/` `dashboard/` は将来の分離先として置かれているディレクトリで、現時点ではまだ土台の整理段階にあります。

## 最短の起動方法

```bash
docker compose up --build
```

## ローカル確認用 Python 環境

このリポジトリでは、プロジェクト直下の `.venv` を使う前提で確認しています。

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
DB_PATH=./data/body_data_lab.sqlite3 uvicorn app.main:app --reload
```

この環境で route import と `app.main` import、DB 初期化、`/docs` 到達確認まで実施済みです。詳細は [docs/dev_environment.md](./docs/dev_environment.md) を参照してください。

## アクセス URL

- App root: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

開発環境の詳細、ローカル起動方法、保存先、ディレクトリ構成、現状の注意点は [docs/dev_environment.md](./docs/dev_environment.md) を参照してください。

## 概要

Body Data Lab は、身体データを収集・蓄積・分析するための開発基盤です。開発はローカル環境を中心に進め、ソースコードは GitHub で管理し、実行結果や異常は将来的にメール通知で把握する前提です。

設計上の将来構成は `api/` `etl/` `db/` `dashboard/` ですが、現時点で実際に動くアプリ本体は `app/` 配下の Python/FastAPI 試作です。方向性の確認には [docs/overview.md](./docs/overview.md) と [docs/design/vision.md](./docs/design/vision.md) を参照してください。

## ディレクトリ構成

```text
body-data-lab/
├─ api/         # Go API の将来配置先
├─ app/         # 現在の実動 FastAPI 試作
├─ dashboard/   # Web UI の将来配置先
├─ data/        # ローカル実行時のデータ置き場
├─ db/          # SQLite / schema の将来配置先
├─ docs/        # 開発・設計ドキュメント
├─ etl/         # Python ETL の将来配置先
├─ .env.example # 環境変数テンプレート
├─ .gitignore
├─ Dockerfile
├─ Makefile
├─ README.md
├─ docker-compose.yml
└─ requirements.txt
```

## 前提環境

- Git
- Docker / Docker Compose
- Python 3.9 以上
- `pip`
- `sqlite3`
- Go 1.22 以上

補足:

- すぐに動作確認したい場合は Docker 起動が最短です
- `api/` と `etl/` は現時点ではプレースホルダ中心のため、`make run-api` と `make run-etl` は将来実装向けの入口です

## セットアップ手順

1. リポジトリを clone します。
2. 環境変数テンプレートをコピーします。

```bash
cp .env.example .env
```

現時点の FastAPI 試作では `.env` 自動読込は実装していないため、ローカル実行時は `.env` の値をシェルで `export` するか、コマンドの前置で環境変数を渡してください。

3. 必要なディレクトリを作成します。

```bash
make setup
```

4. Docker で起動する場合は、そのまま次を実行します。

```bash
docker compose up --build
```

5. ローカル Python 環境で起動する場合は、仮想環境を作成して依存を入れます。

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
DB_PATH=./data/body_data_lab.sqlite3 uvicorn app.main:app --reload
```

## 実行方法

現在すぐに確認できる方法:

- Docker: `docker compose up --build`
- ローカル FastAPI: `DB_PATH=./data/body_data_lab.sqlite3 uvicorn app.main:app --reload`

### Docker で ETL を実行する

API と同じ SQLite volume を使って ETL を手動実行するには:

```bash
docker compose run --rm etl
```

実行ログは標準出力に出力されます。メール通知は mailpit (`http://localhost:8025`) で確認できます。

Makefile の補助コマンド:

- `make setup`: `db/` `etl/` `docs/` を作成
- `make db-init`: `db/body_data_lab.sqlite3` を作成して SQLite 接続確認
- `make run-api`: `api/` 配下の Go API を起動
- `make run-etl`: `etl/` 配下の Python ETL を起動

DB パスの扱い:

- `.env.example` と `make db-init` は、将来の `db/` 集約を見据えて `db/body_data_lab.sqlite3` を例にしています
- 現在の FastAPI 試作は `DB_PATH` を明示すれば任意パスで動作し、既存の開発確認では `./data/body_data_lab.sqlite3` を利用しています

主なアクセス先:

- App root: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Git 運用ルール

- `.env` は Git に含めず、`.env.example` のみ管理する
- SQLite ファイル（`*.db` `*.sqlite` `*.sqlite3`）は Git に含めない
- 作業前に `git pull`、作業後に `git status` で差分を確認する
- 小さな単位で commit し、GitHub に push して管理する
- 設計変更時は `docs/` を先に確認し、既存ドキュメントと矛盾させない
