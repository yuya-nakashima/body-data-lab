# Body Data Lab 設計書

## このフォルダの目的

`docs/design/` は、Body Data Lab をどのようなプロダクトとして育てるかを整理するための設計書群です。MVP を小さく始めつつ、統計分析を段階的に高度化できる構成を目指します。

## 読み始める順番

1. [vision.md](./vision.md)
2. [product_scope.md](./product_scope.md)
3. [requirements.md](./requirements.md)
4. [architecture.md](./architecture.md)
5. [data_model.md](./data_model.md)
6. [analytics_design.md](./analytics_design.md)

## 読み方

- 「何を作るか」を把握したい場合は `vision.md` と `product_scope.md`
- 「何が必要か」を把握したい場合は `requirements.md`
- 「どう分けて設計するか」を把握したい場合は `architecture.md` と `data_model.md`
- 「統計とどう接続するか」を把握したい場合は `analytics_design.md` と `feature_mapping.md`

## 統計知識との関係

- 分析要件や分析結果の解釈は [../statistics/README.md](../statistics/README.md) と対応させています。
- 特に [analytics_design.md](./analytics_design.md) は、各分析レベルから統計知識ファイルへリンクします。

## 補足

現状のリポジトリには FastAPI と SQLite を用いたデータ取り込み・正規化・集計の流れが見えますが、この設計書では Android 中心のプロダクト全体像を主に整理しています。サーバーを常設するか、ローカル中心で進めるかは未確定です。
