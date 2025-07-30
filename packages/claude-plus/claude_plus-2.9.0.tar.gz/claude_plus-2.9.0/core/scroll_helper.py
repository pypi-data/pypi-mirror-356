#!/usr/bin/env python3
"""
Claude Code スクロール操作ヘルパー
ユーザーへの操作ガイド表示と設定確認
"""

import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ScrollHelper:
    """スクロール操作のヘルプとガイダンス"""
    
    @staticmethod
    def show_scroll_guide():
        """スクロール操作ガイドを表示"""
        guide = """
╔══════════════════════════════════════════════════════════════╗
║                 🎯 Claude Code スクロール操作ガイド           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📜 チャット履歴をスクロールする方法:                          ║
║                                                              ║
║  🔹 PageUp / PageDown     ページ単位でスクロール               ║
║  🔹 Shift + ↑ / ↓       行単位でスクロール                   ║  
║  🔹 Ctrl + U / D         高速ページスクロール                  ║
║  🔹 マウスホイール         自然なスクロール                     ║
║  🔹 Esc                  通常入力モードに戻る                  ║
║                                                              ║
║  💡 コピー機能（viモード）:                                   ║
║  🔹 v                    選択開始                            ║
║  🔹 y                    選択範囲をコピー                       ║
║  🔹 j / k                上下移動                            ║
║                                                              ║
║  ✨ これらの操作はClaude Codeペインでのみ動作します            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        
        print(guide)
        logger.info("スクロール操作ガイドを表示しました")
    
    @staticmethod
    def check_scroll_settings(session_name: str) -> Dict[str, Any]:
        """現在のスクロール設定を確認"""
        try:
            # 履歴制限を確認
            result = subprocess.run(
                f"tmux show-options -t {session_name} history-limit",
                shell=True,
                capture_output=True,
                text=True
            )
            history_limit = result.stdout.strip() if result.returncode == 0 else "不明"
            
            # viモードを確認
            result = subprocess.run(
                f"tmux show-options -t {session_name} mode-keys",
                shell=True,
                capture_output=True,
                text=True
            )
            mode_keys = result.stdout.strip() if result.returncode == 0 else "不明"
            
            # マウス設定を確認
            result = subprocess.run(
                f"tmux show-options -t {session_name} mouse",
                shell=True,
                capture_output=True,
                text=True
            )
            mouse_setting = result.stdout.strip() if result.returncode == 0 else "不明"
            
            settings = {
                "履歴制限": history_limit,
                "キーモード": mode_keys,
                "マウス設定": mouse_setting,
                "セッション": session_name
            }
            
            logger.info(f"スクロール設定確認: {settings}")
            return settings
            
        except Exception as e:
            logger.error(f"設定確認エラー: {e}")
            return {"エラー": str(e)}
    
    @staticmethod
    def show_quick_tips():
        """クイックヒントを表示"""
        tips = """
🚀 Claude++ スクロール クイックヒント:

• チャット履歴が長くなったら PageUp でさかのぼれます
• Shift+↑↓ で細かく調整できます  
• 長いコードをコピーしたい時は v → 選択 → y でコピー
• Esc で通常の入力モードに戻ります

💡 履歴は10万行まで保存されるので、長時間の作業でも安心です！
        """
        print(tips)
    
    @staticmethod
    def troubleshoot_scroll_issues():
        """スクロール問題のトラブルシューティング"""
        troubleshoot = """
🔧 スクロールがうまく動かない場合:

1. Claude Codeペイン（上部）にカーソルがあることを確認
2. PageUp/PageDownが反応しない → Ctrl+B を押してからPageUp
3. 通常入力に戻れない → Esc キーを押す
4. コピーモードから抜けられない → Esc または q を押す

📞 それでも解決しない場合は、セッションを再起動してください。
        """
        print(troubleshoot)


def main():
    """テスト用メイン関数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "guide":
            ScrollHelper.show_scroll_guide()
        elif command == "tips":
            ScrollHelper.show_quick_tips()
        elif command == "troubleshoot":
            ScrollHelper.troubleshoot_scroll_issues()
        elif command == "check" and len(sys.argv) > 2:
            session_name = sys.argv[2]
            settings = ScrollHelper.check_scroll_settings(session_name)
            print("📊 現在の設定:")
            for key, value in settings.items():
                print(f"  {key}: {value}")
    else:
        print("使用方法: python3 scroll_helper.py [guide|tips|troubleshoot|check <session_name>]")


if __name__ == "__main__":
    main()