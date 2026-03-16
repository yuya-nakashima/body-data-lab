# マルコフ連鎖

## 概要

マルコフ連鎖は、「次の状態が現在の状態にのみ依存する」とみなす離散時間モデルです。Body Data Lab では、行動モードや疲労状態の遷移を整理する有力候補です。

## 主要概念

- マルコフ性
- 遷移確率行列
- 定常分布
- 既約性と周期性
- 長期挙動

## 重要な数式

- マルコフ性: `P(X_{t+1}=j | X_t=i, X_{t-1}, \ldots) = P(X_{t+1}=j | X_t=i)`
- 遷移行列: `P = (p_{ij})`
- 定常分布: `\pi = \pi P`

## 前提知識

- [確率](../foundations/probability.md)
- [確率過程](./stochastic_processes.md)
- [ベイズ統計](../bayesian/bayesian_statistics.md)

## Body Data Lab での利用例

- 行動モードが「稽古」「通常」「休養」のどこに遷移しやすいかを見る
- 疲労状態の遷移確率を推定して、翌日の状態予測に使う
- クラスタ分析で得た日タイプの遷移構造を確認する

## 関連ファイル

- [確率過程](./stochastic_processes.md)
- [クラスタ分析](../multivariate/cluster_analysis.md)
- [ベイズ統計](../bayesian/bayesian_statistics.md)
- [設計: feature_mapping](../../design/feature_mapping.md)

## 未理解でも先に進めるポイント

- 状態定義が粗くても、遷移を表で見るだけで有用な気づきが得られます。
- まずは単純な遷移頻度表から始め、厳密な連鎖理論は後でよいです。

## 今後深掘りすべき論点

- 潜在状態を用いる隠れマルコフモデルへの発展
- 時変遷移確率の扱い
- 行動介入による遷移変化の評価
