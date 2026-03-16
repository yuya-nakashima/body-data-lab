# API Design

## API が必要になる責務

- データ受信
- 正規化ジョブの起点
- 再集計の起点
- 分析結果取得
- 品質確認用エンドポイント

## Android ローカル完結案との比較

| 観点 | ローカル完結 | API あり |
| --- | --- | --- |
| 初期実装速度 | 高い | やや低い |
| オフライン利用 | 強い | 設計次第 |
| 高度分析 | 制約あり | 拡張しやすい |
| 再計算 | 端末依存 | サーバーで一元化しやすい |
| 運用負荷 | 低い | 上がる |

## 将来サーバー連携する場合の方向性

- `POST /ingest` 系で生データ受信
- `POST /normalize` や `POST /aggregate` 系で再処理
- `GET /metrics/daily` 系で集計結果取得
- `GET /analysis/...` 系で高度分析結果取得

## 現状コードとの接続

- 既存の FastAPI には ingest, normalize, aggregate, quality, metrics, ui の責務が見える
- 現状はプロトタイプ API としては十分だが、正式な公開 API 仕様として固定するには整理が必要

## API 設計上の注意

- 取得元ソースと時刻情報を落とさない
- 同一データの重複送信を許容しつつ冪等に扱う
- 分析結果は対象期間、モデル版数、生成時刻を返したい

## 未確定事項

- Android から直接 API に送るか、中継なしローカル保存を基本にするか
- 認証を早期に入れるか
- 将来マルチユーザー化するか

## 関連参照

- [architecture.md](./architecture.md)
- [data_model.md](./data_model.md)
- [non_functional_requirements.md](./non_functional_requirements.md)
