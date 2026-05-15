# 振り返り入力画面 設計書

## 概要

「無意識との対話」コンセプトに基づく日次振り返り入力画面。
FastAPI が HTML を返し、Android の WebView で表示する。

---

## 現状の構成（参考）

```
Android DashboardActivity (WebView)
    → GET /ui/steps
    → FastAPI が HTML を返す
    → JavaScript で /metrics/daily を fetch して描画
```

振り返り画面も同じパターンで実装する。

---

## 追加する構成

```
Android MainActivity
    → 「振り返りを書く」ボタン
    → ReflectionActivity (WebView)
        → GET /ui/reflections
        → FastAPI が HTML フォームを返す
        → 入力 → POST /reflections or PATCH /reflections/{id}
        → 今日の記録があれば編集モードで表示
```

---

## 画面仕様（Web UI）

### `GET /ui/reflections`

| 状態 | 表示内容 |
|---|---|
| 今日の記録なし | 空フォーム（新規入力モード） |
| 今日の記録あり | 既存内容を表示（編集モード） |

### フォーム構成

```
┌────────────────────────────────────┐
│  今日の振り返り  YYYY-MM-DD        │
├────────────────────────────────────┤
│  今、本当にやりたいことは何ですか？ │
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  └──────────────────────────────┘  │
│  今、不安に感じていることはありますか？ │
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  └──────────────────────────────┘  │
│  無意識が求めていると感じることは？  │
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  └──────────────────────────────┘  │
│  自由に書いてください。              │
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  └──────────────────────────────┘  │
│             [ 保存する ]           │
└────────────────────────────────────┘
```

### 動作仕様

- ページ読み込み時に `GET /reflections/today` を fetch
  - 記録なし → 新規入力モード（POST /reflections）
  - 記録あり → 編集モード（PATCH /reflections/{id}）
- 全フィールド任意入力（全空の場合は保存しない）
- 保存成功時はフィードバックメッセージを表示
- `recorded_at` はクライアント側で現在時刻（JST）を付与

### UI 方針

- `/ui/steps` と同じデザインシステム（フォント・カラー・カード）
- モバイル最適化（padding・font-size）
- シンプルで邪魔のないデザイン（「無意識との対話」コンセプト）

---

## Android 側の変更

### 追加ファイル

| ファイル | 内容 |
|---|---|
| `app/src/main/java/.../ReflectionActivity.kt` | WebView で `/ui/reflections` を表示 |
| `app/src/main/res/layout/activity_reflection.xml` | フルスクリーン WebView レイアウト |

### 変更ファイル

| ファイル | 変更内容 |
|---|---|
| `app/src/main/java/.../MainActivity.kt` | 「振り返りを書く」ボタン追加 |
| `app/src/main/res/layout/activity_main.xml` | ボタン追加 |
| `app/src/main/AndroidManifest.xml` | ReflectionActivity 登録 |

### ReflectionActivity の仕様

`DashboardActivity` と同じ構成：
- フルスクリーン WebView
- JavaScript 有効
- 戻るボタンで WebView 履歴を戻る
- 読み込み失敗時はエラーページ表示

---

## データフロー

```
1. ユーザーが「振り返りを書く」をタップ
2. ReflectionActivity 起動
3. WebView が GET /ui/reflections をリクエスト
4. FastAPI が HTML を返す
5. HTML 内 JS が GET /reflections/today を fetch
6. 記録なし → 空フォーム表示
   記録あり → 既存内容を表示（編集可能）
7. ユーザーが入力して「保存する」をタップ
8. JS が POST /reflections または PATCH /reflections/{id} を呼ぶ
9. 成功メッセージを表示
```

---

## 実装ファイル一覧

### FastAPI（body-data-lab）

| ファイル | 変更内容 |
|---|---|
| `app/routers/ui.py` | `GET /ui/reflections` エンドポイント追加 |

### Android（ninja-habits-android）

| ファイル | 変更内容 |
|---|---|
| `app/src/main/java/com/example/myhealthhub/ReflectionActivity.kt` | 新規作成 |
| `app/src/main/res/layout/activity_reflection.xml` | 新規作成 |
| `app/src/main/java/com/example/myhealthhub/MainActivity.kt` | ボタン追加 |
| `app/src/main/res/layout/activity_main.xml` | ボタン追加 |
| `app/src/main/AndroidManifest.xml` | Activity 登録 |

---

## 関連ドキュメント

- `docs/design/screen_design.md` — 画面一覧
- `docs/android-app.md` — Android 仕様・API 仕様
- `body-data-guide/articles/unconscious-conversation.md` — コンセプト
