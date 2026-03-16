# Requirements

## 機能要件

- データ取得
  - Android / Health Connect 等から歩数、心拍、睡眠を取得する
  - 手動で行動モード、稽古日、メモを入力できる
- データ保存
  - 生データ、正規化データ、日次集計を分けて保持する
  - 将来の分析再計算ができるよう履歴を残す
- 分析
  - 基礎: 平均、中央値、標準偏差、移動平均、単純比較
  - 中級: 相関、回帰、群比較、簡易外れ値確認
  - 上級: PCA、クラスタ、時系列モデル、ベイズ、状態遷移
- 表示
  - 日次・週次・月次ダッシュボード
  - グラフ、要約値、分析コメントの表示
  - 欠測やデータ品質の明示

## 非機能要件の概要

- Android 中心で使いやすいこと
- 機能追加時に分析ロジックを差し替えやすいこと
- データ正確性と再現性を保てること
- 個人データを安全に扱えること

## 分析機能のレベル分け

| レベル | 内容 | 主な統計知識 |
| --- | --- | --- |
| 基礎 | 要約統計、推移表示、単純比較 | [記述統計](../statistics/foundations/descriptive_statistics.md), [時系列の基礎](../statistics/time_series/time_series_basics.md) |
| 中級 | 相関、単回帰、重回帰、ANOVA | [単回帰](../statistics/regression/simple_regression.md), [重回帰](../statistics/regression/multiple_regression.md), [分散分析](../statistics/experimental_design/analysis_of_variance.md) |
| 上級 | PCA、因子、クラスタ、ARIMA、ベイズ、マルコフ | [主成分分析](../statistics/multivariate/principal_component_analysis.md), [ARMA / ARIMA](../statistics/time_series/arma_arima.md), [ベイズ統計](../statistics/bayesian/bayesian_statistics.md), [マルコフ連鎖](../statistics/stochastic/markov_chain.md) |

## 補足要件

- 分析結果は断定的に表示しすぎず、不確実性や前提条件を添える
- 未確定な分析モデルは試験導入扱いにする

## 関連参照

- [architecture.md](./architecture.md)
- [analytics_design.md](./analytics_design.md)
- [non_functional_requirements.md](./non_functional_requirements.md)
