# Body Data Lab

Body Data Lab は、身体データの収集・保存・加工・可視化を試作するための開発用ワークスペースです。

現在の実動環境は `app/` 配下の Python/FastAPI 試作です。`api/` `etl/` `db/` `dashboard/` は将来の分離先として置かれているディレクトリで、現時点ではまだ土台の整理段階にあります。

## 最短の起動方法

```bash
docker compose up --build
```

## アクセス URL

- App root: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

開発環境の詳細、ローカル起動方法、保存先、ディレクトリ構成、現状の注意点は [docs/dev_environment.md](./docs/dev_environment.md) を参照してください。
