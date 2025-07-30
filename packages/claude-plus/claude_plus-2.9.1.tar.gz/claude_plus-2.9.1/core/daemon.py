#!/usr/bin/env python3
"""
Claude++ System - Main Daemon Process
Core orchestrator that manages all subprocess interactions and automations.
"""

import asyncio
import os
import sys
import signal
import logging
import json
import pty
import subprocess
import threading
import time
from pathlib import Path
import yaml
from typing import Dict, List, Optional, Callable, Any
from .notifications import NotificationSystem, NotificationType
from .env_manager import env_manager, get_environment, is_development, is_production
# Auto-Yes エンジンのインポート
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from engines.auto_yes import AutoYesEngine

# 通知はシンプルに状態ファイル経由で管理画面に送信


class RateLimitingFilter(logging.Filter):
    """Rate limiting filter for log messages to prevent spam."""
    
    def __init__(self, rate_limit_seconds=120):  # 60秒→120秒に延長
        super().__init__()
        self.rate_limit = rate_limit_seconds
        self.last_logged = {}
    
    def filter(self, record):
        """Filter log records based on rate limiting."""
        current_time = time.time()
        message_key = f"{record.levelname}:{record.getMessage()[:50]}"  # First 50 chars as key
        
        # Always allow ERROR and WARNING levels
        if record.levelno >= logging.WARNING:
            return True
        
        # Rate limit INFO and DEBUG messages
        if message_key in self.last_logged:
            if current_time - self.last_logged[message_key] < self.rate_limit:
                return False
        
        self.last_logged[message_key] = current_time
        return True


