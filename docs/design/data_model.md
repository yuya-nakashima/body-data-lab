# Data Model

## エンティティ一覧

- `raw_event`: 取得元から受け取った元データ
- `measurement`: 正規化済み観測値
- `daily_metric`: 日次集計値
- `manual_note`: 手動メモ
- `behavior_mode_log`: 行動モード記録
- `training_day_log`: 稽古有無記録
- `analysis_result`: 分析結果キャッシュ

## テーブル候補

| テーブル候補 | 主な役割 | 備考 |
| --- | --- | --- |
| `raw_events` | 生ペイロード保存 | 再正規化のため保持 |
| `measurements` | 観測値の正規化保存 | metric, source, interval を持つ |
| `daily_metrics` | 日次集計値 | UI 表示の基盤 |
| `manual_notes` | 主観メモ | 自由記述とタグ候補 |
| `behavior_modes` | 行動モード記録 | 手動入力中心 |
| `training_days` | 稽古有無 | 二値またはカテゴリ |
| `analysis_results` | 分析出力 | モデル版数を持たせたい |

## リレーション

- `raw_events` 1 対多 `measurements`
- `measurements` 多 対 1 `daily_metrics` への派生元参照があり得る
- `daily_metrics` と `manual_notes` は日付キーで関連づける
- `behavior_modes` と `training_days` も日付キー中心で join する想定

## 生データ / 集計データ / 分析結果の分離

- 生データ
  - 再解釈や重複除去のため保存
- 集計データ
  - 日次、週次、月次など UI 向け
- 分析結果
  - 回帰係数、クラスタラベル、主成分スコアなど
  - 計算条件と版数を付けて再現性を持たせる

## データモデリング上のメモ

- 現状コードの `raw_events`, `measurements`, `daily_metrics` は良い出発点
- 手動入力系エンティティはまだ未実装のため、粒度は今後調整が必要
- 分析結果を永続化するか、その場計算とするかは機能ごとに判断したい

## 関連参照

- [architecture.md](./architecture.md)
- [analytics_design.md](./analytics_design.md)
- [../statistics/time_series/time_series_basics.md](../statistics/time_series/time_series_basics.md)
- [../statistics/multivariate/multivariate_analysis.md](../statistics/multivariate/multivariate_analysis.md)
