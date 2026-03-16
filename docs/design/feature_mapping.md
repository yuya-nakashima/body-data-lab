# Feature Mapping

## 機能と統計知識の対応表

| 機能 | 目的 | 統計知識 | 参照 |
| --- | --- | --- | --- |
| 平均歩数表示 | 全体傾向の把握 | 記述統計 | [記述統計](../statistics/foundations/descriptive_statistics.md) |
| 睡眠時間のヒストグラム | 分布形状の把握 | 分布、記述統計 | [分布](../statistics/foundations/distribution.md) |
| 7 日移動平均 | トレンド把握 | 時系列の基礎 | [時系列の基礎](../statistics/time_series/time_series_basics.md) |
| 稽古日 / 非稽古日比較 | 条件差の確認 | 仮説検定、分散分析 | [仮説検定](../statistics/inference/hypothesis_testing.md) |
| 睡眠と歩数の関係表示 | 関係探索 | 単回帰 | [単回帰](../statistics/regression/simple_regression.md) |
| 疲労スコア説明モデル | 複数要因の把握 | 重回帰 | [重回帰](../statistics/regression/multiple_regression.md) |
| カウントや二値状態の予測 | 目的変数型に合わせた分析 | GLM | [一般化線形モデル](../statistics/regression/generalized_linear_models.md) |
| 疲労スコア候補作成 | 合成指標の生成 | 主成分分析、因子分析 | [主成分分析](../statistics/multivariate/principal_component_analysis.md) |
| 行動モード候補抽出 | パターン発見 | クラスタ分析 | [クラスタ分析](../statistics/multivariate/cluster_analysis.md) |
| 疲労状態分類 | ラベル付き分類 | 判別分析、GLM | [判別分析](../statistics/multivariate/discriminant_analysis.md) |
| 翌日傾向の予測 | 時間依存の利用 | ARMA / ARIMA | [ARMA / ARIMA](../statistics/time_series/arma_arima.md) |
| 周期パターン探索 | 生活リズム把握 | スペクトル解析 | [スペクトル解析](../statistics/time_series/spectral_analysis.md) |
| 状態遷移表示 | 行動や疲労の遷移把握 | マルコフ連鎖 | [マルコフ連鎖](../statistics/stochastic/markov_chain.md) |
| 個人通常状態の更新 | 不確実性込みの推定 | ベイズ統計 | [ベイズ統計](../statistics/bayesian/bayesian_statistics.md) |

## 読み方

- 左から「機能」「狙い」「統計知識」「参照先」の順です。
- 同じ機能でも、MVP 段階では簡易版、将来は高度版へ発展させる想定です。

## 補足

- 疲労スコアや行動モード推定は未確定要素が大きいため、最初から断定的な指標として固定しない方針が望ましいです。

## 関連参照

- [analytics_design.md](./analytics_design.md)
- [development_phases.md](./development_phases.md)
- [../statistics/appendix/glossary.md](../statistics/appendix/glossary.md)