class ClaudePlusDaemon:
    """Main daemon process that orchestrates all Claude++ functionality."""
    
    def __init__(self, config_path: str = None, split_screen: bool = None):
        # 環境管理システムの統合
        self.environment = get_environment()
        self.config_path = config_path or self._find_config()
        self.config = self._load_config()
        self.logger = self._setup_logging()
        
        # split_screen の自動判定（統一アプローチ）
        if split_screen is None:
            # 設定ファイルまたは環境変数から判定
            self.split_screen = self.config.get('ui', {}).get('split_screen', True)
        else:
            self.split_screen = split_screen
        
        # デバッグ用ログ
        self.logger.debug(f"split_screen param: {split_screen}, config value: {self.config.get('ui', {}).get('split_screen', True)}, final value: {self.split_screen}")
        
        # 環境情報のログ出力
        if is_development():
            self.logger.info(f"🔧 開発環境で起動中 (env: {self.environment}, split_screen: {self.split_screen})")
        else:
            self.logger.info(f"🚀 本番環境で起動中 (env: {self.environment}, split_screen: {self.split_screen})")
        
        # Process management
        self.claude_process = None
        self.master_fd = None
        self.slave_fd = None
        self.running = False
        
        # Phase 2改善: 起動時間を記録（誤通知防止用）
        self.start_time = time.time()
        
        # 起動段階の状態管理
        self.startup_phase = "initializing"  # initializing -> ready -> working
        self.is_system_ready = False  # システム準備完了フラグ
        self.has_started_work = False  # 実際の作業開始フラグ
        
        # 通知システムは状態ファイル経由で管理画面に送信
        
        # Notification system (new sync design)
        self.notification_system = NotificationSystem()
        self.notification_system.initialize(self.config)
        
        # Engine instances
        self.engines = {}
        self.pattern_matchers = []
        self.notification_handlers = []
        
        # Auto-Yes エンジンの登録と初期化
        try:
            self.auto_yes_engine = AutoYesEngine()
            # パターンの初期化は同期的に実行
            self.auto_yes_engine.patterns = self.auto_yes_engine._get_default_patterns()
            self.auto_yes_engine._compile_patterns()
            self.auto_yes_engine.register_with_daemon(self)  # パターンマッチャーとして登録
            self.logger.info("✅ Auto-Yes エンジンを登録しました")
        except Exception as e:
            self.logger.error(f"❌ Auto-Yes エンジンの登録に失敗: {e}")
        
        # Async event loop
        self.loop = None
        self.reader_task = None
        
        # Phase 2.5.1: Split screen mode
        # self.split_screen は既に上で設定済み
        self.claude_integration = None
        
        # Signal handling
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # PIDベースのディレクトリとファイルパス設定
        self.pid = os.getpid()
        self.pid_dir = Path(f"/tmp/claude_plus_{self.pid}")
        self.pid_dir.mkdir(exist_ok=True)
        
        # Dashboard state sharing
        self.state_file = self.pid_dir / "state.json"
        self.dashboard_state = {
            "system_status": {
                "auto_save": True,
                "notifications": True,
                "auto_confirm": True,
                "split_screen": self.split_screen
            },
            "work_status": {
                "current_action": "初期化中",
                "working_directory": os.getcwd(),
                "start_time": time.time()
            },
            "statistics": {
                "files_edited": 0,
                "commands_executed": 0,
                "errors_resolved": 0,
                "git_commits": 0
            },
            "notification": {
                "message": None,
                "time": None
            }
        }
        self._save_dashboard_state()
        
    def _find_config(self) -> str:
        """Find configuration file in standard locations."""
        candidates = [
            "config/config.yaml",
            os.path.expanduser("~/.claude-plus/config.yaml"),
            "/etc/claude-plus/config.yaml"
        ]
        
        for path in candidates:
            if os.path.exists(path):
                return path
                
        # Create default config if none found
        default_path = "config/config.yaml"
        os.makedirs(os.path.dirname(default_path), exist_ok=True)
        return default_path
        
    def _load_config(self) -> Dict:
        """Load configuration using environment manager."""
        # 環境管理システムから設定を取得
        config = env_manager.get_config()
        
        if config:
            return config
        else:
            # フォールバック: 従来の設定読み込み
            try:
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            except FileNotFoundError:
                print(f"Warning: Config file not found: {self.config_path}, using defaults")
                return self._default_config()
            except yaml.YAMLError as e:
                print(f"Error: Error parsing config: {e}, using defaults")
                return self._default_config()
            
    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            'system': {'debug': True},
            'claude': {'command': 'claude', 'args': [], 'timeout': 300},
            'process': {'buffer_size': 8192, 'max_retries': 3},
            'logging': {'level': 'INFO', 'file': '/tmp/claude-plus.log'}
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Configure logging system."""
        logger = logging.getLogger('claude-plus')
        
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        logger.setLevel(level)
        
        # Only add handlers if none exist (prevent duplicates)
        if not logger.handlers:
            # Console handler - 通知システムとの競合を避けるため出力抑制
            console_handler = logging.StreamHandler(sys.stderr)
            # 表示崩れ完全防止のためERROR以上のみコンソール出力
            console_level = logging.ERROR  # WARNING/INFO/DEBUGログを完全抑制
            console_handler.setLevel(console_level)
            
            # Rate limiting filter for console output
            rate_filter = RateLimitingFilter(rate_limit_seconds=120)
            console_handler.addFilter(rate_filter)
            
            # シンプルなフォーマッター（左揃え対応）
            formatter = logging.Formatter('\n❌ %(levelname)s: %(message)s\n')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # File handler if specified (always add if requested)
        log_file = log_config.get('file')
        if log_file:
            # Check if file handler already exists
            has_file_handler = any(
                isinstance(h, logging.FileHandler) and h.baseFilename == log_file
                for h in logger.handlers
            )
            if not has_file_handler:
                file_handler = logging.FileHandler(log_file)
                # ファイルには詳細ログを記録
                file_level = getattr(logging, log_config.get('file_level', 'DEBUG'))
                file_handler.setLevel(file_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        
        # Prevent propagation to root logger to avoid duplicates
        logger.propagate = False
        
        return logger
        
    def register_engine(self, name: str, engine_instance):
        """Register an automation engine."""
        self.engines[name] = engine_instance
        self.logger.info(f"Registered engine: {name}")
        
    def register_pattern_matcher(self, matcher: Callable[[str], Optional[str]]):
        """Register a pattern matching function."""
        self.pattern_matchers.append(matcher)
        
    def register_notification_handler(self, handler: Callable[[str, str], None]):
        """Register a notification handler."""
        self.notification_handlers.append(handler)
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        
    async def start(self, claude_args: List[str] = None):
        """Start the daemon and Claude subprocess."""
        print("🚀 Claude++ を起動しています...")
        self.logger.info("Starting Claude++ Daemon")
        self.running = True
        self.loop = asyncio.get_event_loop()  # Store event loop for background threads
        
        try:
            # Initialize engines
            print("⚙️  エンジンを初期化中...")
            await self._log_activity("PROC", "エンジンを初期化中...")
            await self._initialize_engines()
            
            # Initialize notification system (sync design)
            print("🔔 通知システムを初期化中...")
            await self._log_activity("PROC", "通知システムを初期化中...")
            self.notification_system.initialize(self.config)
            
            # Handle task start (for Git branch creation)
            if claude_args:
                print("📋 タスクを開始中...")
                await self._log_activity("TASK", f"タスクを開始: {' '.join(claude_args)}")
            await self._handle_task_start(claude_args)
            
            # Phase 2.5.1: Use split screen mode if enabled
            if self.split_screen:
                print("🖥️  画面分割モードを準備中...")
                await self._log_activity("PROC", "画面分割モードを準備中...")
                self.update_dashboard_state("work_status", "current_action", "画面分割モード準備中")
                from .claude_integration import ClaudeIntegration
                self.claude_integration = ClaudeIntegration(self.config)
                
                # Create and manage tmux session - safe approach
                if not os.environ.get('TMUX'):
                    # Not in tmux - start integration normally and let screen_controller handle tmux
                    print("📺 tmux セッションを作成中...")
                    await self._log_activity("PROC", "tmux セッションを作成中...")
                    self.logger.info("Starting integration with tmux management...")
                    
                    if self.claude_integration.start():
                        print("✅ 画面分割セッションを開始しました")
                        await self._log_activity("OK  ", "画面分割セッションを開始しました")
                        self.logger.info("Started split screen session successfully")
                        
                        # Wait for integration to complete or be interrupted
                        try:
                            # Wait for the integration to be ready
                            print("⏳ Claude Code を準備中...")
                            await self._log_activity("PROC", "Claude Code を準備中...")
                            await asyncio.sleep(2)
                            
                            # Get the session name from screen controller
                            session_name = self.claude_integration.screen_controller.session_name
                            print("🔗 Claude Code に接続中...")
                            await self._log_activity("PROC", "Claude Code に接続中...")
                            self.logger.info(f"Attaching to tmux session: {session_name}")
                            
                            # Start real-time notification monitoring (Auto_ClaudeCode style)
                            print("🔍 リアルタイム監視を開始中...")
                            await self._log_activity("INFO", "リアルタイム監視を開始")
                            self._start_realtime_monitoring(session_name)
                            
                            # システム準備完了状態に移行
                            self.startup_phase = "ready"
                            self.is_system_ready = True
                            self.update_dashboard_state("work_status", "current_action", "システム準備完了 - 待機中")
                            
                            # システム準備完了通知を送信
                            self._trigger_system_ready_notification()
                            
                            # Show scroll guide to user
                            self._show_scroll_guide_message()
                            
                            # Attach to tmux session
                            # Use subprocess.call for better terminal handling
                            attach_cmd = ["tmux", "attach-session", "-t", session_name]
                            self.logger.info(f"Running: {' '.join(attach_cmd)}")
                            
                            # Set up proper terminal environment
                            env = os.environ.copy()
                            if 'TERM' not in env:
                                env['TERM'] = 'xterm-256color'
                            
                            # This will block until tmux exits
                            exit_code = subprocess.call(attach_cmd, env=env)
                            
                            # tmux終了時の通知判定（改善版）
                            # 正常終了（exit_code=0）かつ中断でない場合は完了通知
                            if exit_code == 0 and self.running:
                                self.logger.info("tmux session ended normally - sending completion notification")
                                self._trigger_completion_notification()
                            else:
                                self.logger.info(f"tmux session ended with code {exit_code} - skipping notification")
                            
                            # If we get here, tmux exited
                            self.logger.info("tmux session ended")
                            self.running = False
                        except KeyboardInterrupt:
                            self.logger.info("Received interrupt signal")
                            # 中断時の最終通知
                            self.logger.info("Sending final interruption notification...")
                            self._send_final_notification('interrupted')
                        finally:
                            self.claude_integration.stop()
                    else:
                        self.logger.error("Failed to start split screen session")
                        raise RuntimeError("Split screen initialization failed")
                    
                else:
                    # Already in tmux, start integration normally
                    if self.claude_integration.start():
                        self.logger.info("Started split screen session in existing tmux")
                        # In tmux, just keep running without attaching
                        await asyncio.sleep(2)
                        self.logger.info("Running in existing tmux session")
                        
                        # Keep running until interrupted
                        while self.running and self.claude_integration.running:
                            await asyncio.sleep(1)
                    else:
                        self.logger.error("Failed to start split screen session")
                        raise RuntimeError("Split screen initialization failed")
            else:
                # Traditional mode
                # Start Claude process
                await self._start_claude_process(claude_args or [])
                
                # Start main event loop
                await self._run_main_loop()
            
            # Handle task completion
            await self._handle_task_completion()
            
        except Exception as e:
            self.logger.error(f"Daemon error: {e}")
            raise
        finally:
            await self._cleanup()
            
    async def _initialize_engines(self):
        """Initialize all registered engines."""
        for name, engine in self.engines.items():
            if hasattr(engine, 'initialize'):
                try:
                    await engine.initialize(self.config)
                    self.logger.info(f"Initialized engine: {name}")
                except Exception as e:
                    self.logger.error(f"Failed to initialize {name}: {e}")
                    
    async def _start_claude_process(self, args: List[str]):
        """Start Claude CLI process with PTY."""
        claude_config = self.config.get('claude', {})
        command = claude_config.get('command', 'claude')
        default_args = claude_config.get('args', [])
        
        # Merge args
        full_args = [command] + default_args + args
        
        self.logger.info(f"Starting Claude process: {' '.join(full_args)}")
        
        # Create PTY
        self.master_fd, self.slave_fd = pty.openpty()
        
        # Start process
        self.claude_process = subprocess.Popen(
            full_args,
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            close_fds=True
        )
        
        # Close slave fd in parent process
        os.close(self.slave_fd)
        self.slave_fd = None
        
        self.logger.info(f"Claude process started with PID: {self.claude_process.pid}")
        
    async def _run_main_loop(self):
        """Main event loop for processing Claude output."""
        self.reader_task = asyncio.create_task(self._read_claude_output())
        
        try:
            # Wait for Claude process to complete
            while self.running and self.claude_process.poll() is None:
                await asyncio.sleep(0.1)
                
        except asyncio.CancelledError:
            self.logger.info("Main loop cancelled")
        finally:
            if self.reader_task:
                self.reader_task.cancel()
                
    async def _read_claude_output(self):
        """Read and process output from Claude process."""
        buffer_size = self.config.get('process', {}).get('buffer_size', 8192)
        
        try:
            while self.running:
                # Read data from PTY
                try:
                    data = os.read(self.master_fd, buffer_size)
                    if not data:
                        break
                        
                    text = data.decode('utf-8', errors='ignore')
                    
                    # Process through pattern matchers
                    response = await self._process_patterns(text)
                    if response:
                        await self._send_response(response)
                        
                    # Phase 2.5: デバッグ情報の日本語化
                    if self.config.get('system', {}).get('debug'):
                        debug_text = text.strip()
                        self.logger.debug(f"Claude出力: {debug_text}")
                        
                except OSError:
                    # PTY closed
                    break
                except Exception as e:
                    self.logger.error(f"Error reading Claude output: {e}")
                    
                await asyncio.sleep(0.01)  # Small delay to prevent busy waiting
                
        except asyncio.CancelledError:
            self.logger.info("Output reader cancelled")
            
    async def _process_patterns(self, text: str) -> Optional[str]:
        """Process text through all pattern matchers."""
        for matcher in self.pattern_matchers:
            try:
                response = matcher(text)
                if response:
                    self.logger.info(f"Pattern matched, responding: {response}")
                    return response
            except Exception as e:
                self.logger.error(f"Pattern matcher error: {e}")
                
        return None
        
    async def _send_response(self, response: str):
        """Send response to Claude process."""
        try:
            os.write(self.master_fd, (response + '\n').encode('utf-8'))
            
            # Send notifications
            for handler in self.notification_handlers:
                try:
                    handler("Auto Response", f"Sent: {response}")
                except Exception as e:
                    self.logger.error(f"Notification error: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error sending response: {e}")
            
    def shutdown(self):
        """Shutdown the daemon gracefully."""
        self.logger.info("Shutting down Claude++ Daemon")
        self.running = False
        
        # Phase 2.5.1: Shutdown split screen if active
        if self.claude_integration:
            # マウスホイールバインディング復元（最優先）
            if hasattr(self.claude_integration, 'screen_controller'):
                try:
                    self.claude_integration.screen_controller._restore_mouse_wheel_bindings()
                    self.logger.info("🖱️ マウスホイールバインディング復元完了")
                except Exception as e:
                    self.logger.error(f"マウスホイールバインディング復元エラー: {e}")
            
            # Phase 2.6.1.1: Cursor設定復元
            if hasattr(self.claude_integration, 'screen_controller') and \
               hasattr(self.claude_integration.screen_controller, 'is_cursor_environment') and \
               self.claude_integration.screen_controller.is_cursor_environment:
                try:
                    self.claude_integration.screen_controller.restore_cursor_settings_on_exit()
                    self.logger.info("🔄 Cursor設定の復元を完了しました")
                except Exception as e:
                    self.logger.error(f"Cursor設定復元エラー: {e}")
            
            self.claude_integration.stop()
        
        if self.reader_task:
            self.reader_task.cancel()
            
        if self.claude_process:
            try:
                self.claude_process.terminate()
                self.claude_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.claude_process.kill()
                
        if self.master_fd:
            os.close(self.master_fd)
        
        # PIDディレクトリのクリーンアップ
        try:
            import shutil
            if hasattr(self, 'pid_dir') and self.pid_dir.exists():
                shutil.rmtree(self.pid_dir)
                self.logger.info(f"PIDディレクトリをクリーンアップしました: {self.pid_dir}")
        except Exception as e:
            self.logger.error(f"PIDディレクトリのクリーンアップエラー: {e}")
            
    async def _handle_task_start(self, claude_args: List[str]):
        """Handle task start - trigger Git Pro engine for branch creation."""
        if not claude_args:
            return
            
        # Extract task description from arguments
        task_description = ' '.join(claude_args)
        
        # Call Git Pro engine if available
        git_pro = self.engines.get('git_pro')
        if git_pro and hasattr(git_pro, 'handle_task_start'):
            try:
                await git_pro.handle_task_start(task_description)
            except Exception as e:
                self.logger.error(f"Error in task start handling: {e}")
                
    async def _handle_task_completion(self):
        """Handle task completion - trigger Git Pro engine for commit/PR suggestions."""
        git_pro = self.engines.get('git_pro')
        if git_pro and hasattr(git_pro, 'handle_task_complete'):
            try:
                await git_pro.handle_task_complete()
            except Exception as e:
                self.logger.error(f"Error in task completion handling: {e}")
            
    def _show_scroll_guide_message(self):
        """Show scroll guide message before attaching to tmux (Cursor環境対応)"""
        # Cursor環境かどうかを確認
        is_cursor_env = hasattr(self, 'claude_integration') and \
                       hasattr(self.claude_integration, 'screen_controller') and \
                       getattr(self.claude_integration.screen_controller, 'is_cursor_environment', False)
        
        if is_cursor_env:
            self._show_cursor_startup_guide()
        else:
            self._show_standard_startup_guide()
        
        # 最適化されたユーザー読み取り時間
        # Cursor環境では読みやすいのでさらに短縮
        wait_time = 1.5 if is_cursor_env else 2.5
        time.sleep(wait_time)
    
    def _show_cursor_startup_guide(self):
        """Cursor環境用の起動ガイドを表示"""
        print("\n" + "="*75)
        print("🖥️  Claude++ Ready for Cursor IDE!")
        print("="*75)
        print("✨ マウスホイール・スクロール最適化モードで起動中...")
        print("🎯 readline入力履歴問題を完全解決！")
        print("")
        print("📜 Claude Codeスクロール操作:")
        print("")
        print("  🖱️  マウスホイール（最適化済み）:")
        print("    • マウスホイール上   : 自然なスクロールアップ")
        print("    • マウスホイール下   : 自然なスクロールダウン")
        print("    • 通常のテキスト選択・コピーが可能")
        print("    • 入力履歴の誤動作なし（問題解決済み）")
        print("")
        print("  ⌨️  キーボード操作:")
        print("    • PageUp/PageDown   : ページ単位スクロール")
        print("    • Shift + ↑/↓      : 行単位スクロール")
        print("    • Ctrl + U/D        : 半ページスクロール")
        print("    • g/G               : 最上部/最下部へ移動")
        print("    • Esc               : 通常入力に戻る")
        print("")
        print("🚀 5万行の履歴保存で快適な開発体験！")
        print("="*75)
        print("🔗 Connecting to Claude Code...")
        print("")
    
    def _show_standard_startup_guide(self):
        """標準ターミナル環境用の起動ガイドを表示"""
        print("\n" + "="*75)
        print("🎯 Claude++ Ready!")
        print("="*75)
        print("✨ マウスホイール・スクロール最適化モードで起動")
        print("🎯 readline入力履歴問題を完全解決！")
        print("")
        print("📜 Claude Codeスクロール操作:")
        print("")
        print("  🖱️  マウスホイール（最適化済み）:")
        print("    • マウスホイール上/下 : 自然なスクロール")
        print("    • 通常のマウス操作が可能")
        print("    • 入力履歴の誤動作なし（問題解決済み）")
        print("")
        print("  ⌨️  キーボード操作:")
        print("    • PageUp/PageDown   : ページ単位スクロール")
        print("    • Shift + ↑/↓      : 行単位スクロール")
        print("    • Ctrl + U/D        : 半ページスクロール")
        print("    • g/G               : 最上部/最下部へ移動")
        print("    • Esc               : 通常入力に戻る")
        print("")
        print("💡 5万行の履歴が保存されるので、長時間の作業も安心です！")
        print("="*75)
        print("Connecting to Claude Code...")
        print("")
    
    def _play_notification_sound(self, sound_type: str = 'success'):
        """終了時通知音再生（同期版）"""
        try:
            # 新しい同期通知システムを使用
            if sound_type == 'success':
                self.notification_system.success(
                    "Claude++ セッション完了",
                    "すべての作業が正常に完了しました"
                )
            elif sound_type == 'warning':
                self.notification_system.warning(
                    "Claude++ セッション中断",
                    "セッションが中断されました"
                )
            else:
                self.notification_system.info(
                    "Claude++ セッション終了",
                    "セッションが終了しました"
                )
            
            self.logger.info(f"✅ {sound_type}通知を送信しました")
                
        except Exception as e:
            self.logger.error(f"通知音再生エラー: {e}")
    
    def _send_final_notification(self, session_type: str = 'normal'):
        """最終通知送信（同期版）"""
        try:
            self.logger.info("🔔 最終通知を送信中...")
            
            # 通知システムで統一された方法で送信
            if session_type == 'interrupted':
                self.notification_system.warning(
                    "Claude++ セッション中断",
                    "セッションがユーザーによって中断されました\n設定やファイルは安全に保存されています"
                )
            else:
                self.notification_system.success(
                    "Claude++ セッション完了",
                    "すべての作業が正常に完了しました\n設定が復元され、変更内容が保存されています"
                )
            
            # 最適化された通知送信待機時間
            time.sleep(0.5)  # 通知送信待機短縮
            self.logger.info("✅ 最終通知送信完了")
            
        except Exception as e:
            self.logger.error(f"最終通知送信エラー: {e}")

    def _start_realtime_monitoring(self, session_name: str):
        """Start real-time monitoring of Claude Code output in tmux (Auto_ClaudeCode style)"""
        try:
            self.logger.info("🔍 Starting real-time notification monitoring...")
            
            # Start monitoring in background thread
            monitor_thread = threading.Thread(
                target=self._monitor_claude_output,
                args=(session_name,),
                daemon=True
            )
            monitor_thread.start()
            
            self.logger.info("✅ Real-time monitoring started")
            
        except Exception as e:
            self.logger.error(f"Failed to start real-time monitoring: {e}")
    
    def _monitor_claude_output(self, session_name: str):
        """Monitor Claude Code using tmux silence monitoring - Professional One-Shot Notification Pattern"""
        
        # プロのエンジニアアプローチ: Session-Based One-Shot Notification Pattern
        # 繰り返し通知問題を根本的に解決する業界標準手法
        
        startup_time = time.time()
        startup_grace_period = 30  # 起動後30秒は通知を抑制
        silence_threshold = 4      # 4秒の沈黙で完了通知
        last_notification_time = 0
        notification_cooldown = 8  # 8秒のクールダウン
        
        # 🔑 Professional Pattern: Session State Management
        is_completion_notified = False  # ワンショット通知制御フラグ
        session_id = f"{session_name}_{int(startup_time)}"  # セッション識別子
        
        last_output = ""
        last_activity_time = time.time()
        check_interval = 1  # 1秒間隔でチェック（rate limiting filterで出力制御済み）
        
        self.logger.info(f"🔍 Professional One-Shot Notification Pattern started for session: {session_id}")
        
        # ユーザー入力を求めるパターン（即座に通知が必要）
        urgent_patterns = [
            "Do you want",
            "Would you like", 
            "Continue?",
            "[Y/n]",
            "? (Y/n)",
            "Proceed",
            "Error:",
            "Failed", 
            "Exception",
            "確認してください",
            "エラー"
        ]
        
        # 完了を示すパターン（Claude Codeが明示的に完了を伝える場合）
        completion_patterns = [
            "Task completed",
            "Successfully completed",
            "Done!",
            "Finished",
            "All done",
            "作業完了",
            "完了しました",
            "終了しました",
            "成功しました"
        ]
        
        try:
            while self.running:
                try:
                    current_time = time.time()
                    
                    # 起動後の猶予期間チェック（誤通知防止）
                    time_since_daemon_startup = current_time - self.start_time
                    if time_since_daemon_startup < startup_grace_period:
                        time.sleep(check_interval)
                        continue
                    
                    # tmuxペインの出力をキャプチャ
                    result = subprocess.run(
                        ['tmux', 'capture-pane', '-t', f'{session_name}:0.0', '-p'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        current_output = result.stdout
                        
                        # 出力の変化を検知
                        if current_output != last_output:
                            # 🔄 Activity Reset Mechanism: 新しい活動 = 完了状態リセット
                            new_content = current_output[len(last_output):]
                            last_output = current_output
                            last_activity_time = current_time
                            
                            # 実際の作業開始を検知（ユーザーの入力があった場合）
                            if self.is_system_ready and not self.has_started_work:
                                # ユーザーの実際の入力・作業を検知
                                if self._is_user_activity(new_content):
                                    self.has_started_work = True
                                    self.startup_phase = "working"
                                    self.logger.info("🔄 User activity detected - transitioned to working state")
                                else:
                                    # デバッグ用：何が検知されているかをログ出力
                                    if new_content.strip():
                                        self.logger.debug(f"🔍 Activity check: '{new_content[:100]}...' - not recognized as user activity")
                            
                            # プロの実装: 新しい活動で完了状態をリセット
                            if is_completion_notified:
                                is_completion_notified = False
                                self.logger.info("🔄 Activity detected - completion state reset")
                                
                            # ダッシュボードの作業状態を更新
                            self.update_dashboard_state("work_status", "current_action", "Claude Code 処理中...")
                            
                            # Auto-Yes エンジンの処理（最優先）
                            auto_yes_handled = False
                            for matcher in self.pattern_matchers:
                                try:
                                    response = matcher(new_content)
                                    if response is not None:
                                        self.logger.info(f"🤖 Auto-Yes エンジンが応答: '{response}'")
                                        # 実際の応答をClaude Codeに送信
                                        if hasattr(self, 'claude_integration') and self.claude_integration:
                                            self.claude_integration.screen_controller.send_to_claude(response)
                                            # 安全なログメッセージに変更（コマンド実行を防ぐ）
                                            self.logger.info(f"🤖 Auto-Yes: {response} を選択しました")
                                            # Phase 2.8: ダッシュボードにログ送信
                                            self._log_activity_sync("OK  ", f"Auto-Yes: {response} を選択")
                                            self.increment_statistic("commands_executed")
                                        auto_yes_handled = True
                                        break
                                except Exception as e:
                                    self.logger.error(f"Pattern matcher error: {e}")
                            
                            # 完了パターンの即座チェック（明示的な完了メッセージ）
                            if not auto_yes_handled and not is_completion_notified and self._check_completion_patterns(new_content, completion_patterns):
                                if current_time - last_notification_time >= notification_cooldown:
                                    self.logger.info("🎯 明示的な完了メッセージを検出！")
                                    self._trigger_completion_notification()
                                    is_completion_notified = True
                                    last_notification_time = current_time
                            
                            # 緊急パターン（ユーザー入力要求、エラー）の即座チェック
                            elif not auto_yes_handled and self._check_urgent_patterns(new_content, urgent_patterns):
                                if current_time - last_notification_time >= notification_cooldown:
                                    last_notification_time = current_time
                                    self.logger.info("🚨 Urgent notification sent (user input required)")
                                    
                                    # Coordination Pattern: Auto-Yesエンジンとの協調
                                    # Auto-Yesエンジンが500ms後に応答するため、1.5秒待機してから確認待ち通知
                                    def delayed_notification():
                                        time.sleep(1.5)  # Auto-Yes response time + buffer
                                        # Check if auto-yes handled it by looking for new activity
                                        threading.Thread(target=self._check_and_send_waiting_notification, 
                                                       args=(new_content, urgent_patterns), daemon=True).start()
                                    
                                    threading.Thread(target=delayed_notification, daemon=True).start()
                        
                        else:
                            # 沈黙検知：Claude Codeの動作停止 = 作業完了の可能性
                            silence_duration = current_time - last_activity_time
                            
                            # 🔑 One-Shot Notification Pattern: 未通知 AND 条件満足 AND 確認待ちでない AND 起動直後でない場合のみ通知
                            # grace periodは上で定義済み
                            time_since_startup = current_time - self.start_time
                            
                            if (not is_completion_notified and  # ← 重要: まだ通知していない
                                silence_duration >= silence_threshold and 
                                current_time - last_notification_time >= notification_cooldown and
                                time_since_startup >= startup_grace_period):  # ← 新規: 起動直後の通知を防止
                                
                                # 確認待ち状態チェック（誤った完了通知を防止）
                                waiting_indicators = [
                                    "do you want", "would you like", "continue?", "[y/n]", "? (y/n)",
                                    "proceed", "確認してください", "❯ 1. yes", "❯ 1. no"
                                ]
                                
                                current_lower = current_output.lower()
                                is_waiting_for_input = any(indicator in current_lower for indicator in waiting_indicators)
                                
                                if is_waiting_for_input:
                                    self.logger.info(f"⏳ 確認待ち状態を検出 - 完了通知をスキップ (silence: {silence_duration:.1f}s)")
                                else:
                                    # デバッグ情報を追加
                                    self.logger.info(f"🔍 完了通知条件を満たしました: silence={silence_duration:.1f}s, cooldown={current_time - last_notification_time:.1f}s")
                                    
                                    # 完了通知送信（一度だけ）
                                    self._trigger_completion_notification()
                                    is_completion_notified = True  # ← 重要: 通知済みフラグをセット
                                    last_notification_time = current_time
                                    self.logger.info(f"✅ One-shot completion notification sent (silence: {silence_duration:.1f}s, session: {session_id})")
                                    
                                    # ダッシュボードの状態を更新
                                    self.update_dashboard_state("work_status", "current_action", "作業完了 - 待機中")
                            
                            elif is_completion_notified and silence_duration >= silence_threshold:
                                # Rate-limited debug info: 通知済みのためスキップ
                                # 完全にデバッグログを無効化（表示崩れ防止）
                                pass  # if silence_duration % 60 < 1:  # Only log every 60 seconds (disabled)
                    
                except subprocess.TimeoutExpired:
                    self.logger.debug("tmux capture timeout")
                except subprocess.CalledProcessError as e:
                    self.logger.debug(f"tmux capture failed: {e}")
                except Exception as e:
                    self.logger.error(f"Monitoring error: {e}")
                
                time.sleep(check_interval)
                
        except Exception as e:
            self.logger.error(f"Monitor thread error: {e}")
    
    def _check_completion_patterns(self, text: str, completion_patterns: list) -> bool:
        """Check for completion patterns indicating task is done"""
        try:
            text_lower = text.lower()
            for pattern in completion_patterns:
                if pattern.lower() in text_lower:
                    self.logger.info(f"✅ Completion pattern detected: {pattern}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Pattern check error: {e}")
            return False
    
    def _check_urgent_patterns(self, text: str, urgent_patterns: list) -> bool:
        """Check for urgent patterns requiring immediate notification (user input, errors)"""
        try:
            text_lower = text.lower()
            
            for pattern in urgent_patterns:
                if pattern.lower() in text_lower:
                    # Determine notification type
                    if any(err in pattern.lower() for err in ["error", "failed", "exception", "エラー"]):
                        self._trigger_error_notification(pattern)
                        return True
                    else:
                        # Waiting patterns will be handled by coordination pattern
                        return True
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Urgent pattern checking error: {e}")
            return False
    
    def _is_user_activity(self, new_content: str) -> bool:
        """ユーザーの実際の作業活動を検知"""
        try:
            # ユーザーが実際に作業を開始したと判断できるパターン（拡張版）
            user_activity_patterns = [
                "> ",  # プロンプト表示
                "❯",   # 選択プロンプト
                "Task completed",
                "Successfully",
                "Created",
                "Modified", 
                "Deleted",
                "Writing",
                "Reading",
                "Running",
                "Executing",
                "Building",
                "Testing",
                "File",
                "Error",
                "Warning",
                # Claude Codeの実際の出力パターンを追加
                "I'll",
                "Let me",
                "I'm going to",
                "I need to",
                "I can see",
                "Looking at",
                "Here's what",
                "The file",
                "This code",
                "Based on",
                "It looks like",
                # ツール使用の検知
                "antml:function_calls",
                "antml:invoke",
                "Read",
                "Edit",
                "Write",
                "Bash",
                "Task",
                "Grep",
                "Glob",
                # ユーザー入力の痕跡
                "command to execute",
                "file to read",
                "pattern to search"
            ]
            
            # 起動時のシステムメッセージは作業活動から除外
            startup_messages = [
                "🇯🇵 Claude++ へようこそ！",
                "🚀 Claude++ を起動",
                "⚙️  エンジンを初期化",
                "🔔 通知システムを初期化",
                "🖥️  画面分割モードを準備",
                "📺 tmux セッションを作成",
                "✅ 画面分割セッション",
                "⏳ Claude Code を準備",
                "🔗 Claude Code に接続",
                "🔍 リアルタイム監視を開始",
                "🎯 Claude++ Ready"
            ]
            
            content_lower = new_content.lower()
            
            # 起動メッセージは除外
            for startup_msg in startup_messages:
                if startup_msg.lower() in content_lower:
                    return False
            
            # 実際のユーザー活動パターンをチェック
            for pattern in user_activity_patterns:
                if pattern.lower() in content_lower:
                    return True
                    
            return False
            
        except Exception as e:
            self.logger.debug(f"User activity detection error: {e}")
            return False
    
    def _check_and_send_waiting_notification(self, content: str, urgent_patterns: list):
        """Check if Auto-Yes handled the prompt, send waiting notification if still needed"""
        try:
            # Wait a bit more to ensure Auto-Yes has time to respond
            time.sleep(0.5)
            
            # Check current tmux output to see if Auto-Yes resolved the issue
            result = subprocess.run(
                ['tmux', 'capture-pane', '-t', f'{self.claude_integration.screen_controller.session_name}:0.0', '-p'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                current_output = result.stdout
                
                # Check if the output still contains waiting patterns
                # If Auto-Yes worked, the prompts should be gone
                text_lower = current_output.lower()
                still_waiting = False
                
                waiting_indicators = [
                    "do you want", "would you like", "continue?", "[y/n]", "? (y/n)",
                    "proceed", "確認してください"
                ]
                
                for indicator in waiting_indicators:
                    if indicator in text_lower:
                        still_waiting = True
                        break
                
                # Only send waiting notification if Auto-Yes didn't handle it
                if still_waiting:
                    for pattern in urgent_patterns:
                        if pattern.lower() in content.lower():
                            if not any(err in pattern.lower() for err in ["error", "failed", "exception", "エラー"]):
                                self._trigger_waiting_notification(pattern)
                            break
                    self.logger.info("📋 Waiting notification sent (Auto-Yes did not handle)")
                else:
                    self.logger.info("🤖 Auto-Yes handled the prompt - no waiting notification needed")
            
        except Exception as e:
            self.logger.error(f"Coordination pattern error: {e}")
            # Fallback: send waiting notification anyway
            for pattern in urgent_patterns:
                if pattern.lower() in content.lower():
                    if not any(err in pattern.lower() for err in ["error", "failed", "exception", "エラー"]):
                        self._trigger_waiting_notification(pattern)
                    break
    
    
    def _trigger_system_ready_notification(self):
        """システム準備完了通知を送信"""
        try:
            self.logger.info("🎯 システム準備完了通知を送信中...")
            
            # 1. 管理画面への通知（状態ファイル経由）- タイムスタンプ付き
            try:
                import time as time_module
                notification_time = time_module.time()
                self.update_dashboard_state("notification", "message", "🎯 Claude++ システム準備完了")
                self.update_dashboard_state("notification", "time", notification_time)
            except Exception as e:
                self.logger.warning(f"管理画面通知エラー: {e}")
            
            # 2. PC通知と音声通知（準備完了）
            from .notifications import ConsoleStrategy
            
            # コンソールストラテジーのみ一時的に無効化
            console_strategies = [s for s in self.notification_system.strategies if isinstance(s, ConsoleStrategy)]
            for strategy in console_strategies:
                self.notification_system.strategies.remove(strategy)
            
            # PC通知・音声通知を実行（準備完了メッセージ）
            result = self.notification_system.claude_code_complete(
                "🎯 Claude++ システム準備完了",
                "Claude Codeの起動が完了しました。開発を開始できます。"
            )
            
            # コンソールストラテジーを元に戻す
            for strategy in console_strategies:
                self.notification_system.strategies.append(strategy)
            
            self.logger.info(f"🎯 システム準備完了通知送信結果: {'成功' if result else '失敗'}")
        except Exception as e:
            self.logger.error(f"System ready notification error: {e}")

    def _trigger_completion_notification(self):
        """Trigger completion notification（同期版）"""
        try:
            # Phase 2改善: 起動段階に応じた通知の分岐
            current_time = time.time()
            activity_duration = current_time - self.start_time
            
            # 起動直後の場合は通知をスキップ
            if activity_duration < 30:  # 起動後30秒未満はスキップ
                self.logger.debug(f"🔇 起動直後のため完了通知をスキップ (活動時間: {activity_duration:.1f}秒)")
                return
                
            # 作業開始チェック（改善版）
            if not self.has_started_work:
                # システム準備完了後40秒経過で通知許可（より実用的）
                if self.is_system_ready and activity_duration > 40:  
                    self.logger.info(f"🎵 システム準備完了後40秒経過のため完了通知を許可")
                    # 遅延した作業開始フラグ設定
                    self.has_started_work = True
                    self.startup_phase = "working"
                else:
                    self.logger.info(f"🔇 実際の作業が始まっていないため完了通知をスキップ (startup_phase: {self.startup_phase}, is_system_ready: {self.is_system_ready}, duration: {activity_duration:.1f}s)")
                    return
            
            self.logger.info("🎵 完了通知を送信中...")
            
            # 1. 管理画面への通知と状態更新（状態ファイル経由）- タイムスタンプ付き
            try:
                import time as time_module
                notification_time = time_module.time()
                self.update_dashboard_state("notification", "message", "🎉 開発タスクが完了しました")
                self.update_dashboard_state("notification", "time", notification_time)
                # 作業状態も更新
                self.update_dashboard_state("work_status", "current_action", "🎉 開発タスク完了 - 待機中")
            except Exception as e:
                self.logger.warning(f"管理画面通知エラー: {e}")
            
            # 2. PC通知と音声通知（修正版：コンソールのみ無効化、PC・音声は有効維持）
            # NotificationSystemの各ストラテジーを個別に制御
            from .notifications import ConsoleStrategy
            
            # コンソールストラテジーのみ一時的に無効化
            console_strategies = [s for s in self.notification_system.strategies if isinstance(s, ConsoleStrategy)]
            for strategy in console_strategies:
                self.notification_system.strategies.remove(strategy)
            
            # PC通知・音声通知を実行（コンソール以外のストラテジーで）
            result = self.notification_system.claude_code_complete(
                "🎉 Claude Code 作業完了",
                "開発タスクが正常に完了しました。結果をご確認ください。"
            )
            
            # コンソールストラテジーを元に戻す
            for strategy in console_strategies:
                self.notification_system.strategies.append(strategy)
            
            # 完了通知送信完了
            self.logger.info(f"🎵 完了通知送信結果: {'成功' if result else '失敗'}")
        except Exception as e:
            self.logger.error(f"Completion notification error: {e}")
    
    def _trigger_waiting_notification(self, pattern: str):
        """Trigger waiting/confirmation notification（同期版）"""
        try:
            # 1. 管理画面への通知（状態ファイル経由）- タイムスタンプ付き
            try:
                import time as time_module
                notification_time = time_module.time()
                self.update_dashboard_state("notification", "message", f"🔔 ユーザー確認が必要です")
                self.update_dashboard_state("notification", "time", notification_time)
            except Exception as e:
                self.logger.warning(f"管理画面通知エラー: {e}")
            
            # 2. PC通知と音声通知（修正版：コンソールのみ無効化、PC・音声は有効維持）
            from .notifications import ConsoleStrategy
            
            # コンソールストラテジーのみ一時的に無効化
            console_strategies = [s for s in self.notification_system.strategies if isinstance(s, ConsoleStrategy)]
            for strategy in console_strategies:
                self.notification_system.strategies.remove(strategy)
            
            # PC通知・音声通知を実行
            self.notification_system.claude_code_waiting(
                "Claude Code 確認待ち",
                f"ユーザーの入力・確認が必要です: {pattern}"
            )
            
            # コンソールストラテジーを元に戻す
            for strategy in console_strategies:
                self.notification_system.strategies.append(strategy)
        except Exception as e:
            self.logger.error(f"Waiting notification error: {e}")
    
    def _trigger_error_notification(self, pattern: str):
        """Trigger error notification（同期版）"""
        try:
            # 1. 管理画面への通知（状態ファイル経由）- タイムスタンプ付き
            try:
                import time as time_module
                notification_time = time_module.time()
                self.update_dashboard_state("notification", "message", f"🔔 エラーが発生しました")
                self.update_dashboard_state("notification", "time", notification_time)
            except Exception as e:
                self.logger.warning(f"管理画面通知エラー: {e}")
            
            # 2. PC通知と音声通知（修正版：コンソールのみ無効化、PC・音声は有効維持）
            from .notifications import ConsoleStrategy
            
            # コンソールストラテジーのみ一時的に無効化
            console_strategies = [s for s in self.notification_system.strategies if isinstance(s, ConsoleStrategy)]
            for strategy in console_strategies:
                self.notification_system.strategies.remove(strategy)
            
            # PC通知・音声通知を実行
            self.notification_system.claude_code_error(
                "Claude Code エラー",
                f"エラーが発生しました: {pattern}"
            )
            
            # コンソールストラテジーを元に戻す
            for strategy in console_strategies:
                self.notification_system.strategies.append(strategy)
            
            # ダッシュボードの状態を更新
            self.update_dashboard_state("work_status", "current_action", f"エラー対応中: {pattern}")
            self.increment_statistic("errors_resolved")
            
        except Exception as e:
            self.logger.error(f"Error notification error: {e}")

    def _save_dashboard_state(self):
        """ダッシュボード用の状態をファイルに保存"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.dashboard_state, f, indent=2)
        except Exception as e:
            self.logger.debug(f"Dashboard state save error: {e}")
    
    def update_dashboard_state(self, category: str, key: str, value: Any):
        """ダッシュボードの状態を更新"""
        if category in self.dashboard_state and key in self.dashboard_state[category]:
            self.dashboard_state[category][key] = value
            self._save_dashboard_state()
    
    def increment_statistic(self, stat_name: str, amount: int = 1):
        """統計情報をインクリメント"""
        if stat_name in self.dashboard_state["statistics"]:
            self.dashboard_state["statistics"][stat_name] += amount
            self._save_dashboard_state()
    
    # Phase 2.8: ダッシュボードログ送信メソッド
    async def _log_activity(self, level: str, message: str, category: str = None):
        """
        アクティビティをダッシュボードに送信（非同期版）
        
        Args:
            level: ログレベル (INFO, PROC, GIT, TASK, OK, WARN, ERR, SAVE)
            message: ログメッセージ
            category: カテゴリ（オプション）
        """
        # 通常のログ出力
        if hasattr(self, 'logger'):
            self.logger.info(f"[{level}] {message}")
        
        # 状態ファイル経由で管理画面に送信済み
    
    def _log_activity_sync(self, level: str, message: str, category: str = None):
        """
        アクティビティをダッシュボードに送信（同期版）
        
        Args:
            level: ログレベル (INFO, PROC, GIT, TASK, OK, WARN, ERR, SAVE)
            message: ログメッセージ
            category: カテゴリ（オプション）
        """
        # 通常のログ出力
        if hasattr(self, 'logger'):
            self.logger.info(f"[{level}] {message}")
        
        # 状態ファイル経由で管理画面に送信済み

    async def _cleanup(self):
        """Clean up resources."""
        # Cleanup engines
        for name, engine in self.engines.items():
            if hasattr(engine, 'cleanup'):
                try:
                    await engine.cleanup()
                except Exception as e:
                    self.logger.error(f"Error cleaning up {name}: {e}")
                    
        self.logger.info("Cleanup completed")
    


