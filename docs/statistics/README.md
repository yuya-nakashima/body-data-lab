# 統計知識ドキュメント

## 目的

`docs/statistics/` は、Body Data Lab で扱う分析機能の背景知識を、統計検定 1 級レベルまで意識して整理するためのフォルダです。受験対策ノートではなく、概念整理とアプリへの接続を重視しています。

## ディレクトリ構成

- `foundations/`: 記述統計、確率、分布、線形代数の基礎
- `inference/`: 推定、検定、漸近理論
- `regression/`: 単回帰、重回帰、一般化線形モデル
- `multivariate/`: 多変量解析、主成分分析、因子分析、判別、クラスタ
- `time_series/`: 時系列の基礎、定常過程、ARMA/ARIMA、スペクトル
- `stochastic/`: 確率過程、マルコフ連鎖
- `bayesian/`: ベイズ統計
- `experimental_design/`: 実験計画、分散分析
- `appendix/`: 記号、用語、学習ロードマップ

## 学習順序

推奨順は次の通りです。

1. [appendix/notation.md](./appendix/notation.md)
2. [foundations/descriptive_statistics.md](./foundations/descriptive_statistics.md)
3. [foundations/probability.md](./foundations/probability.md)
4. [foundations/distribution.md](./foundations/distribution.md)
5. [inference/estimation.md](./inference/estimation.md)
6. [inference/hypothesis_testing.md](./inference/hypothesis_testing.md)
7. [regression/simple_regression.md](./regression/simple_regression.md)
8. [regression/multiple_regression.md](./regression/multiple_regression.md)
9. [time_series/time_series_basics.md](./time_series/time_series_basics.md)
10. [appendix/study_roadmap.md](./appendix/study_roadmap.md)

## Body Data Lab との関係

- 歩数、心拍、睡眠の要約には記述統計と分布理解が必要です。
- 疲労やコンディションの傾向評価には推定、検定、回帰、多変量解析が関わります。
- 日次推移や習慣の変化には時系列と確率過程が関わります。
- 個人データの不確実性や逐次更新にはベイズ統計が候補になります。

## 読み進める際の注意

- 数式は理解の足場として記載していますが、厳密証明は最小限です。
- 実装方針は [../design/analytics_design.md](../design/analytics_design.md) を優先し、ここでは知識整理に集中します。
- 未確定な分析仕様は設計書側の記述に合わせて更新する想定です。
