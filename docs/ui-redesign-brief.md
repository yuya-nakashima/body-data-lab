# UI リデザイン指示書 — 今日の目標 セクション

## 対象

`app/templates/reflections.html` 内の「今日の目標」セクションのみ。
他のセクション（Habit Stacking・振り返り・Wish List 等）は変更しない。

---

## 現状

```html
<!-- デイリーゴール -->
<div class="sec-header">
  <span class="sec-label">今日の目標</span>
  <a class="nav-link" href="/ui/daily-goals">ゴールを管理 →</a>
</div>
<div id="goalList"></div>

<div class="divider"></div>
```

`goalList` には JS が以下の HTML を動的に挿入する：

**ゴールがある場合:**
```html
<div class="group-card">
  <div class="group-items">
    <!-- ゴール1件ごとに buildGoalItem() が生成 -->
    <div class="habit-item">
      <div class="chk [done]" onclick="toggleGoal(this, {id})">
        <svg>...</svg>  <!-- チェックマーク -->
      </div>
      <span class="habit-label [struck]">{content}</span>
      <!-- done のときのみ表示 -->
      <div class="count-ctrl">
        <button class="count-btn" onclick="adjustGoalCount(this,{id},-1)">−</button>
        <span class="count-num">{count}</span>
        <button class="count-btn" onclick="adjustGoalCount(this,{id},1)">＋</button>
      </div>
    </div>
  </div>
</div>
```

**ゴールがない場合:**
```html
<div class="no-groups-msg">
  <a href="/ui/daily-goals">今日のゴールを追加する →</a>
</div>
```

---

## 現在のデザイントークン（ページ共通）

```css
背景:           #fafaf9
テキスト:       #1a1a18
カード背景:     #fff
ボーダー:       #e8e8e5
区切り線:       #f0f0ee
アクセント:     #7F77DD（パープル）
チェック完了:   #5DCAA5 bg / #1D9E75 border
セクションラベル: #aaa, 10px, uppercase
リンク:         #7F77DD
```

今日の目標 セクションは現状 Habit Stacking セクションと **まったく同じスタイル**（`.group-card` / `.habit-item` / `.chk` 等）を使っており、視覚的に区別できない。

---

## 課題

1. Habit Stacking と見た目が同一で、どちらのセクションか一瞬わからない
2. セクションラベル「今日の目標」が小さく（10px uppercase）、重要度が伝わらない
3. 完了済みゴールの達成感が薄い

---

## リデザイン要件

### 必須

- **JS 関数・API 呼び出し・クラス名は変更しない**
  - `toggleGoal()` / `adjustGoalCount()` / `buildGoalItem()` はそのまま動作すること
  - `.chk` / `.chk.done` / `.habit-item` / `.habit-label.struck` / `.count-ctrl` / `.count-btn` / `.count-num` のクラス名はそのまま保持（JS が依存している）
  - `id="goalList"` も変更しない
- **Habit Stacking セクションと視覚的に差別化する**
  - 色・形状・タイポグラフィのいずれかで区別をつける
- **タッチターゲット最低 44×44px**
- `env(safe-area-inset-*)` 対応は維持（既存の `body` スタイルを変えない）

### 提案歓迎

- セクションラベルをもう少し目立つサイズ・ウェイトにする
- 完了ゴールに達成感を出す演出（バッジ色・背景ハイライト等）
- ゴールがない場合の空状態をより親しみやすいメッセージに
- Habit Stacking とは異なるアクセントカラーの使い方（同じパープル系でも濃淡を変える等）

---

## 出力形式

`reflections.html` の完全な HTML を出力すること（`<!doctype html>` から `</html>` まで）。
変更箇所は `<style>` タグ内の CSS と、必要であれば `sec-header` 周辺の HTML 構造のみ。
JS ブロック（`<script>` タグ内）は一切変更しないこと。
