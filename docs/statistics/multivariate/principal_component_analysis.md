# 主成分分析

## 概要

主成分分析(PCA)は、多数の変数を少数の合成指標に圧縮する手法です。Body Data Lab では、睡眠、心拍、活動量から「総合コンディション軸」を作る候補になります。

## 主要概念

- 分散最大化
- 直交主成分
- 固有値と寄与率
- スコアと負荷量
- 標準化の必要性

## 重要な数式

- 最適化の考え方: `Var(a^\top X)` を最大化する `a` を探す
- 固有値問題: `\Sigma a = \lambda a`
- 寄与率: `\lambda_k / \sum_j \lambda_j`

## 前提知識

- [線形代数の基礎](../foundations/linear_algebra_basics.md)
- [多変量解析](./multivariate_analysis.md)
- [記述統計](../foundations/descriptive_statistics.md)

## Body Data Lab での利用例

- 複数の身体指標を 1 つか 2 つの見やすい軸に圧縮する
- 疲労スコア候補をデータ駆動で作る
- ダッシュボードの高度分析画面で主成分スコア推移を表示する

## 関連ファイル

- [因子分析](./factor_analysis.md)
- [判別分析](./discriminant_analysis.md)
- [設計: analytics_design](../../design/analytics_design.md)
- [設計: feature_mapping](../../design/feature_mapping.md)

## 未理解でも先に進めるポイント

- 固有値分解の詳細より、「情報をなるべく失わずに次元を減らす」という直感を先に掴めば十分です。
- 主成分の解釈は曖昧になりやすいため、まずは探索的用途に限定してもよいです。

## 今後深掘りすべき論点

- 標準化有無で結果がどう変わるか
- 個人内時系列に PCA をかける妥当性
- 主成分の安定性評価
