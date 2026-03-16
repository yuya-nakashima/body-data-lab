# スペクトル解析

## 概要

スペクトル解析は、時系列を周波数成分の観点から見る方法です。統計検定 1 級では理論面が重要で、Body Data Lab では周期性の探索に中長期的に役立つ可能性があります。

## 主要概念

- 周期性
- 周波数領域
- スペクトル密度
- 周期図
- フィルタリング

## 重要な数式

- スペクトル密度は自己共分散列の Fourier 変換として定義される
- 形式的には `f(\omega) = (1/2\pi) \sum_{k=-\infty}^{\infty} \gamma_k e^{-i k \omega}`

## 前提知識

- [定常過程](./stationary_process.md)
- [ARMA/ARIMA](./arma_arima.md)
- 複素数や Fourier 変換の基礎直感

## Body Data Lab での利用例

- 週周期や特定の生活リズムが強く現れるかを見る
- 心拍や活動量の周期パターンを探索的に確認する

## 関連ファイル

- [時系列の基礎](./time_series_basics.md)
- [定常過程](./stationary_process.md)
- [確率過程](../stochastic/stochastic_processes.md)
- [設計: analytics_design](../../design/analytics_design.md)

## 未理解でも先に進めるポイント

- 現段階では「周期性を見る高度な方法」くらいの理解でも十分です。
- MVP や中級分析では優先度は低く、必要性が出たときに掘る方針でよいです。

## 今後深掘りすべき論点

- サンプル数が少ない個人時系列での実用性
- 不規則欠測がある場合の周期解析
- スペクトル情報を UI にどう翻訳するか
