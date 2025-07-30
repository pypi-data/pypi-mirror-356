#!/usr/bin/env python3
"""
Claude++ コントロールパネル アプリケーション
tmux下部ペインで動作する対話型UI
"""

import sys
import time
import os
import subprocess
from datetime import datetime
import signal

def clear_screen():
    """画面をクリア"""
    os.system('clear')

def show_header():
    """ヘッダーを表示"""
    # tmux互換性重視でシンプルなヘッダー
    print("=" * 60)
    print("             Claude++ Control Panel")
    print("=" * 60)

def show_status():
    """現在の状態を表示"""
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"\n📊 状態: 正常稼働中 | ⏰ {current_time} | 💾 自動保存: ON | 🌿 Git保護: ON")
    print("─" * 65)

def find_active_claude_session():
    """アクティブなclaude-plusセッションを動的に検出"""
    try:
        # アタッチされたclaude-plusセッションを探す
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}:#{session_attached}"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if 'claude_plus' in line:
                    parts = line.split(':')
                    session_name = parts[0]
                    is_attached = parts[1] == "1"
                    
                    if is_attached:
                        return f"{session_name}:0.0"  # Claude Codeペイン
            
            # アタッチされたセッションがない場合、最新のセッションを使用
            all_sessions = subprocess.run(
                ["tmux", "list-sessions", "-F", "#{session_name}:#{session_created}"],
                capture_output=True,
                text=True
            )
            
            if all_sessions.returncode == 0:
                claude_sessions = [line for line in all_sessions.stdout.split('\n') 
                                 if 'claude_plus' in line]
                
                if claude_sessions:
                    # 作成時刻で最新を選択
                    latest_session = max(claude_sessions, key=lambda x: int(x.split(':')[1]))
                    session_name = latest_session.split(':')[0]
                    return f"{session_name}:0.0"
        
        return "claude_plus:0.0"  # フォールバック
        
    except Exception as e:
        return "claude_plus:0.0"  # フォールバック

def check_claude_status():
    """Claude Codeの状態を確認"""
    try:
        # 動的にアクティブなセッションのペインを取得
        claude_pane = find_active_claude_session()
        
        # tmuxペインの内容を確認
        result = subprocess.run(
            ["tmux", "capture-pane", "-t", claude_pane, "-p"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            output = result.stdout
            # Claude Codeのプロンプトや出力を探す
            if "Claude:" in output or "Human:" in output or "$" in output or "❯" in output:
                return True, f"正常動作中 ({claude_pane})"
            else:
                return False, f"起動中... ({claude_pane})"
        else:
            return False, f"ペイン未検出 ({claude_pane})"
    except Exception as e:
        return False, f"確認エラー: {e}"

def show_help():
    """ヘルプを表示"""
    print("\n💡 使い方:")
    print("  • 上の画面のClaude Codeに直接質問してください")
    print("  • 例: 「main.pyを編集して」「テストを実行して」")
    print("\n⌨️  コマンド:")
    print("  help    - このヘルプを表示")
    print("  status  - 現在の状態を確認")
    print("  clear   - 画面をクリア")
    print("  exit    - Claude++を終了")
    print("\n🆘 トラブルシューティング:")
    print("  • Claude Codeが反応しない → 上の画面でEnterキーを押してみてください")
    print("  • エラーが出る → 'status'コマンドで状態を確認")
    print("  • 画面が崩れた → 'clear'コマンドで画面をリセット")

def main():
    """メインループ - シンプル版"""
    clear_screen()
    show_header()
    print("\n🎉 Claude++が起動しました！")
    print("\n📝 重要: 上の画面でClaude Codeと直接会話してください")
    print("   このパネルは情報表示のみです")
    print("\n例:")
    print("   上画面で「main.pyを作成して」と入力")
    print("   上画面で「テストを実行して」と入力")
    
    # 自動状態更新モード
    print("\n🔄 自動状態更新を開始します...")
    print("   Ctrl+C で終了")
    
    try:
        while True:
            show_status()
            
            # Claude Code状態チェック
            is_running, status_msg = check_claude_status()
            
            if is_running:
                print("[OK] Claude Code: 正常動作中")
            else:
                print(f"[!] Claude Code: {status_msg}")
                print("ヒント: 上の画面でEnterキーを押してください")
            
            print("─" * 65)
            print("📝 上の画面でClaude Codeに質問してください")
            print("[Ctrl+C] でClaude++を終了")
            
            # 30秒間隔で更新（CPU使用量軽減・重複描画軽減）
            time.sleep(30)
            clear_screen()
            show_header()
            
    except KeyboardInterrupt:
        print("\n\n👋 Claude++を終了します...")
        # tmuxセッションも終了
        try:
            subprocess.run(["tmux", "kill-session", "-t", "claude_plus"], 
                         capture_output=True)
        except:
            pass
        sys.exit(0)

if __name__ == "__main__":
    main()