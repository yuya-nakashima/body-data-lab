# 時系列の基礎

## 概要

時系列解析は、時間順に並んだデータの依存構造を扱います。Body Data Lab では、日次の歩数、睡眠、心拍の推移を理解する中心的な知識です。

## 主要概念

- トレンド、季節性、周期性
- 自己相関
- ラグ
- 予測と平滑化
- 欠測を含む時系列

## 重要な数式

- 自己相関係数: `\rho_k = Cov(X_t, X_{t-k}) / Var(X_t)`
- 移動平均: `\bar{x}_t^{(m)} = (1/m)\sum_{j=0}^{m-1} x_{t-j}`
- 分解の考え方: `系列 = トレンド + 季節 + 不規則`

## 前提知識

- [記述統計](../foundations/descriptive_statistics.md)
- [確率](../foundations/probability.md)
- [定常過程](./stationary_process.md)

## Body Data Lab での利用例

- 7 日移動平均で歩数のトレンドを見る
- 稽古曜日に応じた週周期を確認する
- 睡眠の崩れが数日後の疲労に波及するかを見る

## 関連ファイル

- [定常過程](./stationary_process.md)
- [ARMA/ARIMA](./arma_arima.md)
- [スペクトル解析](./spectral_analysis.md)
- [設計: analytics_design](../../design/analytics_design.md)

## 未理解でも先に進めるポイント

- MVP では移動平均と折れ線グラフだけでも十分価値があります。
- 自己相関の厳密定義より、「昨日の値が今日にも影響する」感覚を先に掴めば進めます。

## 今後深掘りすべき論点

- 欠測日を含む時系列可視化の扱い
- 介入前後比較と自然変動の切り分け
- 個人データでの予測モデル評価
