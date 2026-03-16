# 一般化線形モデル

## 概要

一般化線形モデル(GLM)は、正規分布以外の目的変数を扱うための拡張です。歩数のようなカウント、二値状態、割合データに対して自然なモデリングを提供します。

## 主要概念

- 指数型分布族
- リンク関数
- 線形予測子
- ロジスティック回帰
- ポアソン回帰

## 重要な数式

- 基本形: `g(E[Y|X]) = X \beta`
- ロジスティック回帰: `\log(p/(1-p)) = X \beta`
- ポアソン回帰: `\log(\lambda) = X \beta`
- 尤度に基づく推定と逸脱度

## 前提知識

- [分布](../foundations/distribution.md)
- [推定](../inference/estimation.md)
- [漸近理論](../inference/asymptotic_theory.md)

## Body Data Lab での利用例

- 歩数の期待値を、曜日や稽古有無で説明する
- 「疲労高い/低い」の二値化ラベルに対してロジスティック回帰を使う
- 睡眠不足日の発生確率を説明変数付きで推定する

## 関連ファイル

- [重回帰](./multiple_regression.md)
- [ベイズ統計](../bayesian/bayesian_statistics.md)
- [時系列の基礎](../time_series/time_series_basics.md)
- [設計: analytics_design](../../design/analytics_design.md)

## 未理解でも先に進めるポイント

- 最初は「目的変数の型に応じて回帰を変える」という理解で十分です。
- パラメータ推定の計算詳細はライブラリに任せても、リンク関数の意味は押さえたいです。

## 今後深掘りすべき論点

- 過分散への対処
- ゼロ過剰モデルの必要性
- 個人内時系列依存を GLM だけで扱う限界