async def main_async():
    """Async main entry point for daemon."""
    daemon = ClaudePlusDaemon()
    
    try:
        # Get args passed to claude
        claude_args = sys.argv[1:] if len(sys.argv) > 1 else []
        await daemon.start(claude_args)
    except KeyboardInterrupt:
        daemon.logger.info("Interrupted by user")
    except Exception as e:
        daemon.logger.error(f"Daemon failed: {e}")
        return 1
        
    return 0


def main():
    """統一メインエントリーポイント (Unified main entry point)."""
    # 環境の自動判定または明示的設定
    if 'CLAUDE_PLUS_ENV' not in os.environ:
        # 環境変数が設定されていない場合は自動判定
        pass  # get_environment() が自動判定する
    
    # 開発環境でも本番環境でも同じ動作に統一
    # 通知テストは明示的に要求された場合のみ実行
    return main_production()

def main_production():
    """本番環境用（通知テストなし）"""
    try:
        print("🚀 Claude++ を起動しています...")
        daemon = ClaudePlusDaemon()  # 自動設定判定
        print("⚙️  エンジンを初期化中...")
        claude_args = sys.argv[1:] if len(sys.argv) > 1 else []
        if claude_args:
            print("📋 タスクを開始中...")
        print("🖥️  画面分割モードを準備中...")
        return asyncio.run(daemon.start(claude_args))
    except KeyboardInterrupt:
        print("\n🛑 Claude++を終了しました")
        return 0
    except FileNotFoundError:
        print("❌ エラー: 'claude' コマンドが見つかりません")
        print("💡 Claude CLI がインストールされているか確認してください")
        return 1
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        daemon.logger.error(f"Production daemon failed: {e}")
        return 1

