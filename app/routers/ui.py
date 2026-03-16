from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/ui", tags=["ui"])


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
          <div class="label">平均 (mean)</div>
          <div id="mean" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">標準偏差 (std)</div>
          <div id="std" class="value">-</div>
        </div>
        <div class="card">
          <div class="label">7日移動平均 (最新)</div>
          <div id="dma7-latest" class="value">-</div>
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
