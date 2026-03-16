# 線形代数の基礎

## 概要

線形代数は、回帰、多変量解析、時系列、状態空間モデルを支える基礎です。Body Data Lab では、複数の身体指標をまとめて扱う局面で不可欠になります。

## 主要概念

- ベクトルと行列
- 内積、ノルム、直交
- 行列の積、逆行列、転置
- 固有値、固有ベクトル
- ランクと線形独立

## 重要な数式

- 回帰の正規方程式: `\hat{\beta} = (X^\top X)^{-1} X^\top y`
- 共分散行列: `\Sigma = E[(X - \mu)(X - \mu)^\top]`
- 固有値問題: `A v = \lambda v`
- 二次形式: `x^\top A x`

## 前提知識

- 一次関数と連立方程式の基本
- [分布](./distribution.md) の多変量的な見方
- [重回帰](../regression/multiple_regression.md) と [主成分分析](../multivariate/principal_component_analysis.md) の土台

## Body Data Lab での利用例

- 睡眠、歩数、心拍、主観メモを 1 つの行列として扱う
- 主成分分析でコンディション指標を作る
- 共線性が強い説明変数群を整理する

## 関連ファイル

- [重回帰](../regression/multiple_regression.md)
- [主成分分析](../multivariate/principal_component_analysis.md)
- [因子分析](../multivariate/factor_analysis.md)
- [判別分析](../multivariate/discriminant_analysis.md)

## 未理解でも先に進めるポイント

- 行列積と転置の意味だけ掴めば、回帰や PCA の式を読む足場になります。
- 固有値分解の厳密証明は後回しで問題ありません。

## 今後深掘りすべき論点

- 数値安定性と計算量
- 特異行列や擬似逆行列の扱い
- 共分散行列の固有構造と可視化の結び付き
