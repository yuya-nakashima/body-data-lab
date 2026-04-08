#!/bin/bash
# SQLite を S3 にバックアップするスクリプト
# 使い方: bash docs/ops/backup.sh
#
# 前提:
#   - aws cli がインストール済み
#   - EC2 に S3 書き込み権限の IAM ロールがアタッチされている
#   - S3_BUCKET 環境変数を設定済み（例: export S3_BUCKET=body-data-lab-backup）

set -euo pipefail

DB_PATH="${DB_PATH:-/home/ec2-user/body-data-lab/data/body_data_lab.sqlite3}"
S3_BUCKET="${S3_BUCKET:?S3_BUCKET 環境変数を設定してください}"
TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")
BACKUP_KEY="backups/body_data_lab_${TIMESTAMP}.sqlite3"

if [ ! -f "$DB_PATH" ]; then
  echo "DB ファイルが見つかりません: $DB_PATH"
  exit 1
fi

aws s3 cp "$DB_PATH" "s3://${S3_BUCKET}/${BACKUP_KEY}"
echo "バックアップ完了: s3://${S3_BUCKET}/${BACKUP_KEY}"

# 30日以上古いバックアップを削除
aws s3 ls "s3://${S3_BUCKET}/backups/" | while read -r line; do
  DATE=$(echo "$line" | awk '{print $1}')
  FILE=$(echo "$line" | awk '{print $4}')
  if [[ $(date -d "$DATE" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$DATE" +%s) -lt $(date -d "30 days ago" +%s 2>/dev/null || date -v-30d +%s) ]]; then
    aws s3 rm "s3://${S3_BUCKET}/backups/${FILE}"
    echo "古いバックアップを削除: ${FILE}"
  fi
done
