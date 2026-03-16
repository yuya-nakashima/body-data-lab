# Development Phases

## フェーズ 1: MVP

### ゴール

- 身体データの取り込み、保存、日次集計、基本可視化を成立させる
- 手動メモと文脈データを最低限結びつける

### 主な対象

- 歩数
- 睡眠
- 心拍
- 行動モード
- 稽古有無
- 手動メモ

### 対応する統計知識

- [記述統計](../statistics/foundations/descriptive_statistics.md)
- [時系列の基礎](../statistics/time_series/time_series_basics.md)

## フェーズ 2: 統計 2 級レベルの分析拡張

### ゴール

- 群比較、相関、単回帰、重回帰を用いて仮説検証の入口を作る
- データ品質に応じて分析可能範囲を制御する

### 主な対象

- 稽古日 / 非稽古日の比較
- 睡眠と疲労メモの関係
- 複数要因での疲労説明

### 対応する統計知識

- [推定](../statistics/inference/estimation.md)
- [仮説検定](../statistics/inference/hypothesis_testing.md)
- [単回帰](../statistics/regression/simple_regression.md)
- [重回帰](../statistics/regression/multiple_regression.md)
- [分散分析](../statistics/experimental_design/analysis_of_variance.md)

## フェーズ 3: 統計 1 級レベルの分析拡張

### ゴール

- 多変量解析、時系列モデル、ベイズ、状態遷移を段階導入する
- 学習用ドキュメントと分析機能を相互更新できる状態にする

### 主な対象

- コンディション合成指標
- 行動パターン抽出
- 短期予測
- 状態推定

### 対応する統計知識

- [主成分分析](../statistics/multivariate/principal_component_analysis.md)
- [因子分析](../statistics/multivariate/factor_analysis.md)
- [ARMA / ARIMA](../statistics/time_series/arma_arima.md)
- [ベイズ統計](../statistics/bayesian/bayesian_statistics.md)
- [マルコフ連鎖](../statistics/stochastic/markov_chain.md)

## フェーズ移行の判断材料

- データ蓄積日数
- 欠測率と手動入力継続率
- 分析機能の解釈可能性
- 実装負荷と保守可能性

## 関連参照

- [product_scope.md](./product_scope.md)
- [analytics_design.md](./analytics_design.md)
- [../statistics/appendix/study_roadmap.md](../statistics/appendix/study_roadmap.md)
