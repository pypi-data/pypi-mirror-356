"""
Claude Code統合エンジン
画面分割環境でClaude Codeを実行・管理する中核モジュール
"""

import asyncio
import os
import sys
import logging
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import queue

# プロジェクト内モジュール
from .screen_controller import ScreenController, DisplayMode
from .control_panel import ControlPanel
from .input_router import InputRouter
from .error_handler import get_error_handler
from .notifications import NotificationSystem

logger = logging.getLogger(__name__)


class ClaudeIntegration:
    """Claude Code統合エンジン"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.running = False
        
        # エラーハンドラー
        self.error_handler = get_error_handler()
        
        # コンポーネント初期化
        # PIDを取得して渡す
        self.pid = os.getpid()
        self.screen_controller = ScreenController(pid=self.pid, config=self.config)
        self.control_panel = ControlPanel(self.screen_controller)
        self.input_router = InputRouter()
        
        # Claude Codeプロセス
        self.claude_process = None
        
        # 通信用キュー
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        
        # スレッド
        self.input_thread = None
        self.output_thread = None
        self.monitor_thread = None
        
        # 既存機能との統合
        self.auto_yes_enabled = config.get('auto_yes', {}).get('enabled', True)
        self.auto_save_enabled = config.get('transparent_git', {}).get('enabled', True)
        self.auto_save_interval = config.get('transparent_git', {}).get('auto_save_interval', 30)
        
        # 自動保存タイマー
        self.last_save_time = time.time()
        
        # Phase 2.6.1.1: 通知システムと状態監視
        self.notification_system = NotificationSystem()
        self.state_monitor = None
        self.cursor_enhancer = None
    
    def start(self) -> bool:
        """統合セッションを開始"""
        logger.info("Claude++ 統合セッションを開始します")
        
        try:
            # 画面分割を開始
            if not self.screen_controller.start_session():
                error = Exception("画面分割の開始に失敗しました")
                # エラーハンドラーは非同期なので、ここでは同期処理で対応
                logger.error("画面分割の開始に失敗しました")
                return False
            
            time.sleep(2)  # tmuxセッションが安定するまで待機
            
            # Claude Codeを起動
            if not self._start_claude_code():
                logger.error("Claude Codeの起動に失敗しました")
                self.screen_controller.stop_session()
                return False
            
            # Phase 2.6.1.1: 通知システムと状態監視を初期化
            self._initialize_notification_system()
            
            # コントロールパネルの初期UI表示
            self._show_welcome_ui()
            
            # 各種スレッドを開始
            self.running = True
            self._start_threads()
            
            logger.info("統合セッションが正常に開始されました")
            return True
            
        except Exception as e:
            logger.error(f"統合セッション開始エラー: {e}")
            # 非同期エラーハンドラーは呼べないので、同期的にクリーンアップ
            self._cleanup_on_error()
            return False
    
    def _cleanup_on_error(self):
        """エラー時のクリーンアップ"""
        try:
            if self.screen_controller:
                self.screen_controller.stop_session()
            self.running = False
        except Exception as e:
            logger.error(f"クリーンアップエラー: {e}")
    
    def _start_claude_code(self) -> bool:
        """Claude Codeを起動"""
        try:
            # Claude Codeコマンドを構築
            claude_cmd = self._build_claude_command()
            
            # コマンドの存在確認
            # PATH=... で始まる場合は実際のコマンドを抽出
            if "PATH=" in claude_cmd and " " in claude_cmd:
                # PATH='...' command の形式から command を抽出
                cmd_parts = claude_cmd.split()
                for i, part in enumerate(cmd_parts):
                    if not part.startswith("PATH=") and not part.startswith("'"):
                        base_cmd = part
                        break
                else:
                    base_cmd = cmd_parts[-1]
            else:
                base_cmd = claude_cmd.split()[0]
            
            if not self._check_command_exists(base_cmd):
                logger.error(f"コマンドが見つかりません: PATH='{os.environ.get('PATH', '')}'")
                logger.error(f"Claude Codeの起動に失敗しました")
                return False
            
            # 上部ペインでClaude Codeを起動
            success = self.screen_controller.send_to_claude(claude_cmd)
            
            if success:
                logger.info(f"Claude Codeを起動しました: {claude_cmd}")
                # Claude起動を待つ
                time.sleep(3)
                
                # 起動確認のみ（コントロールパネルアプリが別途起動される）
                logger.info("Claude Code起動完了")
                return True
            else:
                logger.error("Claude Codeの起動コマンド送信に失敗")
                self.screen_controller.send_to_control(
                    "❌ エラー: Claude Codeの起動に失敗しました。\n"
                    "   もう一度お試しください。"
                )
                return False
                
        except Exception as e:
            logger.error(f"Claude Code起動エラー: {e}")
            return False
    
    def _check_command_exists(self, command: str) -> bool:
        """コマンドの存在確認"""
        try:
            import os
            # 完全パスの場合は直接チェック
            if os.path.isabs(command):
                return os.path.isfile(command) and os.access(command, os.X_OK)
            
            # 相対パスの場合のみwhichを使用
            import subprocess
            result = subprocess.run(
                ['which', command], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"コマンド存在確認エラー: {e}")
            return False
    
    def _build_claude_command(self) -> str:
        """Claude Codeコマンドを構築"""
        # 設定からコマンドを取得（claude_codeまたはclaude設定）
        base_cmd = (self.config.get('claude_code', {}).get('command') or 
                   self.config.get('claude', {}).get('command') or 
                   '/Users/harry/.nodebrew/current/bin/claude')
        
        # Auto_ClaudeCodeラッパーを完全に回避
        if base_cmd == 'claude':
            base_cmd = '/Users/harry/.nodebrew/current/bin/claude'
        
        # PATH環境変数制御付きでコマンドを実行
        cleaned_path = self._get_cleaned_path()
        
        # Phase 2.5.1: インタラクティブモードでは引数なしで起動
        # PATH環境変数をクリーンアップして実行
        return f"PATH='{cleaned_path}' {base_cmd}"
    
    def _get_cleaned_path(self) -> str:
        """Claude CLI実行に必要なPATHを構築"""
        current_path = os.environ.get('PATH', '')
        path_parts = current_path.split(':')
        
        # Claude CLIのbinディレクトリは必須
        auto_claude_bin = "/Users/harry/Dropbox/Tool_Development/Auto_ClaudeCode/bin"
        
        # PATHにClaude CLIが含まれているかチェック
        if auto_claude_bin not in path_parts:
            # Claude CLIが見つからない場合は追加
            path_parts.append(auto_claude_bin)
            logger.info(f"Claude CLI実行用PATHに追加: {auto_claude_bin}")
        
        cleaned_path = ':'.join(path_parts)
        logger.debug(f"Claude実行用PATH構築完了")
        
        return cleaned_path
    
    def _start_threads(self):
        """各種監視・処理スレッドを開始"""
        # 入力処理スレッド
        self.input_thread = threading.Thread(target=self._input_loop)
        self.input_thread.daemon = True
        self.input_thread.start()
        
        # 出力監視スレッド
        self.output_thread = threading.Thread(target=self._output_monitor_loop)
        self.output_thread.daemon = True
        self.output_thread.start()
        
        # 自動保存スレッド
        if self.auto_save_enabled:
            self.monitor_thread = threading.Thread(target=self._auto_save_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
        
        logger.debug("すべての監視スレッドを開始しました")
    
    def _input_loop(self):
        """入力処理ループ（コントロールパネルアプリが独自に処理するので最小限）"""
        while self.running:
            try:
                # 定期的な監視のみ（実際の入力処理はコントロールパネルアプリが行う）
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"入力処理エラー: {e}")
    
    def _process_user_input(self, user_input: str):
        """ユーザー入力を処理"""
        logger.debug(f"ユーザー入力: {user_input}")
        
        # コントロールパネルで処理
        panel_result = self.control_panel.process_input(user_input)
        
        if panel_result["type"] == "claude_command":
            # InputRouterで解析
            routing_result = self.input_router.route_input(user_input)
            
            # Claude Codeに転送（自動確認機能付き）
            claude_cmd = routing_result["claude_command"]
            
            # ファイル操作の場合は自動確認機能を使用
            if routing_result["analysis"].get("type") == "file_operation":
                logger.debug("ファイル操作を検出 - 自動確認機能を使用")
                self.screen_controller.send_user_input_with_auto_confirm(claude_cmd)
            else:
                # 通常のコマンドは従来通り
                self.screen_controller.send_to_claude(claude_cmd)
            
            # ステータス更新
            if routing_result["analysis"].get("target"):
                self.control_panel.update_status(
                    working_on=routing_result["analysis"]["target"],
                    mode="作業中"
                )
        
        elif panel_result["type"] == "mode_change":
            # モード切り替え
            mode_map = {
                "beginner": DisplayMode.BEGINNER,
                "developer": DisplayMode.DEVELOPER,
                "focus": DisplayMode.FOCUS
            }
            new_mode = mode_map.get(panel_result["mode"])
            if new_mode:
                self.screen_controller.switch_mode(new_mode)
                self.screen_controller.send_to_control(
                    f"✅ {panel_result['message']}"
                )
        
        elif panel_result["type"] == "help":
            # ヘルプ表示
            self.screen_controller.send_to_control(panel_result["message"])
    
    def _output_monitor_loop(self):
        """Claude Code出力監視ループ"""
        last_output = ""
        
        while self.running:
            try:
                # Claude Codeの出力をキャプチャ
                current_output = self.screen_controller.capture_claude_output()
                
                if current_output and current_output != last_output:
                    # 新しい出力を検出
                    new_lines = self._extract_new_lines(last_output, current_output)
                    
                    for line in new_lines:
                        self._process_claude_output(line)
                    
                    # 自動確認プロンプトをチェック
                    if self.auto_yes_enabled:
                        self._check_auto_confirmation(current_output)
                    
                    last_output = current_output
                
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"出力監視エラー: {e}")
    
    def _check_auto_confirmation(self, output: str):
        """確認プロンプトの自動処理"""
        if not output:
            return
        
        # 確認プロンプトのパターンを検出
        confirmation_patterns = [
            "Do you want to create",
            "Do you want to edit",
            "Do you want to delete",
            "❯ 1. Yes",
        ]
        
        has_confirmation = any(pattern in output for pattern in confirmation_patterns)
        
        if has_confirmation:
            logger.debug("確認プロンプトを検出 - 自動確認を実行")
            # screen_controllerの自動確認メソッドを使用
            if hasattr(self.screen_controller, 'check_and_handle_prompts'):
                success = self.screen_controller.check_and_handle_prompts()
                if success:
                    logger.debug("自動確認処理が完了しました")
                    # コントロールパネルに通知
                    if hasattr(self.screen_controller, 'send_to_control'):
                        self.screen_controller.send_to_control("🤖 確認プロンプトに自動応答しました")
                else:
                    logger.warning("自動確認処理に失敗しました")
    
    def _extract_new_lines(self, old_output: str, new_output: str) -> list:
        """新しい出力行を抽出"""
        old_lines = old_output.split('\n') if old_output else []
        new_lines = new_output.split('\n') if new_output else []
        
        # 新しい行のみを抽出
        if len(new_lines) > len(old_lines):
            return new_lines[len(old_lines):]
        return []
    
    def _process_claude_output(self, line: str):
        """Claude Codeの出力行を処理"""
        # 重複実装削除: Auto-Yes機能は engines/auto_yes.py に一本化
        # これにより daemon.py の沈黙検知システムとの協調が正常に動作
        
        # エラー検出のみ残す
        if "error:" in line.lower() or "exception" in line.lower():
            error_info = self.control_panel.handle_error(line)
            self.screen_controller.send_to_control(error_info["error"])
            if "hint" in error_info:
                self.screen_controller.send_to_control(error_info["hint"])
        
        # ファイル操作検出
        if "created" in line.lower() or "modified" in line.lower():
            self.screen_controller.send_to_control(f"📝 {line}")
    
    def _auto_save_loop(self):
        """自動保存ループ"""
        while self.running:
            try:
                current_time = time.time()
                elapsed = current_time - self.last_save_time
                
                # 30分経過したら自動保存
                if elapsed >= self.auto_save_interval * 60:
                    self._perform_auto_save()
                    self.last_save_time = current_time
                
                # 1分ごとにチェック
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"自動保存エラー: {e}")
    
    def _perform_auto_save(self):
        """自動保存を実行"""
        logger.debug("自動保存を実行します")
        
        # Git操作（既存のgit_proエンジンと連携予定）
        self.screen_controller.send_to_control("💾 作業を自動保存中...")
        
        # TODO: git_pro.pyとの統合
        # 現在は通知のみ
        time.sleep(2)
        self.screen_controller.send_to_control("✅ 自動保存が完了しました")
        self.control_panel.reset_auto_save_timer()
    
    def _show_welcome_ui(self):
        """ウェルカムUIを表示（コントロールパネルアプリが起動するので最小限に）"""
        logger.info("コントロールパネルアプリが起動しています")
    
    def stop(self):
        """統合セッションを停止"""
        logger.info("統合セッションを停止します")
        
        self.running = False
        
        # 通知システムの停止処理（新しい同期システムは特別な停止処理不要）
        pass
        
        # スレッドの終了を待つ
        if self.input_thread:
            self.input_thread.join(timeout=2)
        if self.output_thread:
            self.output_thread.join(timeout=2)
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        # 画面分割セッションを停止
        self.screen_controller.stop_session()
        
        logger.info("統合セッションが停止しました")
    
    def _initialize_notification_system(self):
        """通知システムと状態監視を初期化（Phase 2.6.1.1）"""
        try:
            # 同期通知システム初期化
            self.notification_system.initialize(self.config)
            
            # システム準備完了通知（起動時）
            self.notification_system.success(
                "🎯 Claude++ システム準備完了",
                "Claude Codeの起動が完了しました。開発を開始できます。"
            )
            
        except Exception as e:
            logger.error(f"通知システム初期化エラー: {e}")
            # 通知システムが失敗しても全体は継続