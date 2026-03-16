# 学習ロードマップ

## 概要

このロードマップは、Body Data Lab の開発と並行して統計知識を積み上げるための順序案です。統計検定 1 級を意識しつつ、アプリ実装に役立つ順で整理します。

## 主要概念

- 基礎: データ要約、確率、分布、回帰の入口
- 2 級相当: 推定、検定、単回帰、重回帰、分散分析
- 準 1 級から 1 級相当: 漸近理論、多変量解析、時系列、ベイズ、確率過程

## 重要な数式

- 各段階で最低限押さえたい式は以下です。
- 基礎: `\bar{x}`, `s^2`, `Cov(X,Y)`
- 2 級相当: `t` 統計量、`F` 統計量、`\hat{\beta} = (X^\top X)^{-1}X^\top y`
- 1 級相当: 漸近正規性、GLM、AR モデル、事後分布

## 前提知識

- [記号一覧](./notation.md)
- [用語集](./glossary.md)
- [設計: development_phases](../../design/development_phases.md)

## Body Data Lab での利用例

- フェーズ 1 では記述統計と簡単な時系列可視化に集中する
- フェーズ 2 で回帰や群比較を使って、仮説検証型の分析に進む
- フェーズ 3 で PCA、時系列モデル、ベイズ、マルコフ連鎖を導入する

## 関連ファイル

- [記述統計](../foundations/descriptive_statistics.md)
- [推定](../inference/estimation.md)
- [重回帰](../regression/multiple_regression.md)
- [時系列の基礎](../time_series/time_series_basics.md)

## 未理解でも先に進めるポイント

- すべてを理解してから実装する必要はありません。
- 実データに触れながら必要な章に戻る往復型の学習で十分です。

## 今後深掘りすべき論点

- 推奨順序を実装フェーズにどう同期させるか
- 学習優先度と機能価値のバランス
- 数理厳密性をどこまで追うかの運用ルール

## 学習ステップ案

### フェーズ A: 基礎固め

1. [記述統計](../foundations/descriptive_statistics.md)
2. [確率](../foundations/probability.md)
3. [分布](../foundations/distribution.md)
4. [時系列の基礎](../time_series/time_series_basics.md)

### フェーズ B: 統計検定 2 級相当を意識

1. [推定](../inference/estimation.md)
2. [仮説検定](../inference/hypothesis_testing.md)
3. [単回帰](../regression/simple_regression.md)
4. [重回帰](../regression/multiple_regression.md)
5. [分散分析](../experimental_design/analysis_of_variance.md)

### フェーズ C: 準 1 級から 1 級相当への橋渡し

1. [線形代数の基礎](../foundations/linear_algebra_basics.md)
2. [漸近理論](../inference/asymptotic_theory.md)
3. [一般化線形モデル](../regression/generalized_linear_models.md)
4. [多変量解析](../multivariate/multivariate_analysis.md)
5. [定常過程](../time_series/stationary_process.md)

### フェーズ D: 1 級相当の拡張

1. [主成分分析](../multivariate/principal_component_analysis.md)
2. [因子分析](../multivariate/factor_analysis.md)
3. [ARMA / ARIMA](../time_series/arma_arima.md)
4. [ベイズ統計](../bayesian/bayesian_statistics.md)
5. [マルコフ連鎖](../stochastic/markov_chain.md)
6. [スペクトル解析](../time_series/spectral_analysis.md)
