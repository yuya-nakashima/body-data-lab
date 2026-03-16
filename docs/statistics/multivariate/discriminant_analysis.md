# 判別分析

## 概要

判別分析は、既知の群情報を使って観測を分類する手法です。Body Data Lab では、「疲労高い日」「通常日」などのラベルがある場合に、どの変数が分類に効くかを整理する用途があります。

## 主要概念

- 線形判別
- 群平均ベクトル
- 群内分散と群間分散
- 判別境界
- 誤分類率

## 重要な数式

- 線形判別得点: `\delta_k(x) = x^\top \Sigma^{-1}\mu_k - (1/2)\mu_k^\top \Sigma^{-1}\mu_k + \log \pi_k`
- Fisher の基準: 群間分散を大きく、群内分散を小さくする方向を選ぶ

## 前提知識

- [多変量解析](./multivariate_analysis.md)
- [分布](../foundations/distribution.md)
- [ベイズ統計](../bayesian/bayesian_statistics.md)

## Body Data Lab での利用例

- 自己申告でラベルづけした疲労状態を、睡眠・心拍・活動量から判別する
- 行動モード推定の単純な教師ありベースラインを作る

## 関連ファイル

- [クラスタ分析](./cluster_analysis.md)
- [一般化線形モデル](../regression/generalized_linear_models.md)
- [マルコフ連鎖](../stochastic/markov_chain.md)
- [設計: analytics_design](../../design/analytics_design.md)

## 未理解でも先に進めるポイント

- まずは分類問題の基礎として理解し、実運用ではロジスティック回帰との比較対象として扱うとよいです。
- 判別分析が前提とする分布仮定は、初期段階では厳密に満たされない可能性があります。

## 今後深掘りすべき論点

- 不均衡データへの対応
- 個人別モデルと汎用モデルの切り分け
- 誤分類コストの設計
