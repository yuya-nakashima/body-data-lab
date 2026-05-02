from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/ui", tags=["ui"])


@router.get("/reflections", response_class=HTMLResponse)
def reflections_ui() -> HTMLResponse:
    html = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>振り返り</title>
    <style>
      :root { color-scheme: light; }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        padding: 24px 20px 40px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f6f7fb;
        color: #111827;
      }
      h1 {
        margin: 0 0 4px;
        font-size: 22px;
      }
      .date {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 24px;
      }
      .field {
        margin-bottom: 20px;
      }
      label {
        display: block;
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 6px;
      }
      textarea {
        width: 100%;
        min-height: 90px;
        padding: 12px;
        font-size: 15px;
        font-family: inherit;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        background: #ffffff;
        color: #111827;
        resize: vertical;
        outline: none;
        transition: border-color 0.15s;
      }
      textarea:focus {
        border-color: #6366f1;
      }
      button {
        width: 100%;
        padding: 14px;
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        background: #6366f1;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        margin-top: 8px;
        transition: background 0.15s;
      }
      button:active { background: #4f46e5; }
      button:disabled { background: #a5b4fc; cursor: default; }
      .feedback {
        margin-top: 16px;
        padding: 12px;
        border-radius: 10px;
        font-size: 14px;
        display: none;
      }
      .feedback.success {
        background: #f0fdf4;
        color: #16a34a;
        border: 1px solid #bbf7d0;
      }
      .feedback.error {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
      }
    </style>
  </head>
  <body>
    <h1>今日の振り返り</h1>
    <div class="date" id="today-date"></div>

    <div class="field">
      <label>今、本当にやりたいことは何ですか？</label>
      <textarea id="want_to_do" placeholder="自由に書いてください。"></textarea>
    </div>
    <div class="field">
      <label>今、不安に感じていることはありますか？</label>
      <textarea id="anxiety" placeholder="自由に書いてください。"></textarea>
    </div>
    <div class="field">
      <label>無意識が求めていると感じることはありますか？</label>
      <textarea id="unconscious_desire" placeholder="自由に書いてください。"></textarea>
    </div>
    <div class="field">
      <label>自由に書いてください。</label>
      <textarea id="free_text" placeholder="何でも。"></textarea>
    </div>

    <button id="save-btn" onclick="save()">保存する</button>
    <div class="feedback" id="feedback"></div>

    <script>
      let existingId = null;

      function todayJST() {
        const now = new Date();
        const jst = new Date(now.getTime() + 9 * 60 * 60 * 1000);
        return jst.toISOString().slice(0, 10);
      }

      function nowJST() {
        const now = new Date();
        const jst = new Date(now.getTime() + 9 * 60 * 60 * 1000);
        return jst.toISOString().replace("Z", "+09:00").slice(0, 19) + "+09:00";
      }

      function showFeedback(msg, type) {
        const el = document.getElementById("feedback");
        el.textContent = msg;
        el.className = "feedback " + type;
        el.style.display = "block";
        setTimeout(() => { el.style.display = "none"; }, 3000);
      }

      async function init() {
        const today = todayJST();
        document.getElementById("today-date").textContent = today;

        try {
          const res = await fetch("/reflections/today");
          if (!res.ok) return;
          const data = await res.json();
          const r = data.reflection;
          if (r) {
            existingId = r.id;
            document.getElementById("want_to_do").value = r.want_to_do || "";
            document.getElementById("anxiety").value = r.anxiety || "";
            document.getElementById("unconscious_desire").value = r.unconscious_desire || "";
            document.getElementById("free_text").value = r.free_text || "";
          }
        } catch (e) {
          // 無視して空フォームで起動
        }
      }

      async function save() {
        const btn = document.getElementById("save-btn");
        btn.disabled = true;

        const body = {
          want_to_do: document.getElementById("want_to_do").value.trim() || null,
          anxiety: document.getElementById("anxiety").value.trim() || null,
          unconscious_desire: document.getElementById("unconscious_desire").value.trim() || null,
          free_text: document.getElementById("free_text").value.trim() || null,
        };

        const isEmpty = Object.values(body).every(v => v === null);
        if (isEmpty) {
          showFeedback("何か入力してから保存してください。", "error");
          btn.disabled = false;
          return;
        }

        try {
          let res;
          if (existingId) {
            res = await fetch("/reflections/" + existingId, {
              method: "PATCH",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(body),
            });
          } else {
            res = await fetch("/reflections", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ ...body, recorded_at: nowJST() }),
            });
            if (res.ok) {
              const data = await res.json();
              existingId = data.reflection?.id ?? null;
            }
          }

          if (res.ok) {
            showFeedback("保存しました。", "success");
          } else {
            showFeedback("保存に失敗しました (" + res.status + ")", "error");
          }
        } catch (e) {
          showFeedback("通信エラー: " + e.message, "error");
        }

        btn.disabled = false;
      }

      init();
    </script>
  </body>
