# AWS デプロイ設計

Body Data Lab バックエンドを AWS 上で稼働させ、Android アプリからデータを受信・メール通知を送る構成の設計書。

---

## 全体構成

```
[Android アプリ]
  Health Connect → 歩数データ取得
        │
        │ HTTPS POST /ingest
        ▼
[EC2 (t3.micro)]
  ┌─────────────────────────────┐
  │  nginx (リバースプロキシ)    │  ← Let's Encrypt TLS 終端
  │    ↓ :8000                  │
  │  FastAPI (Docker)           │  ← ingest / normalize / aggregate / metrics
  │    ↓                        │
  │  SQLite (EBS)               │  ← /app/data/body_data_lab.sqlite3
  │                             │
  │  cron → etl/main.py         │  ← 毎朝 6:00 JST 実行
  │    ↓                        │
  │  Gmail SMTP                 │  ← 日次サマリーメール送信
  └─────────────────────────────┘
        │
        │ Elastic IP (固定)
        ▼
  [ドメイン or IP で Android が接続]
```

---

## 使用 AWS サービス

| サービス | 用途 | 選定理由 |
|---------|------|---------|
| **EC2 t3.micro** | FastAPI 実行 + ETL cron | SQLite が persistent に使えるサーバー構成が最シンプル。個人用途なら無料枠または月 $10-15 程度 |
| **EBS (8GB gp3)** | SQLite データ永続化 | EC2 にデフォルトでアタッチされる。data/ をここに置く |
| **Elastic IP** | 固定パブリック IP | Android アプリの接続先 URL が変わらないようにする |
| **Security Group** | ファイアウォール | SSH (22), HTTPS (443) のみ開放。8000 は外に出さない |

### 使わないもの（理由）

| サービス | 使わない理由 |
|---------|------------|
| RDS | SQLite で十分。個人データ量では不要 |
| ECS / Fargate | SQLite の永続化が複雑になる。EC2 + Docker Compose の方がシンプル |
| Lambda | 常駐 + SQLite との相性が悪い |
| SES | Gmail SMTP で動いているので変えない。送信量も少ない |
| Route 53 | ドメインを持っていれば使う。なければ Elastic IP + nip.io で代替可能 |
| ALB | 1台構成なので不要 |
| CloudWatch | ログは EC2 上の journald + ファイルで十分 |

---

## ネットワーク・セキュリティ設計

### Security Group ルール

| 方向 | ポート | 送信元 | 用途 |
|-----|-------|--------|------|
| インバウンド | 22 | 自宅 IP のみ | SSH 管理 |
| インバウンド | 443 | 0.0.0.0/0 | Android からの HTTPS |
| アウトバウンド | 全て | 0.0.0.0/0 | Gmail SMTP, パッケージ更新 |

**ポート 8000 は外部に開放しない**（nginx 経由のみ）。

### HTTPS 対応

**ドメインがある場合（推奨）:**
- nginx + Certbot (Let's Encrypt) で無料 TLS 証明書
- `https://your-domain.com/ingest` を Android の API_URL に設定

**ドメインがない場合:**
- Elastic IP を使って `https://[EIP].nip.io` 形式で Let's Encrypt 発行可能
  - 例: `https://13-115-123-45.nip.io`
  - nip.io は IP をドメインに変換するフリーサービス

---

## EC2 上のソフトウェア構成

```
/home/ec2-user/body-data-lab/   ← git clone 先
  app/
  etl/
  docker-compose.yml
  .env                          ← 環境変数（MAIL_*, DB_PATH）
  data/
    body_data_lab.sqlite3       ← EBS に永続化

/etc/nginx/conf.d/body-data-lab.conf   ← nginx 設定
/etc/cron.d/body-data-lab-etl          ← ETL cron
```

### docker-compose（本番用）

現在の `docker-compose.yml` から `--reload` を外し、`mailpit` を削除した本番設定を用意する。

```yaml
services:
  app:
    build: .
    ports:
      - "127.0.0.1:8000:8000"      # ← localhost のみ。nginx 経由で外部公開
    volumes:
      - /home/ec2-user/body-data-lab/data:/app/data
    env_file: .env
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    restart: unless-stopped
```

`127.0.0.1:8000` にバインドすることで、EC2 の Security Group で 8000 を開けなくても nginx 経由でのみアクセスできる。

### nginx 設定

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;   # または [EIP].nip.io

    ssl_certificate     /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}