def main_with_notification_test():
    """開発環境用（通知テスト付き）"""
    daemon = ClaudePlusDaemon()  # 自動設定判定
    
    # 開発環境では常に通知テストを実行
    daemon.logger.info("🧪 Running notification system test...")
    try:
        # Quick notification test
        from .notifications import info, success, warning, error
        
        # 通知テストを目立つように表示
        print("\n" + "="*50)
        print("🔔 通知システムテスト開始")
        print("="*50)
        
        # 各種通知をテスト
        print("1️⃣ 情報通知テスト...")
        info("開発モード", "Claude++ Dev が起動しました")
        time.sleep(1)
        
        print("2️⃣ 成功通知テスト...")
        success("システム正常", "すべてのシステムが動作中です")
        time.sleep(1)
        
        print("3️⃣ 警告通知テスト...")
        warning("テスト警告", "これはテスト警告です")
        time.sleep(1)
        
        print("4️⃣ エラー通知テスト...")
        error("テストエラー", "これはテストエラーです（無視してください）")
        
        print("\n✅ 通知テスト完了")
        print("確認事項:")
        print("• 音が4回鳴りましたか？")
        print("• 通知が4つ表示されましたか？")
        print("• 継続音はありませんか？")
        print("="*50 + "\n")
        
        daemon.logger.info("✅ Notification test completed")
        time.sleep(2)  # ユーザーが確認できるように少し待つ
        
    except Exception as e:
        daemon.logger.warning(f"⚠️  Notification test failed: {e}")
        print(f"\n❌ 通知テスト失敗: {e}\n")
    
    try:
        # Get args passed to claude
        claude_args = sys.argv[1:] if len(sys.argv) > 1 else []
        return asyncio.run(daemon.start(claude_args))
    except KeyboardInterrupt:
        daemon.logger.info("Development session interrupted by user")
        return 0
    except Exception as e:
        daemon.logger.error(f"Development daemon failed: {e}")
        return 1

def main_dev():
    """Development entry point (後方互換性維持用)."""
    # 開発環境を明示的に設定
    os.environ['CLAUDE_PLUS_ENV'] = 'development'
    # 統一されたメインエントリーポイントを呼び出し
    return main()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))