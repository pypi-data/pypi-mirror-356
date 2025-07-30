#!/usr/bin/env python3
"""
ペイン独立スクロール制御モジュール
Claude Codeペインのみスクロール可能にし、コントロールパネルは固定
"""

import subprocess
import logging

logger = logging.getLogger(__name__)


class PaneScrollController:
    """ペイン独立スクロール制御クラス"""
    
    @staticmethod
    def setup_independent_scrolling(session_name: str):
        """独立スクロールの設定"""
        try:
            # Claudeペイン（上部）とコントロールペイン（下部）を識別
            claude_pane = f"{session_name}:0.0"
            control_pane = f"{session_name}:0.1"
            
            # コントロールペインのスクロールを無効化
            # remain-on-exitを設定して、ペインの内容を固定
            subprocess.run([
                'tmux', 'set-option', '-t', control_pane, 
                'remain-on-exit', 'on'
            ], capture_output=True)
            
            # コントロールペインのバッファサイズを小さくする
            subprocess.run([
                'tmux', 'set-option', '-t', control_pane,
                'history-limit', '0'
            ], capture_output=True)
            
            logger.info("独立スクロールを設定しました")
            return True
            
        except Exception as e:
            logger.error(f"独立スクロール設定エラー: {e}")
            return False
    
    @staticmethod
    def create_scroll_keybindings(session_name: str):
        """スクロール用キーバインドの作成"""
        try:
            # Ctrl+b, PageUp/PageDownでClaudeペインのみスクロール
            claude_pane = f"{session_name}:0.0"
            
            # PageUpでClaudeペインをスクロール
            subprocess.run([
                'tmux', 'bind-key', '-n', 'PageUp',
                f'if-shell -F -t = "#{pane_id}" = "{claude_pane}" "copy-mode -u"'
            ], capture_output=True)
            
            # PageDownでClaudeペインをスクロール
            subprocess.run([
                'tmux', 'bind-key', '-n', 'PageDown',
                f'if-shell -F -t = "#{pane_id}" = "{claude_pane}" "copy-mode; send-keys -X page-down"'
            ], capture_output=True)
            
            logger.info("スクロールキーバインドを設定しました")
            return True
            
        except Exception as e:
            logger.error(f"キーバインド設定エラー: {e}")
            return False