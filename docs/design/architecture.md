# Architecture

## 基本方針

Android 中心で開始し、必要に応じてサーバー分析へ拡張できるレイヤー分離を採用します。少なくとも次の責務は分離したいです。

1. データ取得
2. 正規化
3. 保存
4. 集計
5. 分析
6. 表示

## 想定構成

### ローカル中心案

- Android アプリが Health Connect 等からデータ取得
- ローカル DB に保存
- 端末上で日次集計と基礎分析
- 必要な画面に即時表示

### ローカル + 軽量 API 案

- Android で取得したデータを API に送信
- サーバー側で生データ保存、正規化、再集計
- 高度分析や再計算をサーバー側へ寄せる

### 現時点のリポジトリとの接続

- 既存コードでは FastAPI と SQLite による `ingest -> normalize -> aggregate -> metrics/ui` の流れが確認できる
- これをそのまま正式アーキテクチャとみなすか、プロトタイプ実装とみなすかは未確定

## レイヤー分離の意図

- データ取得レイヤー: ソース差異を吸収する
- データモデルレイヤー: 生データと分析向けデータを分離する
- 分析レイヤー: 基礎集計と高度分析を段階的に追加できるようにする
- UI レイヤー: 分析ロジックに依存しすぎない表示設計にする

## 将来のサーバー分析やバッチ処理

- 日次再集計バッチ
- 特徴量生成バッチ
- 重い時系列モデルやベイズ推論の非同期実行
- 長期履歴バックアップ

## アーキテクチャ上の未確定事項

- 完全ローカルで始めるか、早い段階で API を置くか
- 分析処理を Android で持つ範囲
- 通知や定期再計算の実行主体

## 関連参照

- [data_collection.md](./data_collection.md)
- [data_model.md](./data_model.md)
- [api_design.md](./api_design.md)
- [../statistics/stochastic/stochastic_processes.md](../statistics/stochastic/stochastic_processes.md)
