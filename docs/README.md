# Body Data Lab Docs

## 概要

この `docs/` は、Body Data Lab を「身体データを扱うアプリ」と「統計学を実データで学ぶ場」の両面から整理するためのドキュメント群です。

- `statistics/`: 統計検定 1 級レベルまでを意識した知識整理
- `design/`: アプリの目的、要件、構成、分析設計の整理

## 読み方

最初は次の順で読む想定です。

1. [design/vision.md](./design/vision.md)
2. [design/product_scope.md](./design/product_scope.md)
3. [design/requirements.md](./design/requirements.md)
4. [design/analytics_design.md](./design/analytics_design.md)
5. [statistics/README.md](./statistics/README.md)
6. [statistics/appendix/study_roadmap.md](./statistics/appendix/study_roadmap.md)

## `statistics/` と `design/` の関係

- `design/` は「何を作るか」「どこまで作るか」「どう拡張するか」を整理します。
- `statistics/` は「分析機能の背景にある知識」を整理します。
- 設計書の分析関連章では、必要に応じて `statistics/` の該当ファイルを相対パスで参照します。

## 実装へ進む際の使い方

- MVP 実装前に `design/requirements.md` と `design/data_model.md` を確認し、最低限のデータ構造を固めます。
- 分析機能を追加する際は `design/analytics_design.md` から対象分析を選び、対応する `statistics/` の知識を参照します。
- 未確定事項は [design/risks_and_unknowns.md](./design/risks_and_unknowns.md) で管理し、実装判断時に再確認します。

## 補足

現時点では、Android 中心の利用と Health Connect 連携を主軸に想定していますが、サーバー常設や高度分析の配置先は未確定です。設計書では、その不確定性を前提に段階的に整理しています。
