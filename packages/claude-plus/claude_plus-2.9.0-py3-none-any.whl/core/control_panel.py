"""
日本語コントロールパネル
ユーザー入力の受付、ステータス表示、エラー翻訳を担当
"""

import asyncio
import time
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)


@dataclass
class Status:
    """システムステータス"""
    mode: str = "準備完了"
    auto_save_next: Optional[datetime] = None
    current_branch: str = "main"
    working_on: Optional[str] = None
    last_error: Optional[str] = None


class ErrorTranslator:
    """エラーメッセージの日本語翻訳"""
    
    ERROR_PATTERNS = {
        r"file not found": "ファイルが見つかりません",
        r"permission denied": "アクセス権限がありません",
        r"no such file or directory": "ファイルまたはディレクトリが存在しません",
        r"command not found": "コマンドが見つかりません",
        r"connection refused": "接続が拒否されました",
        r"timeout": "タイムアウトしました",
        r"module not found": "モジュールが見つかりません",
        r"syntax error": "構文エラーです",
        r"import error": "インポートエラーです",
        r"index out of range": "インデックスが範囲外です",
        r"key error": "キーが存在しません",
        r"type error": "型が一致しません",
        r"value error": "値が不正です",
        r"network error": "ネットワークエラーです",
        r"disk full": "ディスク容量が不足しています",
    }
    
    HINT_PATTERNS = {
        r"module not found.*requests": "pip install requests を実行してください",
        r"permission denied.*\.py": "chmod +x でファイルに実行権限を付与してください",
        r"git.*not a git repository": "git init でリポジトリを初期化してください",
        r"command not found.*python": "Pythonがインストールされているか確認してください",
        r"connection refused.*api": "APIサーバーが起動しているか確認してください",
    }
    
    @classmethod
    def translate(cls, error_msg: str) -> tuple[str, Optional[str]]:
        """エラーメッセージを翻訳し、ヒントを返す"""
        error_lower = error_msg.lower()
        
        # エラーメッセージの翻訳
        translated = error_msg
        for pattern, translation in cls.ERROR_PATTERNS.items():
            if re.search(pattern, error_lower):
                translated = translation
                break
        
        # ヒントの検索
        hint = None
        for pattern, hint_text in cls.HINT_PATTERNS.items():
            if re.search(pattern, error_lower):
                hint = hint_text
                break
        
        return translated, hint


class ControlPanel:
    """日本語コントロールパネル"""
    
    def __init__(self, screen_controller=None):
        self.screen_controller = screen_controller
        self.status = Status()
        self.command_history: List[str] = []
        self.running = False
        
        # 自動保存タイマー設定（30分）
        self.auto_save_interval = timedelta(minutes=30)
        self.reset_auto_save_timer()
    
    def reset_auto_save_timer(self):
        """自動保存タイマーをリセット"""
        self.status.auto_save_next = datetime.now() + self.auto_save_interval
    
    def format_status_line(self) -> str:
        """ステータスラインをフォーマット"""
        parts = []
        
        # 現在の状態
        parts.append(f"📊 {self.status.mode}")
        
        # 自動保存までの時間
        if self.status.auto_save_next:
            remaining = self.status.auto_save_next - datetime.now()
            minutes = int(remaining.total_seconds() / 60)
            if minutes > 0:
                parts.append(f"💾 自動保存: {minutes}分後")
            else:
                parts.append("💾 自動保存中...")
        
        # 現在のブランチ
        parts.append(f"🌿 {self.status.current_branch}")
        
        # 作業中のファイル
        if self.status.working_on:
            parts.append(f"📝 {self.status.working_on}")
        
        return " | ".join(parts)
    
    def format_welcome_message(self) -> List[str]:
        """ウェルカムメッセージをフォーマット"""
        return [
            "🇯🇵 Claude++ へようこそ！",
            "━" * 50,
            self.format_status_line(),
            "━" * 50,
            "",
            "💡 使い方のヒント:",
            "  • ファイル編集: 「main.pyを編集して」",
            "  • テスト作成: 「テストを書いて」",
            "  • モード切替: 「:mode developer」",
            "  • ヘルプ: 「:help」",
            "",
            "入力 > "
        ]
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """ユーザー入力を処理"""
        self.command_history.append(user_input)
        
        # コマンドモード（:で始まる）
        if user_input.startswith(":"):
            return self._process_command(user_input)
        
        # 通常の入力
        return {
            "type": "claude_command",
            "content": user_input,
            "timestamp": datetime.now()
        }
    
    def _process_command(self, command: str) -> Dict[str, Any]:
        """コマンドモードの処理"""
        cmd_parts = command[1:].split()
        if not cmd_parts:
            return {"type": "error", "message": "コマンドが空です"}
        
        cmd = cmd_parts[0].lower()
        args = cmd_parts[1:] if len(cmd_parts) > 1 else []
        
        if cmd == "mode":
            if args and args[0] in ["beginner", "developer", "focus"]:
                return {
                    "type": "mode_change",
                    "mode": args[0],
                    "message": f"{args[0]}モードに切り替えます"
                }
            else:
                return {
                    "type": "error",
                    "message": "使用法: :mode [beginner|developer|focus]"
                }
        
        elif cmd == "help":
            return {
                "type": "help",
                "message": self._get_help_text()
            }
        
        elif cmd == "status":
            return {
                "type": "status",
                "message": self.format_status_line()
            }
        
        elif cmd == "history":
            return {
                "type": "history",
                "commands": self.command_history[-10:]  # 最新10件
            }
        
        else:
            return {
                "type": "error",
                "message": f"不明なコマンド: {cmd}"
            }
    
    def _get_help_text(self) -> str:
        """ヘルプテキストを取得"""
        return """
📚 Claude++ ヘルプ

【基本的な使い方】
• ファイル編集: 「main.pyを編集して」
• テスト作成: 「テストを書いて」
• 保存: 「変更を保存して」
• 実行: 「実行して」

【コマンド】
• :mode [beginner|developer|focus] - 表示モード切替
• :status - 現在の状態を表示
• :history - コマンド履歴を表示
• :help - このヘルプを表示

【モード説明】
• beginner: Claude Code 90% + ステータス 10%
• developer: Claude Code 50% + コントロール 50%
• focus: Claude Code 100%（音声通知のみ）
"""
    
    def handle_error(self, error_msg: str) -> Dict[str, str]:
        """エラーを処理して日本語化"""
        self.status.last_error = error_msg
        translated, hint = ErrorTranslator.translate(error_msg)
        
        result = {
            "error": f"⚠️ {translated}",
            "original": error_msg
        }
        
        if hint:
            result["hint"] = f"💡 {hint}"
        
        return result
    
    def update_status(self, **kwargs):
        """ステータスを更新"""
        for key, value in kwargs.items():
            if hasattr(self.status, key):
                setattr(self.status, key, value)
    
    async def display_loop(self):
        """表示ループ（非同期）"""
        self.running = True
        
        # 初期表示
        if self.screen_controller:
            for line in self.format_welcome_message():
                self.screen_controller.send_to_control(line)
        
        # ステータス更新ループ
        while self.running:
            await asyncio.sleep(1)
            
            # 1分ごとにステータスラインを更新
            if int(time.time()) % 60 == 0:
                if self.screen_controller:
                    status_line = self.format_status_line()
                    # ステータスラインのみ更新（実装は簡略化）
                    self.screen_controller.send_to_control(f"\r{status_line}")
    
    def stop(self):
        """コントロールパネルを停止"""
        self.running = False