# ベイズ統計

## 概要

ベイズ統計は、事前知識と観測データを統合して不確実性を更新する枠組みです。Body Data Lab では、個人ごとの通常状態を逐次学習する用途と相性があります。

## 主要概念

- 事前分布、尤度、事後分布
- 逐次更新
- 事後予測分布
- 階層ベイズ
- MCMC や近似推論

## 重要な数式

- 事後分布: `p(\theta|x) \propto p(x|\theta) p(\theta)`
- 事後予測: `p(\tilde{x}|x) = \int p(\tilde{x}|\theta) p(\theta|x) d\theta`

## 前提知識

- [確率](../foundations/probability.md)
- [推定](../inference/estimation.md)
- [漸近理論](../inference/asymptotic_theory.md)

## Body Data Lab での利用例

- 観測日数が少ない初期ユーザーでも、事前情報を使って安定した推定を行う
- 心拍や睡眠の通常範囲を逐次更新する
- 行動モードや疲労状態の推定に不確実性を明示する

## 関連ファイル

- [マルコフ連鎖](../stochastic/markov_chain.md)
- [一般化線形モデル](../regression/generalized_linear_models.md)
- [因子分析](../multivariate/factor_analysis.md)
- [設計: analytics_design](../../design/analytics_design.md)

## 未理解でも先に進めるポイント

- まずは「推定値を 1 点ではなく分布で持つ」という感覚が重要です。
- 初期段階では厳密な MCMC 実装を考えず、ベイズ的な考え方を設計に反映するだけでも十分です。

## 今後深掘りすべき論点

- 事前分布の置き方
- オンデバイス推論とサーバー推論の分担
- UI 上で不確実性をどう伝えるか
