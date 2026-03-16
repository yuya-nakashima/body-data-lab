# Screen Design

## 画面一覧

| 画面 | 目的 | MVP 必須 |
| --- | --- | --- |
| ホームダッシュボード | 当日と直近推移の俯瞰 | 必須 |
| 日次詳細 | 1 日の各指標確認 | 必須 |
| データ入力 | 行動モード、稽古有無、メモ入力 | 必須 |
| データ品質確認 | 欠測、重複、同期状態確認 | 推奨 |
| 分析画面 | 相関、回帰、高度分析の表示 | 将来 |
| 設定 / データ連携 | 取得元設定と権限管理 | 必須 |

## 各画面の目的

- ホームダッシュボード
  - 平均歩数、最新睡眠、直近 7 日推移を一目で見る
- 日次詳細
  - 時系列とメモを同時に確認する
- データ入力
  - 手動文脈データを簡単に入れる
- データ品質確認
  - 欠測で誤解しないための安全装置にする

## MVP で必要な画面

- ダッシュボード
- 日次詳細
- 手動入力
- データ連携 / 権限設定

## 分析結果の見せ方

- 基礎分析はグラフと短い要約で示す
- 群比較や回帰は、効果量・対象期間・前提をセットで表示する
- 上級分析は「探索的分析」と明記し、断定的解釈を避ける

## UI 上の注意

- 数値の見せすぎを避け、意味のまとまり単位で表示する
- データが足りない場合は「分析不可」や「参考値」と明示する
- [../statistics/foundations/descriptive_statistics.md](../statistics/foundations/descriptive_statistics.md) や [../statistics/time_series/time_series_basics.md](../statistics/time_series/time_series_basics.md) に対応する見せ方を意識する

## 関連参照

- [analytics_design.md](./analytics_design.md)
- [requirements.md](./requirements.md)
- [feature_mapping.md](./feature_mapping.md)
