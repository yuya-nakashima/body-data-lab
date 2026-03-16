# Risks And Unknowns

## まだ未確定なこと

- Android ローカル中心で進めるか、API 主体で進めるか
- 疲労やコンディションを単独手入力にするか、推定指標にするか
- 行動モードのカテゴリ数と粒度
- 高度分析の実行場所と更新頻度

## 今後検証が必要なこと

- Health Connect 由来データの欠測と遅延の実態
- 歩数、睡眠、心拍のうちどれが最も安定運用できるか
- 手動入力の継続可能性
- データ量が少ない段階でどこまで分析して意味があるか

## 技術的リスク

- 取得元差異による値の非一貫性
- 端末依存のバックグラウンド同期制約
- 高度分析導入時の計算負荷と実装複雑化
- モデル版数管理や再計算管理の不足

## 統計的解釈上の注意

- 相関を因果と誤認しやすい
- 個人時系列データに独立標本前提をそのまま当てにくい
- 小標本での有意差判定は不安定
- 探索的分析の結果を過信しやすい

## 運用上の注意

- データが欠けているのに「改善した」と見えてしまうリスク
- 手動入力の定義ぶれによるラベル汚染
- 介入実験の実施負荷

## 関連参照

- [data_collection.md](./data_collection.md)
- [analytics_design.md](./analytics_design.md)
- [../statistics/inference/hypothesis_testing.md](../statistics/inference/hypothesis_testing.md)
- [../statistics/time_series/stationary_process.md](../statistics/time_series/stationary_process.md)
