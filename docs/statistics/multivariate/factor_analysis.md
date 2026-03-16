# 因子分析

## 概要

因子分析は、観測変数の背後にある少数の潜在因子を仮定する手法です。Body Data Lab では、疲労、回復、ストレスといった直接観測しにくい概念を整理する候補になります。

## 主要概念

- 共通因子と独自因子
- 因子負荷量
- 共通性
- 回転
- 探索的因子分析と確認的因子分析

## 重要な数式

- 基本モデル: `X = \Lambda F + \varepsilon`
- 共分散構造: `\Sigma = \Lambda \Lambda^\top + \Psi`

## 前提知識

- [多変量解析](./multivariate_analysis.md)
- [線形代数の基礎](../foundations/linear_algebra_basics.md)
- [主成分分析](./principal_component_analysis.md)

## Body Data Lab での利用例

- 睡眠、心拍、主観メモから「回復因子」と「負荷因子」を仮定する
- 将来、自己評価アンケート項目を増やしたときに潜在概念を整理する

## 関連ファイル

- [主成分分析](./principal_component_analysis.md)
- [ベイズ統計](../bayesian/bayesian_statistics.md)
- [設計: analytics_design](../../design/analytics_design.md)
- [設計: risks_and_unknowns](../../design/risks_and_unknowns.md)

## 未理解でも先に進めるポイント

- MVP では因子分析を使わなくてもよく、主成分分析のほうが導入しやすいです。
- 潜在因子は解釈が主観的になりやすい点だけ押さえておけば、設計議論は進められます。

## 今後深掘りすべき論点

- 観測項目数が少ない場合の適用限界
- 回転方法の選択
- 潜在変数をアプリ指標として公開する際の説明責任