</html>
    """
    return HTMLResponse(content=html)



@router.get("/steps", response_class=HTMLResponse)
def steps_ui() -> HTMLResponse:
    html = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Daily Steps</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      :root {
        color-scheme: light;
      }
      body {
        margin: 0;
        padding: 24px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #f6f7fb;
        color: #111827;
      }
      .container {
        max-width: 980px;
        margin: 0 auto;
      }
      h1 {
        margin: 0 0 16px;
        font-size: 24px;
      }
      .meta,
      .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 8px;
        margin-bottom: 16px;
      }
      .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 12px;
      }
      .label {
        font-size: 12px;
        color: #6b7280;
      }
      .value {
        margin-top: 6px;
        font-size: 18px;
        font-weight: 600;
      }
      .chart-card {
        height: 420px;
      }
      .error {
        color: #b91c1c;
        margin-top: 8px;
      }
      .footnote {
        margin-top: 12px;
        font-size: 12px;
        color: #6b7280;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>歩数（日次）</h1>

      <div class="meta">
        <div class="card">
          <div class="label">start_day</div>
          <div id="start-day" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">end_day</div>
          <div id="end-day" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">rows件数</div>
          <div id="rows-count" class="value">0</div>
        </div>
      </div>

      <div class="card chart-card">
        <canvas id="steps-chart"></canvas>
      </div>
      <div id="error" class="error"></div>
      <div class="footnote">source: health_connect / metric: steps_total / days: 90</div>

      <div class="stats" style="margin-top: 16px;">
        <div class="card">
          <div class="label">最新値</div>
          <div id="latest" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">前日差分</div>
          <div id="day-diff" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">週平均差</div>
          <div id="week-diff" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">7日移動平均</div>
          <div id="dma7-latest" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">平均 (mean)</div>
          <div id="mean" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">標準偏差 (std)</div>
          <div id="std" class="value">-</div>
        </div>
      </div>
    </div>

    <script>
      const endpoint = "/metrics/daily?metric=steps_total&source=health_connect&days=90";

      function mean(values) {
        if (values.length === 0) return null;
        return values.reduce((sum, v) => sum + v, 0) / values.length;
      }

      function std(values, avg) {
        if (values.length === 0 || avg === null) return null;
        const variance = values.reduce((sum, v) => sum + (v - avg) ** 2, 0) / values.length;
        return Math.sqrt(variance);
      }

      function movingAverage(values, windowSize) {
        const result = [];
        for (let i = 0; i < values.length; i++) {
          if (i < windowSize - 1) {
            result.push(null);
            continue;
          }
          let sum = 0;
          for (let j = i - windowSize + 1; j <= i; j++) {
            sum += values[j];
          }
          result.push(sum / windowSize);
        }
        return result;
      }

      function formatNumber(value, fractionDigits = 1) {
        if (value === null || !Number.isFinite(value)) return "-";
        return value.toLocaleString("ja-JP", {
          minimumFractionDigits: fractionDigits,
          maximumFractionDigits: fractionDigits,
        });
      }

      async function init() {
        const startDayEl = document.getElementById("start-day");
        const endDayEl = document.getElementById("end-day");
        const rowsCountEl = document.getElementById("rows-count");
        const latestEl = document.getElementById("latest");
        const dayDiffEl = document.getElementById("day-diff");
        const weekDiffEl = document.getElementById("week-diff");
        const meanEl = document.getElementById("mean");
        const stdEl = document.getElementById("std");
        const dma7LatestEl = document.getElementById("dma7-latest");
        const errorEl = document.getElementById("error");

        try {
          const res = await fetch(endpoint);
          if (!res.ok) {
            throw new Error("fetch failed: " + res.status);
          }

          const payload = await res.json();
          const rows = Array.isArray(payload.rows) ? payload.rows : [];
          const labels = rows.map((r) => r.day);
          const values = rows.map((r) => Number(r.value ?? 0));
          const dma7 = movingAverage(values, 7);

          startDayEl.textContent = payload.start_day ?? "-";
          endDayEl.textContent = payload.end_day ?? "-";
          rowsCountEl.textContent = String(rows.length);

          const avg = mean(values);
          const sigma = std(values, avg);
          const dma7Latest = dma7.filter((v) => Number.isFinite(v)).slice(-1)[0] ?? null;

          // 最新値・前日差分・週平均差
          const latestVal = values.length > 0 ? values[values.length - 1] : null;
          const prevVal = values.length > 1 ? values[values.length - 2] : null;
          const week7 = values.length >= 7 ? values.slice(-7) : null;
          const week7avg = week7 ? mean(week7) : null;

          latestEl.textContent = latestVal !== null ? Math.round(latestVal).toLocaleString("ja-JP") + " 歩" : "-";

          if (latestVal !== null && prevVal !== null) {
            const diff = Math.round(latestVal - prevVal);
            dayDiffEl.textContent = (diff >= 0 ? "+" : "") + diff.toLocaleString("ja-JP") + " 歩";
            dayDiffEl.style.color = diff >= 0 ? "#16a34a" : "#dc2626";
          } else {
            dayDiffEl.textContent = "-";
          }

          if (latestVal !== null && week7avg !== null) {
            const wdiff = Math.round(latestVal - week7avg);
            weekDiffEl.textContent = (wdiff >= 0 ? "+" : "") + wdiff.toLocaleString("ja-JP") + " 歩";
            weekDiffEl.style.color = wdiff >= 0 ? "#16a34a" : "#dc2626";
          } else {
            weekDiffEl.textContent = "-";
          }

          meanEl.textContent = formatNumber(avg);
          stdEl.textContent = formatNumber(sigma);
          dma7LatestEl.textContent = formatNumber(dma7Latest);

          const ctx = document.getElementById("steps-chart");
          new Chart(ctx, {
            type: "line",
            data: {
              labels,
              datasets: [
                {
                  label: "steps_total",
                  data: values,
                  borderColor: "#1d4ed8",
                  backgroundColor: "rgba(29, 78, 216, 0.12)",
                  tension: 0,
                  pointRadius: 2,
                  pointHoverRadius: 4,
                  fill: false,
                },
                {
                  label: "7dma",
                  data: dma7,
                  borderColor: "#dc2626",
                  tension: 0,
                  borderDash: [6, 4],
                  pointRadius: 0,
                  spanGaps: true,
                },
              ],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              interaction: {
                mode: "index",
                intersect: false,
              },
              scales: {
                y: {
                  beginAtZero: true,
                  title: {
                    display: true,
                    text: "steps",
                  },
                },
              },
            },
          });
        } catch (err) {
          errorEl.textContent = "データ取得に失敗しました: " + err.message;
        }
      }

      init();
    </script>
  </body>
</html>
    """
    return HTMLResponse(content=html)