```

### ETL cron

```cron
# /etc/cron.d/body-data-lab-etl
# 毎朝 6:00 JST (= 21:00 UTC 前日) に ETL 実行
0 21 * * * ec2-user cd /home/ec2-user/body-data-lab && /usr/bin/docker compose run --rm etl >> /var/log/body-data-lab-etl.log 2>&1
```

---

## Android アプリの変更点

### 変更箇所: `MainActivity.kt`

```kotlin
// 変更前
private val API_URL = "http://127.0.0.1:8000/ingest"

// 変更後
private val API_URL = "https://your-domain.com/ingest"
```

### `AndroidManifest.xml` の変更

HTTPS に変更するため `usesCleartextTraffic` は不要になる（削除 or false に）。

```xml
<!-- 削除 -->
android:usesCleartextTraffic="true"
```

### 送信するペイロード形式の確認

現在の Android 送信フォーマット:
```json
{
  "source": "health_connect",
  "metric": "steps",
  "start_at": "2026-04-07T00:00:00+09:00",
  "end_at": "2026-04-08T00:00:00+09:00",
  "value": 8432,
  "unit": "count"
}
```

バックエンドの `POST /ingest` が受け取る形式と一致しているか確認が必要。
→ `app/routers/ingest.py` を参照して齟齬があれば合わせる。

---

## セットアップ手順（概要）

詳細な手順は別途 `docs/ops/setup_ec2.md` にまとめる予定。

1. **EC2 起動**
   - AMI: Amazon Linux 2023 (x86_64)
   - インスタンスタイプ: t3.micro（無料枠）または t3.small
   - ストレージ: gp3 8GB（デフォルトで十分）
   - Security Group: SSH (自宅IP), HTTPS (0.0.0.0/0)
   - キーペア: 作成してローカルに保存

2. **Elastic IP 取得・アタッチ**

3. **EC2 初期設定**
   ```bash
   sudo dnf update -y
   sudo dnf install -y docker nginx git
   sudo systemctl enable --now docker
   sudo usermod -aG docker ec2-user
   ```

4. **Docker Compose インストール**
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

5. **アプリデプロイ**
   ```bash
   git clone https://github.com/your-repo/body-data-lab.git
   cd body-data-lab
   cp .env.example .env
   # .env に MAIL_* を設定
   docker compose up -d app
   ```

6. **nginx + Let's Encrypt 設定**
   ```bash
   sudo dnf install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

7. **cron 設定**
   ```bash
   sudo cp docs/ops/cron/body-data-lab-etl /etc/cron.d/
   ```

8. **Android アプリの API_URL を更新してビルド・インストール**

---

## コスト概算

| 項目 | 月額概算 |
|-----|---------|
| EC2 t3.micro (無料枠終了後) | ~$10 |
| EBS 8GB gp3 | ~$0.6 |
| Elastic IP (インスタンスにアタッチ中は無料) | $0 |
| データ転送 (送信 1GB 以下) | ~$0 |
| **合計** | **~$11/月** |

無料枠 (12ヶ月以内) なら EC2 + EBS = **$0**。

---

## 今後の拡張ポイント

- **バックアップ**: SQLite ファイルを S3 に定期アップロード（aws cli + cron）
- **監視**: CloudWatch Agent でディスク・メモリ監視（無料枠内）
- **認証**: API キー認証を `/ingest` に追加（Android からはヘッダーで送信）
- **HTTPS 証明書自動更新**: `certbot renew` を cron に追加

---

## 関連ファイル

- `docker-compose.yml` — ローカル開発用設定
- `Dockerfile` — アプリイメージ定義
- `.env.example` — 環境変数テンプレート
- `etl/main.py` — ETL エントリポイント
- `docs/design/architecture.md` — 全体アーキテクチャ方針
- `docs/features/notifications.md` — 通知仕様
