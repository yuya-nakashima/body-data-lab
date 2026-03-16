# 単回帰

## 概要

単回帰は、1 つの説明変数と 1 つの目的変数の関係を定量化する基本手法です。Body Data Lab では、睡眠時間と疲労感、歩数と体調メモの関係を見る最初の分析として使いやすいです。

## 主要概念

- 回帰直線
- 傾きと切片
- 残差
- 決定係数 `R^2`
- 相関と回帰の違い

## 重要な数式

- モデル: `Y_i = \beta_0 + \beta_1 X_i + \varepsilon_i`
- 最小二乗推定量: `\hat{\beta}_1 = \sum (x_i-\bar{x})(y_i-\bar{y}) / \sum (x_i-\bar{x})^2`
- 予測値: `\hat{Y}_i = \hat{\beta}_0 + \hat{\beta}_1 X_i`

## 前提知識

- [記述統計](../foundations/descriptive_statistics.md)
- [推定](../inference/estimation.md)
- [仮説検定](../inference/hypothesis_testing.md)

## Body Data Lab での利用例

- 睡眠時間が 1 時間増えると疲労メモがどれだけ変わるかを見る
- 歩数と安静時心拍の単純な関係を探索する
- まず散布図と回帰線で関係を掴み、その後に多変量化する

## 関連ファイル

- [重回帰](./multiple_regression.md)
- [一般化線形モデル](./generalized_linear_models.md)
- [時系列の基礎](../time_series/time_series_basics.md)
- [設計: analytics_design](../../design/analytics_design.md)

## 未理解でも先に進めるポイント

- 残差診断まで完全に理解していなくても、関係の概形を見る用途では有効です。
- 因果関係ではなく関連の要約である点を守れば、初期分析として十分使えます。

## 今後深掘りすべき論点

- 外れ値に弱い点への対策
- 誤差独立性が崩れる時系列データへの適用限界
- 非線形関係をどう検出するか
