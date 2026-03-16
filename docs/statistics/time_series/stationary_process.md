# 定常過程

## 概要

定常過程は、時間がずれても確率構造が大きく変わらない過程です。ARMA 系やスペクトル解析を理解する前提であり、Body Data Lab の長期データをどうモデル化するか考える基盤になります。

## 主要概念

- 強定常と弱定常
- 平均一定、分散一定
- 自己共分散がラグのみに依存
- ホワイトノイズ
- 非定常性

## 重要な数式

- 弱定常条件: `E[X_t]=\mu`, `Var(X_t)=\sigma^2`, `Cov(X_t,X_{t-k})=\gamma_k`
- ホワイトノイズ: `E[\varepsilon_t]=0`, `Var(\varepsilon_t)=\sigma^2`, `Cov(\varepsilon_t,\varepsilon_{t-k})=0`

## 前提知識

- [時系列の基礎](./time_series_basics.md)
- [確率過程](../stochastic/stochastic_processes.md)
- [確率](../foundations/probability.md)

## Body Data Lab での利用例

- 歩数の長期トレンドを除いた残差系列に AR モデルを当てる前提確認
- 心拍の周期性を除去した後の揺らぎを分析する

## 関連ファイル

- [ARMA/ARIMA](./arma_arima.md)
- [スペクトル解析](./spectral_analysis.md)
- [確率過程](../stochastic/stochastic_processes.md)
- [設計: risks_and_unknowns](../../design/risks_and_unknowns.md)

## 未理解でも先に進めるポイント

- 初期段階では、系列にトレンドがあるかないかを図で見るだけでも有効です。
- 定常性検定の詳細は後回しでも、非定常なら単純平均比較が危うい点は押さえたいです。

## 今後深掘りすべき論点

- 季節差分や変換でどこまで定常化できるか
- 構造変化点があるときの扱い
- 定常性前提を満たさない個人データの実務対応
