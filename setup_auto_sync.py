#!/usr/bin/env python3
"""
目的: フォーク自動同期の設定をセットアップする
入力: なし
出力: cronジョブとsystemdサービスの設定手順を表示
実行方法: uv run setup_auto_sync.py
"""

# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

import os
from pathlib import Path


def get_current_dir() -> str:
    """現在のスクリプトのディレクトリを取得"""
    return str(Path(__file__).parent.absolute())


def print_cron_setup():
    """cronジョブの設定方法を表示"""
    current_dir = get_current_dir()
    
    print("📅 Cronジョブ設定 (定期実行)")
    print("=" * 50)
    print("以下のコマンドでcronジョブを追加できます:\n")
    
    print("1. crontabエディタを開く:")
    print("   crontab -e\n")
    
    print("2. 以下の行を追加:")
    print("   # 毎日午前9時に同期チェック")
    print(f"   0 9 * * * cd {current_dir} && uv run sync_upstream.py >> sync.log 2>&1")
    print()
    print("   # 毎時0分に同期チェック")
    print(f"   0 * * * * cd {current_dir} && uv run sync_upstream.py >> sync.log 2>&1")
    print()


def print_systemd_setup():
    """systemdサービスの設定方法を表示"""
    current_dir = get_current_dir()
    user = os.getenv('USER', 'user')
    
    print("🔧 Systemdサービス設定 (起動時実行)")
    print("=" * 50)
    print("以下の手順でsystemdサービスを設定できます:\n")
    
    print("1. サービスファイルを作成:")
    print(f"   sudo tee /etc/systemd/system/fork-sync.service << 'EOF'")
    print("[Unit]")
    print("Description=Fork Repository Sync")
    print("After=network.target")
    print()
    print("[Service]")
    print("Type=oneshot")
    print(f"User={user}")
    print(f"WorkingDirectory={current_dir}")
    print(f"ExecStart={current_dir}/startup_sync.sh")
    print()
    print("[Install]")
    print("WantedBy=multi-user.target")
    print("EOF\n")
    
    print("2. サービスを有効化:")
    print("   sudo systemctl enable fork-sync.service")
    print("   sudo systemctl start fork-sync.service\n")
    
    print("3. 状態確認:")
    print("   sudo systemctl status fork-sync.service\n")


def print_manual_usage():
    """手動実行の方法を表示"""
    print("🔧 手動実行")
    print("=" * 50)
    print("いつでも手動で同期できます:")
    print("   uv run sync_upstream.py\n")
    print("ログファイルを確認:")
    print("   tail -f sync.log\n")


if __name__ == "__main__":
    print("🚀 フォーク自動同期セットアップガイド")
    print("=" * 60)
    print()
    
    print_manual_usage()
    print_cron_setup()
    print_systemd_setup()
    
    print("💡 推奨設定:")
    print("- 開発用: 手動実行またはcronで毎日1回")
    print("- プロダクション用: systemdサービス + cronで定期チェック")
    print()
    print("⚠️  注意: 未コミットの変更がある場合は同期をスキップします")