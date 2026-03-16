# 重回帰

## 概要

重回帰は、複数の説明変数から目的変数を説明するモデルです。Body Data Lab では、睡眠、歩数、心拍、稽古有無、行動モードを同時に入れて疲労やコンディションの変動を説明する土台になります。

## 主要概念

- 偏回帰係数
- ダミー変数
- 交互作用
- 共線性
- モデル選択

## 重要な数式

- モデル: `Y = X \beta + \varepsilon`
- 最小二乗解: `\hat{\beta} = (X^\top X)^{-1} X^\top y`
- 残差分散推定: `\hat{\sigma}^2 = RSS / (n-p)`
- VIF の基本形: `VIF_j = 1 / (1 - R_j^2)`

## 前提知識

- [線形代数の基礎](../foundations/linear_algebra_basics.md)
- [単回帰](./simple_regression.md)
- [推定](../inference/estimation.md)

## Body Data Lab での利用例

- 疲労スコアを、睡眠、歩数、安静時心拍、稽古有無で説明する
- 稽古日ダミーと睡眠時間の交互作用を入れて、稽古日の睡眠重要度が高いかを見る
- 行動モード別の差をダミー変数で表す

## 関連ファイル

- [一般化線形モデル](./generalized_linear_models.md)
- [分散分析](../experimental_design/analysis_of_variance.md)
- [主成分分析](../multivariate/principal_component_analysis.md)
- [設計: feature_mapping](../../design/feature_mapping.md)

## 未理解でも先に進めるポイント

- まずは説明変数を少数に絞れば、MVP 後の中級分析として十分実用的です。
- 共線性診断は後回しでもよいですが、似た指標を同時投入しすぎない注意は必要です。

## 今後深掘りすべき論点

- 欠測補完と回帰推定の関係
- 正則化回帰の導入可否
- 個人データに対する解釈と過学習の境界
