#!/bin/bash
# 目的: システム起動時にフォークの同期をチェック
# 入力: なし
# 出力: 同期結果をログに記録
# 実行方法: システム起動時に自動実行

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/sync.log"

echo "$(date): 起動時同期チェック開始" >> "$LOG_FILE"

cd "$SCRIPT_DIR"
if uv run sync_upstream.py >> "$LOG_FILE" 2>&1; then
    echo "$(date): 同期成功" >> "$LOG_FILE"
else
    echo "$(date): 同期失敗" >> "$LOG_FILE"
fi