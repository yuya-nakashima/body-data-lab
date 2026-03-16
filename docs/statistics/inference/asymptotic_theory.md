# 漸近理論

## 概要

漸近理論は、標本サイズが大きくなるときの推定量や検定統計量の振る舞いを扱います。統計検定 1 級では重要度が高く、Body Data Lab では大規模な日次蓄積データや逐次更新モデルの理解に役立ちます。

## 主要概念

- 大数の法則
- 中心極限定理
- 漸近正規性
- 一致性
- Delta method

## 重要な数式

- 中心極限定理: `\sqrt{n}(\bar{X} - \mu) \Rightarrow N(0, \sigma^2)`
- 漸近正規性: `\sqrt{n}(\hat{\theta} - \theta_0) \Rightarrow N(0, I(\theta_0)^{-1})`
- Delta method: `\sqrt{n}(g(\hat{\theta}) - g(\theta)) \Rightarrow N(0, [g'(\theta)]^2 V)`

## 前提知識

- [確率](../foundations/probability.md)
- [推定](./estimation.md)
- 微分の基本

## Body Data Lab での利用例

- 十分な観測日数があるとき、平均や回帰係数の近似分布を使って区間推定する
- 比率や対数変換後の指標の標準誤差を Delta method で近似する
- 大量データでブートストラップと漸近近似のどちらを採用するか判断する

## 関連ファイル

- [推定](./estimation.md)
- [仮説検定](./hypothesis_testing.md)
- [一般化線形モデル](../regression/generalized_linear_models.md)
- [ベイズ統計](../bayesian/bayesian_statistics.md)

## 未理解でも先に進めるポイント

- 初期実装では漸近理論を明示せずとも、既存ライブラリの出力を使うことは可能です。
- ただし、標本数が少ないのに大標本近似を使っていないかは意識しておく必要があります。

## 今後深掘りすべき論点

- 時系列依存があるときの漸近理論
- M 推定やサンドイッチ分散の導入
- 実データでの有限標本誤差評価
