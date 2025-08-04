#!/usr/bin/env python3
"""
目的: フォークを upstream リポジトリと同期する
入力: なし（git リポジトリのディレクトリで実行）
出力: 同期結果をコンソールに出力
実行方法: uv run sync_upstream.py
"""

# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: str = None) -> tuple[bool, str]:
    """コマンドを実行し、成功/失敗と出力を返す"""
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=cwd,
            check=False
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def check_git_repo() -> bool:
    """現在のディレクトリがgitリポジトリかチェック"""
    return Path('.git').exists()


def check_upstream_remote() -> bool:
    """upstream リモートが設定されているかチェック"""
    success, output = run_command(['git', 'remote'])
    return success and 'upstream' in output


def get_current_branch() -> str:
    """現在のブランチ名を取得"""
    success, output = run_command(['git', 'branch', '--show-current'])
    return output.strip() if success else 'main'


def sync_with_upstream() -> bool:
    """upstream と同期する"""
    print("🔄 upstream との同期を開始...")
    
    if not check_git_repo():
        print("❌ エラー: gitリポジトリではありません")
        return False
    
    if not check_upstream_remote():
        print("❌ エラー: upstream リモートが設定されていません")
        return False
    
    current_branch = get_current_branch()
    print(f"📍 現在のブランチ: {current_branch}")
    
    # upstream から fetch
    print("📥 upstream から変更を取得中...")
    success, output = run_command(['git', 'fetch', 'upstream'])
    if not success:
        print(f"❌ fetch エラー: {output}")
        return False
    
    # ローカルの変更状態をチェック
    success, output = run_command(['git', 'status', '--porcelain'])
    if success and output.strip():
        print("⚠️  未コミットの変更があります。先にコミットまたはstashしてください。")
        return False
    
    # upstream と比較
    success, output = run_command(['git', 'rev-list', '--count', f'{current_branch}..upstream/{current_branch}'])
    if not success:
        print(f"❌ ブランチ比較エラー: {output}")
        return False
    
    commits_behind = int(output.strip()) if output.strip().isdigit() else 0
    
    if commits_behind == 0:
        print("✅ フォークは最新です")
        return True
    
    print(f"📊 upstream より {commits_behind} コミット遅れています")
    
    # マージ実行
    print("🔀 upstream の変更をマージ中...")
    success, output = run_command(['git', 'merge', f'upstream/{current_branch}'])
    if not success:
        print(f"❌ マージエラー: {output}")
        return False
    
    # origin にプッシュ
    print("📤 フォークに変更をプッシュ中...")
    success, output = run_command(['git', 'push', 'origin', current_branch])
    if not success:
        print(f"❌ プッシュエラー: {output}")
        return False
    
    print("✅ 同期完了！")
    return True


if __name__ == "__main__":
    success = sync_with_upstream()
    sys.exit(0 if success else 1)