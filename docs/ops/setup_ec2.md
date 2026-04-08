# EC2 セットアップ手順

Body Data Lab を AWS EC2 上で稼働させる手順書。

設計の背景は [../design/aws_deployment.md](../design/aws_deployment.md) を参照。

---

## 前提

- AWS アカウントあり
- ローカルに AWS CLI または AWS コンソールからの操作が可能
- ドメインまたは Elastic IP（nip.io 経由）を用意する

---

## 1. EC2 インスタンス起動

AWS コンソール → EC2 → インスタンスを起動

| 項目 | 値 |
|-----|---|
| AMI | Amazon Linux 2023 (x86_64) |
| インスタンスタイプ | t3.micro（無料枠）または t3.small |
| ストレージ | gp3 8GB（デフォルト） |
| キーペア | 作成してローカルに保存（`~/.ssh/body-data-lab.pem`） |

**Security Group の設定:**

| タイプ | ポート | ソース | 用途 |
|------|-------|-------|------|
| SSH | 22 | 自宅 IP/32 | 管理 |
| HTTPS | 443 | 0.0.0.0/0, ::/0 | Android からのデータ送信 |

---

## 2. Elastic IP 取得・アタッチ

AWS コンソール → EC2 → Elastic IP アドレス → 割り当て → インスタンスに関連付け

---

## 3. SSH 接続確認

```bash
chmod 400 ~/.ssh/body-data-lab.pem
ssh -i ~/.ssh/body-data-lab.pem ec2-user@[Elastic IP]
```

---

## 4. EC2 初期設定

```bash
# パッケージ更新
sudo dnf update -y

# Docker, nginx, git インストール
sudo dnf install -y docker nginx git

# Docker 起動・自動起動設定
sudo systemctl enable --now docker

# ec2-user を docker グループに追加（再ログイン後に有効）
sudo usermod -aG docker ec2-user

# 再ログイン
exit
ssh -i ~/.ssh/body-data-lab.pem ec2-user@[Elastic IP]
```

---

## 5. Docker Compose インストール

```bash
COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

---

## 6. アプリデプロイ

```bash
git clone https://github.com/[your-repo]/body-data-lab.git
cd body-data-lab

# .env 作成（.env.example を参考に MAIL_* を設定）
cp .env.example .env
nano .env
```

`.env` に設定する最低限の項目:

```env
DB_PATH=/app/data/body_data_lab.sqlite3
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-gmail@gmail.com
MAIL_TO=your-gmail@gmail.com
MAIL_TLS=true
```

```bash
# データディレクトリ作成
mkdir -p ~/body-data-lab/data

# 本番用 compose で起動
docker-compose -f docker-compose.prod.yml up -d

# 動作確認
curl http://127.0.0.1:8000/
```

---

## 7. nginx + Let's Encrypt 設定

### ドメインがある場合

```bash
# DNS の A レコードを Elastic IP に向けておく

sudo dnf install -y certbot python3-certbot-nginx

# nginx 設定ファイル配置（YOUR_DOMAIN を実際のドメインに置換）
sudo cp ~/body-data-lab/docs/ops/nginx.conf /etc/nginx/conf.d/body-data-lab.conf
sudo sed -i 's/YOUR_DOMAIN/your-domain.com/g' /etc/nginx/conf.d/body-data-lab.conf

# 証明書取得
sudo certbot --nginx -d your-domain.com

# nginx 起動・自動起動
sudo systemctl enable --now nginx
```

### ドメインがない場合（nip.io を使う）

Elastic IP が `13.115.123.45` の場合、ドメインは `13-115-123-45.nip.io` になる。

```bash
sudo certbot --nginx -d 13-115-123-45.nip.io
```

---

## 8. ETL cron 設定

```bash
# cron ファイルを配置
sudo tee /etc/cron.d/body-data-lab-etl > /dev/null << 'EOF'
# 毎朝 6:00 JST (= UTC 21:00 前日) に ETL 実行
0 21 * * * ec2-user cd /home/ec2-user/body-data-lab && docker-compose -f docker-compose.prod.yml run --rm etl >> /var/log/body-data-lab-etl.log 2>&1
EOF

sudo chmod 644 /etc/cron.d/body-data-lab-etl
sudo systemctl restart crond
```

ログ確認:
```bash
tail -f /var/log/body-data-lab-etl.log
```

---

## 9. 動作確認

```bash
# API 疎通確認（EC2 から）
curl http://127.0.0.1:8000/

# HTTPS 確認（外部から、または EC2 から）
curl https://your-domain.com/

# Swagger UI（ブラウザで開く）
# https://your-domain.com/docs
```

---

## 10. Android アプリの接続先を変更

`MainActivity.kt` の `API_URL` を更新:

```kotlin
// 変更後
private val API_URL = "https://your-domain.com/ingest"
```

`AndroidManifest.xml` から cleartext 許可を削除:

```xml
<!-- この行を削除 -->
android:usesCleartextTraffic="true"
```

Android Studio でビルドしてデバイスにインストールする。

---

## メンテナンス操作

```bash
# アプリ再起動
cd ~/body-data-lab
docker-compose -f docker-compose.prod.yml restart app

# ログ確認
docker-compose -f docker-compose.prod.yml logs -f app

# アプリ更新（git pull してリビルド）
git pull
docker-compose -f docker-compose.prod.yml up -d --build app

# ETL 手動実行
docker-compose -f docker-compose.prod.yml run --rm etl

# Let's Encrypt 証明書更新（自動更新の確認）
sudo certbot renew --dry-run
```

---

## 関連ファイル

- `docker-compose.prod.yml` — 本番用 Docker Compose 設定
- `docs/ops/nginx.conf` — nginx 設定テンプレート
- `docs/design/aws_deployment.md` — AWS 構成設計
- `.env.example` — 環境変数テンプレート
