# Analytics Design

## 目的

分析機能を「基礎」「中級」「上級」に分け、実装段階と統計学習段階を同期させます。ここでは、何を分析し、その背後にどの統計知識があるかを対応づけます。

## MVP でやる分析

| 分析 | 目的 | 主な出力 | 参照統計 |
| --- | --- | --- | --- |
| 要約統計 | データの全体像把握 | 平均、中央値、標準偏差 | [記述統計](../statistics/foundations/descriptive_statistics.md) |
| 推移分析 | 時間変化把握 | 折れ線、7 日移動平均 | [時系列の基礎](../statistics/time_series/time_series_basics.md) |
| 単純比較 | 稽古日 / 非稽古日比較 | 平均差、箱ひげ図候補 | [仮説検定](../statistics/inference/hypothesis_testing.md), [分散分析](../statistics/experimental_design/analysis_of_variance.md) |
| 品質確認 | 欠測・重複・遅延把握 | カバレッジ、ギャップ、遅延統計 | [記述統計](../statistics/foundations/descriptive_statistics.md) |

## 将来やる分析

| レベル | 分析 | 目的 | 参照統計 |
| --- | --- | --- | --- |
| 中級 | 相関分析 | 指標間の関係探索 | [記述統計](../statistics/foundations/descriptive_statistics.md), [単回帰](../statistics/regression/simple_regression.md) |
| 中級 | 重回帰 | 疲労やコンディションの説明 | [重回帰](../statistics/regression/multiple_regression.md) |
| 中級 | GLM | カウントや二値状態のモデル化 | [一般化線形モデル](../statistics/regression/generalized_linear_models.md) |
| 上級 | PCA | 合成コンディション軸作成 | [主成分分析](../statistics/multivariate/principal_component_analysis.md) |
| 上級 | 因子分析 | 潜在状態の仮説整理 | [因子分析](../statistics/multivariate/factor_analysis.md) |
| 上級 | クラスタ分析 | 行動パターン抽出 | [クラスタ分析](../statistics/multivariate/cluster_analysis.md) |
| 上級 | ARIMA 系 | 短期予測と異常検知 | [ARMA / ARIMA](../statistics/time_series/arma_arima.md) |
| 上級 | ベイズ推定 | 個人適応型推定 | [ベイズ統計](../statistics/bayesian/bayesian_statistics.md) |
| 上級 | 状態遷移分析 | 行動モード変化把握 | [マルコフ連鎖](../statistics/stochastic/markov_chain.md) |

## 分析レベルごとの位置づけ

### 基礎

- まずは「見える化」と「欠測の把握」
- 指標そのものより、継続的に記録できる導線が重要

### 中級

- 相関や回帰で仮説検証の入口を作る
- ただし因果解釈は控えめにする

### 上級

- 合成指標、状態推定、予測、潜在構造に進む
- モデル前提と不確実性の明示が重要

## 実装上の設計メモ

- 基礎分析はローカル実行でも成立しやすい
- 中級以上は計算量と再現性の観点から分析ジョブ化を検討したい
- 分析結果は説明文より先に、前提条件と対象期間を明示したい

## 未確定事項

- 疲労スコアを手動入力ベースで作るか、複数指標から推定するか
- 上級分析をオンデバイスで行うか、API 経由で行うか
- 群比較や回帰を UI でどこまで一般ユーザー向けに公開するか

## 関連参照

- [feature_mapping.md](./feature_mapping.md)
- [development_phases.md](./development_phases.md)
- [../statistics/appendix/study_roadmap.md](../statistics/appendix/study_roadmap.md)
