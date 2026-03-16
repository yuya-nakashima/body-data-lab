# 分散分析

## 概要

分散分析(ANOVA)は、複数群の平均差を分散分解で評価する手法です。Body Data Lab では、行動モード別、曜日別、稽古有無別の比較に使えます。

## 主要概念

- 群間変動と群内変動
- F 検定
- 一元配置、二元配置
- 交互作用
- 多重比較

## 重要な数式

- `F = MS_{\text{between}} / MS_{\text{within}}`
- `SS_{\text{total}} = SS_{\text{between}} + SS_{\text{within}}`

## 前提知識

- [仮説検定](../inference/hypothesis_testing.md)
- [重回帰](../regression/multiple_regression.md)
- [実験計画](./design_of_experiments.md)

## Body Data Lab での利用例

- 行動モード別の平均歩数差を確認する
- 稽古有無と曜日の交互作用が睡眠にあるかを見る
- 主観疲労スコアを複数条件で比較する

## 関連ファイル

- [実験計画](./design_of_experiments.md)
- [重回帰](../regression/multiple_regression.md)
- [設計: analytics_design](../../design/analytics_design.md)
- [設計: feature_mapping](../../design/feature_mapping.md)

## 未理解でも先に進めるポイント

- まずは 2 群比較から始め、群数が増えた段階で ANOVA を導入してもよいです。
- 分散分析は回帰モデルで書き換えられるため、回帰を理解していれば入りやすいです。

## 今後深掘りすべき論点

- 繰り返し測定 ANOVA の必要性
- 分散不均一や非正規性への対応
- 事後比較の設計
