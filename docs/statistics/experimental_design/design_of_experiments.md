# 実験計画

## 概要

実験計画は、限られた試行から比較可能なデータを得るための設計です。Body Data Lab では、就寝時間変更や運動習慣変更の効果を自己実験的に確かめるときに重要になります。

## 主要概念

- 要因と水準
- 反復
- 無作為化
- ブロック化
- 交絡

## 重要な数式

- 厳密な式よりも、分散分解と比較可能性の設計が中心
- 基本発想は「処置効果 + 誤差」で表す

## 前提知識

- [仮説検定](../inference/hypothesis_testing.md)
- [分散分析](./analysis_of_variance.md)
- [記述統計](../foundations/descriptive_statistics.md)

## Body Data Lab での利用例

- 就寝前ルーチン A と B を週単位で切り替えて比較する
- 稽古日の食事タイミング変更が翌日の疲労に与える影響を記録する
- 手動メモ項目を揃え、比較可能なデータを取る

## 関連ファイル

- [分散分析](./analysis_of_variance.md)
- [仮説検定](../inference/hypothesis_testing.md)
- [設計: data_collection](../../design/data_collection.md)
- [設計: risks_and_unknowns](../../design/risks_and_unknowns.md)

## 未理解でも先に進めるポイント

- 高度な実験計画法を使わなくても、記録条件を揃えるだけで分析の質は上がります。
- まずは比較したい要因を明文化することが重要です。

## 今後深掘りすべき論点

- n-of-1 試験の取り入れ方
- 自己実験における実行負荷と統計的厳密性のバランス
- 介入遵守の記録方法
