# Data Collection

## 取得対象データ

| データ | 主な取得元 | 取得方式 | MVP 優先度 |
| --- | --- | --- | --- |
| 歩数 | Health Connect | 自動 | 高 |
| 心拍数 | Health Connect / ウェアラブル連携 | 自動 | 中 |
| 睡眠 | Health Connect / 外部アプリ連携 | 自動 | 中 |
| 行動モード | 手動入力 | 手動 | 高 |
| 稽古日 / 非稽古日 | 手動入力 | 手動 | 高 |
| 手動メモ | アプリ入力 | 手動 | 高 |
| ストレス、体重、食事、運動内容 | 未確定 | 将来拡張 | 低 |

## 手動入力と自動取得の区分

- 自動取得: 客観データで継続取得しやすいもの
- 手動入力: 文脈や主観評価が必要なもの
- 併用対象: 行動モードの自動推定を将来検討するが、初期は手動入力を正とする

## データ品質の課題

- デバイス差による歩数や心拍の偏り
- 睡眠推定ロジックのアプリ依存差
- 同一期間の重複記録
- 欠測日、遅延同期、タイムゾーン差
- 手動入力の継続負荷

## 品質確保の方針

- 生データを保持し、正規化規則を後から更新できるようにする
- ソース情報と取得時刻を残す
- 欠測や重複を UI に明示する
- 統計比較前に [../statistics/foundations/descriptive_statistics.md](../statistics/foundations/descriptive_statistics.md) 的な要約と分布確認を挟む

## 未確定事項

- Health Connect で取得可能な項目の実装優先順位
- 稽古日の定義粒度
- 行動モードのカテゴリ設計

## 関連参照

- [data_model.md](./data_model.md)
- [risks_and_unknowns.md](./risks_and_unknowns.md)
- [../statistics/experimental_design/design_of_experiments.md](../statistics/experimental_design/design_of_experiments.md)
