# 仮説検定

## 概要

仮説検定は、観測された差や傾向が偶然の範囲かどうかを判断する枠組みです。Body Data Lab では、稽古日と非稽古日で平均歩数や睡眠が異なるか、といった比較に使います。

## 主要概念

- 帰無仮説と対立仮説
- 検定統計量、棄却域、p 値
- 第一種過誤と第二種過誤
- t 検定、比率検定、カイ二乗検定
- 多重比較の問題

## 重要な数式

- t 統計量: `t = (\bar{x} - \mu_0) / (s / \sqrt{n})`
- 2 群平均差の検定統計量: `(\bar{x}_1 - \bar{x}_2) / SE`
- p 値: `P(T \ge t_{\mathrm{obs}} | H_0)` のように定義される tail probability

## 前提知識

- [推定](./estimation.md)
- [分布](../foundations/distribution.md)
- [分散分析](../experimental_design/analysis_of_variance.md)

## Body Data Lab での利用例

- 稽古日と非稽古日の平均睡眠時間差の検定
- 新しい就寝ルール導入前後で疲労スコアが変化したかの確認
- 行動モード別に心拍分布が異なるかの探索

## 関連ファイル

- [推定](./estimation.md)
- [分散分析](../experimental_design/analysis_of_variance.md)
- [重回帰](../regression/multiple_regression.md)
- [設計: analytics_design](../../design/analytics_design.md)

## 未理解でも先に進めるポイント

- p 値の厳密な哲学を理解していなくても、比較の手順設計は進められます。
- MVP では「有意差判定」より効果量と可視化を優先してもよいです。

## 今後深掘りすべき論点

- 個人時系列で通常の独立標本検定を使う妥当性
- 多重比較補正をどの段階で導入するか
- 有意差と実用差の切り分け
