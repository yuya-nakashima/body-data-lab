# ARMA / ARIMA

## 概要

ARMA / ARIMA は、自己相関を持つ時系列を表現する代表的モデルです。Body Data Lab では、日次データの短期予測や異常検知の基礎モデルとして検討できます。

## 主要概念

- AR モデル
- MA モデル
- ARMA モデル
- 差分と ARIMA
- 予測誤差

## 重要な数式

- AR(p): `X_t = \phi_1 X_{t-1} + \cdots + \phi_p X_{t-p} + \varepsilon_t`
- MA(q): `X_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}`
- ARIMA(p,d,q): 差分系列 `\nabla^d X_t` に ARMA を当てる

## 前提知識

- [時系列の基礎](./time_series_basics.md)
- [定常過程](./stationary_process.md)
- [漸近理論](../inference/asymptotic_theory.md)

## Body Data Lab での利用例

- 歩数や睡眠の翌日予測を試す
- 予測区間から外れた日を異常候補として扱う
- 介入後のトレンド変化を残差ベースで確認する

## 関連ファイル

- [スペクトル解析](./spectral_analysis.md)
- [確率過程](../stochastic/stochastic_processes.md)
- [ベイズ統計](../bayesian/bayesian_statistics.md)
- [設計: development_phases](../../design/development_phases.md)

## 未理解でも先に進めるポイント

- ACF と PACF の厳密理解がなくても、自己相関を見る文化を作る価値はあります。
- MVP では ARIMA を入れず、移動平均から始めるほうが妥当です。

## 今後深掘りすべき論点

- 季節 ARIMA の必要性
- 外生変数付き時系列回帰への発展
- モデル更新頻度と計算コスト
