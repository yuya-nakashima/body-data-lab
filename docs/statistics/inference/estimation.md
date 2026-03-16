# 推定

## 概要

推定は、観測データから未知母数を推し量る枠組みです。Body Data Lab では、平均歩数、睡眠不足日の割合、回帰係数、状態推定などを「どれくらい確からしいか」とともに扱うための基礎になります。

## 主要概念

- 点推定と区間推定
- 不偏性、一致性、有効性
- 最尤推定
- モーメント法
- 信頼区間

## 重要な数式

- 尤度: `L(\theta) = \prod_{i=1}^{n} f(x_i; \theta)`
- 対数尤度: `\ell(\theta) = \sum_{i=1}^{n} \log f(x_i; \theta)`
- Wald 型区間推定: `\hat{\theta} \pm z_{\alpha/2} \cdot SE(\hat{\theta})`
- 標本平均の標準誤差: `SE(\bar{x}) = s / \sqrt{n}`

## 前提知識

- [確率](../foundations/probability.md)
- [分布](../foundations/distribution.md)
- [漸近理論](./asymptotic_theory.md)

## Body Data Lab での利用例

- 直近 30 日の平均歩数に信頼区間を添える
- 睡眠時間と疲労メモの関係に対する回帰係数を推定する
- 個人の通常時心拍の範囲を推定し、逸脱検知の基準にする

## 関連ファイル

- [仮説検定](./hypothesis_testing.md)
- [漸近理論](./asymptotic_theory.md)
- [単回帰](../regression/simple_regression.md)
- [ベイズ統計](../bayesian/bayesian_statistics.md)

## 未理解でも先に進めるポイント

- MVP では区間推定を省き、点推定だけでも機能は成立します。
- 最尤推定の一般論が曖昧でも、平均や割合の推定は先に実装・活用できます。

## 今後深掘りすべき論点

- 小標本での信頼区間の安定性
- 欠測や外れ値を含む推定量のロバスト性
- 個人内時系列データに対する独立標本前提の限界
