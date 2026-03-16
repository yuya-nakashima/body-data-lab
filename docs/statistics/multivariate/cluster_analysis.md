# クラスタ分析

## 概要

クラスタ分析は、ラベルのないデータを似たもの同士でまとめる手法です。Body Data Lab では、生活パターンや行動モードを探索的に見つける用途が考えられます。

## 主要概念

- 類似度と距離
- k-means
- 階層クラスタリング
- クラスタ数の選択
- 探索的分析としての位置づけ

## 重要な数式

- k-means の目的関数: `\sum_{k=1}^{K} \sum_{i \in C_k} ||x_i - \mu_k||^2`
- ユークリッド距離: `||x-y|| = \sqrt{\sum_j (x_j-y_j)^2}`

## 前提知識

- [記述統計](../foundations/descriptive_statistics.md)
- [線形代数の基礎](../foundations/linear_algebra_basics.md)
- [多変量解析](./multivariate_analysis.md)

## Body Data Lab での利用例

- 日単位データから「高活動日」「回復日」「低調日」のようなパターン候補を探す
- 行動モード入力がない期間に、特徴量から暫定的なクラスタを付与する

## 関連ファイル

- [判別分析](./discriminant_analysis.md)
- [主成分分析](./principal_component_analysis.md)
- [マルコフ連鎖](../stochastic/markov_chain.md)
- [設計: feature_mapping](../../design/feature_mapping.md)

## 未理解でも先に進めるポイント

- クラスタは真理ではなく、見方の 1 つだと理解しておけば先に進めます。
- まずは PCA で 2 次元に落としてからクラスタを見る方法が分かりやすいです。

## 今後深掘りすべき論点

- クラスタ数の妥当性評価
- 時系列依存を無視したクラスタリングの限界
- クラスタ結果を UI にどう説明するか
