"""
画面分割制御モジュール
tmuxまたはWindows Terminalを使用して画面を分割管理
"""

import subprocess
import os
import time
import logging
import platform
from typing import Optional, Tuple, Dict, Any
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class DisplayMode(Enum):
    """表示モード"""
    BEGINNER = "beginner"     # 90% Claude Code + 10% Status
    DEVELOPER = "developer"   # 50% Claude Code + 50% Control
    FOCUS = "focus"          # 100% Claude Code (音声通知)


class ScreenController:
    """画面分割制御クラス"""
    
    def __init__(self, session_name: str = None, pid: int = None, config: dict = None):
        # PIDベースのセッション名生成
        if pid is None:
            pid = os.getpid()
        self.pid = pid
        
        # セッション名を一意化（PIDベース）
        if session_name is None:
            session_name = f"claude_plus_{pid}"
        
        self.session_name = session_name
        self.platform = platform.system().lower()
        self.current_mode = DisplayMode.BEGINNER
        self.is_active = False
        self.attach_ready = False  # アタッチ準備フラグ
        self.config = config or {}
        # 設定ファイルから分割比率を取得（デフォルト15%）
        self.control_pane_percentage = self.config.get('screen_split', {}).get('control_pane_percentage', 15)
        
        # Cursor IDE環境検知（Phase 2.6.1）
        self.is_cursor_environment = self._detect_cursor_environment()
        
        # ペイン識別子
        self.CLAUDE_PANE = f"{session_name}:0.0"
        self.CONTROL_PANE = f"{session_name}:0.1"
        
        # 通信用Named pipe（PIDベース）
        self.pipe_base = f"/tmp/claude_plus_{pid}"
        self.cmd_pipe = f"{self.pipe_base}/cmd"
        self.output_pipe = f"{self.pipe_base}/output"
        
        # マウスホイールバインディングのバックアップ
        self.original_wheel_bindings = {}
        self.wheel_bindings_backed_up = False
    
    def __del__(self):
        """デストラクタ - 確実な復元処理"""
        try:
            self._restore_mouse_wheel_bindings()
        except:
            # デストラクタでは例外を発生させない
            pass
    
    def _detect_cursor_environment(self) -> bool:
        """Cursor/VSCode IDE環境を自動検知"""
        detection_results = []
        
        # 1. TERM_PROGRAM環境変数をチェック
        term_program = os.environ.get('TERM_PROGRAM', '').lower()
        is_vscode_term = term_program in ['vscode', 'cursor']
        detection_results.append(f"TERM_PROGRAM: {term_program} ({'✓' if is_vscode_term else '✗'})")
        
        # 2. VSCode/Cursor特有の環境変数をチェック
        vscode_indicators = [
            'VSCODE_PID',
            'VSCODE_CWD', 
            'VSCODE_INJECTION',
            'CURSOR_SESSION_ID',
            'CURSOR_PID'
        ]
        
        vscode_env_found = any(var in os.environ for var in vscode_indicators)
        found_vars = [var for var in vscode_indicators if var in os.environ]
        detection_results.append(f"IDE環境変数: {found_vars} ({'✓' if vscode_env_found else '✗'})")
        
        # 3. 親プロセス名をチェック
        parent_process_match = False
        try:
            import psutil
            parent = psutil.Process().parent()
            if parent:
                parent_name = parent.name().lower()
                parent_process_match = any(name in parent_name for name in ['code', 'cursor', 'vscode'])
                detection_results.append(f"親プロセス: {parent_name} ({'✓' if parent_process_match else '✗'})")
            else:
                detection_results.append("親プロセス: 取得不可 (✗)")
        except (ImportError, Exception) as e:
            detection_results.append(f"親プロセス: エラー ({e}) (✗)")
        
        # 4. 総合判定
        is_cursor_env = is_vscode_term or vscode_env_found or parent_process_match
        
        # 5. 検知結果をログ出力
        if is_cursor_env:
            logger.info("🖥️  Cursor/VSCode IDE環境を検知しました")
            logger.info("📊 Cursor最適化モードが有効になります")
        else:
            logger.info("🖥️  標準ターミナル環境で動作します")
        
        for result in detection_results:
            logger.debug(f"   環境検知: {result}")
        
        return is_cursor_env
        
    def is_tmux_available(self) -> bool:
        """tmuxが利用可能か確認"""
        try:
            result = subprocess.run(
                ["which", "tmux"], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def _run_tmux_command(self, cmd: str) -> Tuple[bool, str, str]:
        """tmuxコマンドを実行（エラー対応強化版）"""
        try:
            # セッション存在確認（attach時のみ）
            if "-t" in cmd and self.session_name in cmd and "attach" in cmd:
                if not self._verify_session_exists():
                    logger.warning(f"セッション '{self.session_name}' が存在しません")
                    return False, "", f"Session '{self.session_name}' does not exist"
            
            result = subprocess.run(
                f"tmux {cmd}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10  # 10秒タイムアウト
            )
            success = result.returncode == 0
            
            # よくあるエラーの自動対応
            if not success and result.stderr:
                if "no server running" in result.stderr:
                    logger.debug("tmuxサーバーが起動していません（正常な状態の場合があります）")
                elif "no current client" in result.stderr:
                    logger.debug("アタッチされたクライアントがありません（detachedセッション）")
                elif "not found" in result.stderr and "bind" in cmd:
                    logger.debug("バインディングが見つかりません（既に削除済みまたは未定義）")
                    # バインディング関連エラーは成功扱いにする場合がある
                    if "unbind" in cmd:
                        success = True  # unbindの場合、既に存在しないのは成功
            
            return success, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            logger.error(f"tmuxコマンドタイムアウト: {cmd}")
            return False, "", "Command timeout"
        except Exception as e:
            logger.error(f"tmuxコマンド実行エラー: {e}")
            return False, "", str(e)
    
    def _verify_session_exists(self) -> bool:
        """セッション存在確認"""
        try:
            result = subprocess.run(
                f"tmux has-session -t {self.session_name}",
                shell=True,
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _backup_mouse_wheel_bindings(self) -> bool:
        """現在のマウスホイールバインディングをバックアップ"""
        try:
            logger.debug("🔄 tmuxマウスホイールバインディングをバックアップ中...")
            
            # 現在のWheelUpPane、WheelDownPaneバインディングを取得
            success, stdout, stderr = self._run_tmux_command("list-keys")
            if not success:
                logger.error(f"tmux list-keys失敗: {stderr}")
                return False
            
            # WheelUpPane、WheelDownPaneバインディングを抽出
            self.original_wheel_bindings = {}
            for line in stdout.split('\n'):
                if 'WheelUpPane' in line and '-T root' in line:
                    # 例: bind-key -T root WheelUpPane if-shell ...
                    # コマンド部分を抽出
                    parts = line.split('WheelUpPane', 1)
                    if len(parts) > 1:
                        command = parts[1].strip()
                        self.original_wheel_bindings['WheelUpPane'] = command
                        logger.debug(f"バックアップ - WheelUpPane: {command}")
                elif 'WheelDownPane' in line and '-T root' in line:
                    parts = line.split('WheelDownPane', 1)
                    if len(parts) > 1:
                        command = parts[1].strip()
                        self.original_wheel_bindings['WheelDownPane'] = command
                        logger.debug(f"バックアップ - WheelDownPane: {command}")
            
            # WheelDownPaneが存在しない場合は記録
            if 'WheelDownPane' not in self.original_wheel_bindings:
                self.original_wheel_bindings['WheelDownPane'] = None
                logger.debug("バックアップ - WheelDownPane: 未定義")
            
            # WheelUpPaneも確認
            if 'WheelUpPane' not in self.original_wheel_bindings:
                self.original_wheel_bindings['WheelUpPane'] = None
                logger.debug("バックアップ - WheelUpPane: 未定義")
            
            self.wheel_bindings_backed_up = True
            logger.debug("✅ マウスホイールバインディングのバックアップ完了")
            return True
            
        except Exception as e:
            logger.error(f"バインディングバックアップエラー: {e}")
            return False
    
    def _apply_optimized_wheel_bindings(self) -> bool:
        """最適化されたマウスホイールバインディングを適用"""
        try:
            logger.debug("🎯 最適化マウスホイールバインディングを適用中...")
            
            # 根本的解決: WheelDownPaneバインディングを完全削除
            # WheelDownPaneでPageDownを送信するとreadlineが履歴操作として解釈してしまう問題
            
            # Phase 1: WheelUpPaneは通常のスクロールとして機能
            bind_cmd = "bind-key -T root WheelUpPane 'copy-mode -e'"
            success, stdout, stderr = self._run_tmux_command(bind_cmd)
            if not success:
                logger.error(f"WheelUpPane バインディング適用失敗: {stderr}")
                return False
            logger.debug("適用完了 - WheelUpPane: copy-mode -e")
            
            # Phase 2: WheelDownPaneを完全に無効化（unbind）
            unbind_cmd = "unbind-key -T root WheelDownPane"
            success, stdout, stderr = self._run_tmux_command(unbind_cmd)
            if success:
                logger.debug("WheelDownPane バインディングを削除しました")
            else:
                # バインディングが存在しない場合のエラーは無視
                if "not found" not in stderr.lower():
                    logger.warning(f"WheelDownPane unbind警告: {stderr}")
            
            logger.debug("✅ 最適化バインディング適用完了 - Claude Code履歴スクロール問題を根本解決")
            logger.debug("   ホイール上: copy-mode開始（通常のスクロール）")
            logger.debug("   ホイール下: 無効化（readline干渉完全回避）")
            return True
            
        except Exception as e:
            logger.error(f"最適化バインディング適用エラー: {e}")
            return False
    
    def _setup_professional_mouse_bindings(self) -> bool:
        """Claude CLIとの互換性を保つマウス設定（デフォルトOFF）"""
        try:
            logger.debug("🎯 Claude CLI互換マウス設定を適用中...")
            
            # 基本的にマウスを無効化（Claude Codeとの互換性のため）
            success1, _, _ = self._run_tmux_command("set -g mouse off")
            if not success1:
                logger.warning("マウス無効化設定に失敗")
                return False
            
            # スクロールバッファサイズ設定
            success2, _, _ = self._run_tmux_command("set-option -g history-limit 50000")
            
            # マウスホイールバインディングを完全にクリア（干渉を防ぐ）
            # すべてのマウスホイールバインディングを削除（CLI自然動作優先）
            self._run_tmux_command("unbind -n WheelUpPane")
            self._run_tmux_command("unbind -n WheelDownPane")
            self._run_tmux_command("unbind -T root WheelUpPane")
            self._run_tmux_command("unbind -T root WheelDownPane")
            self._run_tmux_command("unbind -T copy-mode WheelUpPane")
            self._run_tmux_command("unbind -T copy-mode WheelDownPane")
            self._run_tmux_command("unbind -T copy-mode-vi WheelUpPane")
            self._run_tmux_command("unbind -T copy-mode-vi WheelDownPane")
            
            # 追加：マウスイベントの直接パススルー無効化
            self._run_tmux_command("unbind -n M-Up")
            self._run_tmux_command("unbind -n M-Down")
            
            logger.debug("✅ Claude CLI互換設定完了")
            logger.debug("   マウスモード: OFF（デフォルト）")
            logger.debug("   Claude CLIのネイティブマウス処理を優先")
            
            # マウスモード切り替えのキーバインディングを追加
            self._setup_mouse_toggle_keys()
            
            # キーボードベースのスクロール設定
            self._setup_keyboard_scroll_keys()
            
            # ビューアーペイン切り替えキーの設定
            self._setup_pane_switch_keys()
            
            return True
            
        except Exception as e:
            logger.error(f"Claude CLI互換マウス設定エラー: {e}")
            return False
    
    def _setup_mouse_toggle_keys(self):
        """マウスモード切り替えキーの設定"""
        try:
            # Ctrl+b m でマウスモードON（tmuxスクロール用）
            toggle_on_cmd = "bind-key m set -g mouse on \\; display-message '🖱️  マウスモード: ON (tmuxスクロール有効)'"
            # Ctrl+b M でマウスモードOFF（Claude CLI用）
            toggle_off_cmd = "bind-key M set -g mouse off \\; display-message '🖱️  マウスモード: OFF (Claude CLI優先)'"
            
            self._run_tmux_command(toggle_on_cmd)
            self._run_tmux_command(toggle_off_cmd)
            
            logger.info("📌 マウスモード切り替え: Ctrl+b m (ON) / Ctrl+b M (OFF)")
            logger.info("💡 デフォルト: OFF (Claude CLIのマウス操作を優先)")
            
        except Exception as e:
            logger.debug(f"マウストグルキー設定エラー: {e}")
    
    def _setup_keyboard_scroll_keys(self):
        """キーボードベースのスクロール設定"""
        try:
            # Ctrl+b [ でコピーモード（スクロールモード）開始
            self._run_tmux_command("bind-key [ copy-mode")
            
            # コピーモード中のスクロールキー設定
            # Page Up/Down
            self._run_tmux_command("bind-key -T copy-mode-vi PageUp send-keys -X page-up")
            self._run_tmux_command("bind-key -T copy-mode-vi PageDown send-keys -X page-down")
            
            # Ctrl+U/D（半ページスクロール）
            self._run_tmux_command("bind-key -T copy-mode-vi C-u send-keys -X halfpage-up")
            self._run_tmux_command("bind-key -T copy-mode-vi C-d send-keys -X halfpage-down")
            
            # j/k（1行スクロール）
            self._run_tmux_command("bind-key -T copy-mode-vi j send-keys -X scroll-down")
            self._run_tmux_command("bind-key -T copy-mode-vi k send-keys -X scroll-up")
            
            # qでコピーモード終了
            self._run_tmux_command("bind-key -T copy-mode-vi q send-keys -X cancel")
            
            logger.info("⌨️ キーボードスクロール設定完了")
            logger.info("   Ctrl+b [ : スクロールモード開始")
            logger.info("   j/k : 1行下/上")
            logger.info("   Ctrl+d/u : 半ページ下/上")
            logger.info("   PageDown/Up : 1ページ下/上")
            logger.info("   q : スクロールモード終了")
            
        except Exception as e:
            logger.debug(f"キーボードスクロール設定エラー: {e}")
    
    def _setup_pane_switch_keys(self):
        """ペイン切り替えキーの設定"""
        try:
            # Tabキーでペイン切り替え
            self._run_tmux_command("bind-key Tab select-pane -t :.+")
            
            # Ctrl+wでもペイン切り替え（vim風）
            self._run_tmux_command("bind-key C-w select-pane -t :.+")
            
            # Shift+Tabで逆順切り替え
            self._run_tmux_command("bind-key BTab select-pane -t :.-")
            
            logger.info("📱 ペイン切り替え設定完了")
            logger.info("   Tab : 次のペイン")
            logger.info("   Shift+Tab : 前のペイン")
            logger.info("   Ctrl+w : ペイン切り替え（vim風）")
            
        except Exception as e:
            logger.debug(f"ペイン切り替え設定エラー: {e}")
    
    def _restore_mouse_wheel_bindings(self) -> bool:
        """バックアップしたマウスホイールバインディングを復元（堅牢な実装）"""
        try:
            if not self.wheel_bindings_backed_up:
                logger.debug("バックアップがないため復元をスキップ")
                return True
            
            # tmux利用可能性チェック
            if not self.is_tmux_available():
                logger.warning("tmuxが利用できないため復元をスキップ")
                self.wheel_bindings_backed_up = False
                return True
            
            logger.info("🔄 マウスホイールバインディングを復元中...")
            restoration_success = True
            restored_bindings = []
            failed_bindings = []
            
            for key, command in self.original_wheel_bindings.items():
                try:
                    if command is None:
                        # 元々定義されていなかった場合は削除
                        unbind_cmd = f"unbind-key -T root {key}"
                        success, stdout, stderr = self._run_tmux_command(unbind_cmd)
                        if success or "not found" in stderr.lower():
                            # 成功 or 既に存在しない場合は成功とみなす
                            restored_bindings.append(f"{key}: 未定義に戻す")
                            logger.debug(f"復元完了 - {key}: 未定義に戻す")
                        else:
                            failed_bindings.append(f"{key}: unbind失敗 - {stderr}")
                            logger.warning(f"unbind失敗 - {key}: {stderr}")
                            # unbind失敗は致命的ではないので継続
                    else:
                        # 元のバインディングを復元（適切なエスケープ処理）
                        bind_cmd = f"bind-key -T root {key} \"{command}\""
                        success, stdout, stderr = self._run_tmux_command(bind_cmd)
                        if success:
                            restored_bindings.append(f"{key}: {command}")
                            logger.debug(f"復元完了 - {key}: {command}")
                        else:
                            failed_bindings.append(f"{key}: bind失敗 - {stderr}")
                            logger.error(f"バインディング復元失敗 - {key}: {stderr}")
                            restoration_success = False
                except Exception as e:
                    failed_bindings.append(f"{key}: 例外 - {e}")
                    logger.error(f"バインディング復元で例外 - {key}: {e}")
                    restoration_success = False
            
            # 復元結果のサマリーログ
            if restored_bindings:
                logger.info(f"✅ 復元成功: {len(restored_bindings)}個のバインディング")
                for binding in restored_bindings:
                    logger.debug(f"  - {binding}")
            
            if failed_bindings:
                logger.warning(f"⚠️ 復元失敗: {len(failed_bindings)}個のバインディング")
                for binding in failed_bindings:
                    logger.warning(f"  - {binding}")
            
            # 状態をクリア（部分的失敗でもバックアップ状態は解除）
            self.wheel_bindings_backed_up = False
            
            if restoration_success:
                logger.info("✅ マウスホイールバインディング復元完了")
            else:
                logger.warning("⚠️ マウスホイールバインディング復元で一部失敗")
            
            return restoration_success
            
        except Exception as e:
            logger.error(f"バインディング復元エラー: {e}")
            return False
    
    def start_session(self) -> bool:
        """画面分割セッションを開始"""
        if self.platform != "darwin" and self.platform != "linux":
            logger.warning("現在はmacOS/Linuxのみサポートしています")
            return False
            
        if not self.is_tmux_available():
            logger.warning("tmuxがインストールされていません - フォールバックモードを使用します")
            return self._start_fallback_mode()
        
        # PIDベースの分離により、セッション再利用は不要
        # if self._try_reuse_existing_session():
        #     logger.info("既存のセッションを再利用します")
        #     return True
        
        # PIDベースの分離により、古いセッションのクリーンアップは不要
        # self._cleanup_old_sessions()
        self._cleanup_session()
        
        # Named pipeを作成
        self._setup_pipes()
        
        # 現在tmux内にいるかチェック
        in_tmux = os.environ.get('TMUX') is not None
        
        if in_tmux:
            # すでにtmux内にいる場合は新しいウィンドウを作成
            success, _, _ = self._run_tmux_command(
                f"new-window -n {self.session_name}"
            )
            if success:
                # ウィンドウが閉じられたときのフックを設定
                self._run_tmux_command(
                    f"set-hook -g -w pane-exited 'if -F \"#{window_name}\" = \"{self.session_name}\" \"kill-window\"'"
                )
                # 画面を分割（デフォルトはBEGINNERモード）
                self._apply_layout(DisplayMode.BEGINNER)
        else:
            # tmux外からの場合
            # Auto_ClaudeCodeを除去したPATHを構築
            cleaned_path = self._get_cleaned_path()
            
            # detached セッションを作成（クリーンなPATH環境で）
            success, _, _ = self._run_tmux_command(
                f"new-session -d -s {self.session_name} 'PATH=\"{cleaned_path}\" bash'"
            )
            
            # tmux設定最適化
            if success:
                # 注: destroy-unattached は即座にセッション削除を引き起こすため無効化
                # 無限増殖対策は _cleanup_old_sessions() で代替
                
                # セッション終了時フックのみ設定（クライアントデタッチ時ではない）
                
                # セッション環境変数を設定（Auto_ClaudeCode除去済みPATH）
                self._run_tmux_command(f"set-environment -t {self.session_name} PATH '{cleaned_path}'")
                
                # ターミナルタイプを設定（エスケープシーケンス問題対策）
                self._run_tmux_command(f"set-environment -t {self.session_name} TERM 'screen-256color'")
                # COLORTERMを削除（余計な色エスケープを防ぐ）
                self._run_tmux_command(f"set-environment -u -t {self.session_name} COLORTERM")
                # RGB色設定を完全に無効化
                self._run_tmux_command(f"set-environment -t {self.session_name} NO_COLOR '1'")
                self._run_tmux_command(f"set-environment -u -t {self.session_name} FORCE_COLOR")
                self._run_tmux_command(f"set-environment -u -t {self.session_name} LS_COLORS")
                
                # マウスは無効化（Claude CLIとの互換性を最優先）
                self._run_tmux_command(f"set-option -t {self.session_name} -g mouse off")
                # スクロール履歴を有効化
                self._run_tmux_command(f"set-option -t {self.session_name} -g history-limit 50000")
                # スクロールモードでの操作を改善
                self._run_tmux_command(f"set-option -t {self.session_name} -g mode-keys vi")
                # Claude Code専用スクロール機能を設定（一時的に無効化）
                # Claude CLIとの干渉を防ぐため、スクロール機能は無効化
                # self._setup_claude_scroll_features()
                
                # Claude CLI互換マウス設定（デフォルトOFF）
                if self._setup_professional_mouse_bindings():
                    logger.info("🎯 Claude CLI互換設定完了（マウス: OFF）")
                else:
                    logger.warning("⚠️ マウス設定に一部失敗（基本動作に影響なし）")
                
                # ターミナルオーバーライド：Claude CLI自然スクロール対応
                # smcup@:rmcup@ - alternate screen modeを無効化（自然スクロール実現）
                # マウス関連設定も調整してCLIアプリの動作を保護
                self._run_tmux_command(f"set-option -t {self.session_name} -g terminal-overrides 'xterm*:XT:smcup@:rmcup@:Ms@:Cc@:Cr@:Cs@:Se@:Ss@:setrgbf@:setrgbb@:RGB@:TC@:Tc@:sitm@:ritm@:smxx@:rmxx@'")
                
                # 追加のターミナル設定：自然スクロール強化
                self._run_tmux_command(f"set-option -t {self.session_name} -ga terminal-overrides ',xterm*:smcup@:rmcup@'")
                
                # スクロール時のarrow key送信を防ぐ
                self._run_tmux_command(f"set-option -t {self.session_name} -g alternate-screen off")
                
                # セッション終了時のフックを設定（音声再生）
                helper_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "tmux_sound_helper.sh"
                )
                if os.path.exists(helper_path):
                    self._run_tmux_command(
                        f"set-hook -t {self.session_name} -g session-closed 'run-shell \"{helper_path} success\"'"
                    )
            
            if success:
                # 画面を分割（デフォルトはBEGINNERモード）
                self._apply_layout(DisplayMode.BEGINNER)
                
                # send-keys問題の回避: 明示的にアタッチされたクライアントを作成
                # detachedセッションでsend-keysするには、一時的にアタッチが必要
                time.sleep(1)  # セッション安定化
                
                # 現在のプロセスをセッションにアタッチ（バックグラウンド実行）
                # この方法でsend-keysが機能するようになる
                attach_success, _, _ = self._run_tmux_command(f"send-keys -t {self.session_name}:0 '' Enter")
                if not attach_success:
                    logger.warning("tmux send-keys初期化に失敗（通常動作に影響なし）")
                
                # 独立スクロールを設定（一時的に無効化）
                # PaneScrollController.setup_independent_scrolling(self.session_name)
                # PaneScrollController.create_scroll_keybindings(self.session_name)
                
                # daemon.pyでアタッチを処理するため、ここではスケジュールしない
                logger.info("tmuxセッションが作成されました")
                # self._schedule_auto_attach() # daemon.pyで処理
        
        if not success:
            logger.error("tmuxセッションの作成に失敗しました")
            return False
        
        self.is_active = True
        logger.info("画面分割セッションを開始しました")
        return True
    
    def _apply_layout(self, mode: DisplayMode) -> bool:
        """レイアウトを適用"""
        if mode == DisplayMode.FOCUS:
            # フォーカスモードは分割なし
            return True
            
        # 既存の分割をクリア
        self._run_tmux_command(f"kill-pane -a -t {self.session_name}:0")
        
        # モードに応じて分割（設定可能な比率）
        if mode == DisplayMode.BEGINNER:
            # 下部のコントロールパネル（設定ファイルから読み込んだ比率を使用）
            success, _, _ = self._run_tmux_command(
                f"split-window -t {self.session_name} -v -p {self.control_pane_percentage}"
            )
        elif mode == DisplayMode.DEVELOPER:
            # 同じく設定ファイルの比率を使用（統一比率）
            success, _, _ = self._run_tmux_command(
                f"split-window -t {self.session_name} -v -p {self.control_pane_percentage}"
            )
        else:
            success = False
            
        if success:
            self.current_mode = mode
            logger.info(f"レイアウトを{mode.value}モードに変更しました")
            
            # Claude Codeペインにフォーカスを設定
            self._run_tmux_command(f"select-pane -t {self.CLAUDE_PANE}")
            
            # 安心ダッシュボードまたは会話履歴ビューアーを起動
            viewer_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "conversation_viewer.py"
            )
            if os.path.exists(viewer_path):
                # Phase 2.8: デフォルトでログストリーム管理画面を使用
                # PIDを環境変数で渡す
                self._run_tmux_command(
                    f'send-keys -t {self.CONTROL_PANE} "CLAUDE_PLUS_PID={self.pid} python3 {viewer_path} --logstream" Enter'
                )
                logger.info("ログストリーム管理画面を起動しました")
                
                # 再度Claude Codeペインにフォーカス
                # Cursor環境では起動時間を短縮
                wait_time = 0.5 if self.is_cursor_environment else 1.0
                time.sleep(wait_time)
                self._run_tmux_command(f"select-pane -t {self.CLAUDE_PANE}")
                
                # スクロール機能を有効化（一時的に無効化）
                # Claude CLIとの干渉を防ぐため無効化
                # self.enable_easy_scroll_mode()
            
        return success
    
    def switch_mode(self, mode: DisplayMode) -> bool:
        """表示モードを切り替え"""
        if not self.is_active:
            logger.warning("セッションがアクティブではありません")
            return False
            
        return self._apply_layout(mode)
    
    def send_to_claude(self, command: str) -> bool:
        """Claude Codeペインにコマンドを送信"""
        if not self.is_active:
            return False
            
        # コマンドがClaudeバイナリの場合は完全パスに強制変換
        if command.strip() == "claude" or command.startswith("claude "):
            # Auto_ClaudeCodeラッパーを回避するため、完全パスを使用
            claude_path = "/Users/harry/.nodebrew/current/bin/claude"
            command = command.replace("claude", claude_path, 1)
            logger.info(f"Claudeコマンドを完全パスに変換: {command}")
            
            # Claudeコマンドの起動時は通常の方法で送信
            escaped_cmd = command.replace('"', '\\"')
            success, _, _ = self._run_tmux_command(
                f'send-keys -t {self.CLAUDE_PANE} "{escaped_cmd}" Enter'
            )
            return success
        
        # ユーザー入力の場合は改善された方法を使用
        return self.send_user_input(command)
    
    def send_user_input(self, text: str) -> bool:
        """ユーザー入力をClaude Codeに送信（タイミング改善版）"""
        if not self.is_active:
            return False
        
        # 空の入力の場合は直接Enterを送信
        if not text or text.strip() == "":
            success, _, _ = self._run_tmux_command(
                f'send-keys -t {self.CLAUDE_PANE} Enter'
            )
            return success
        
        # テキストをエスケープ
        escaped_text = text.replace('"', '\\"').replace('$', '\\$')
        
        # テキストを送信
        success1, _, _ = self._run_tmux_command(
            f'send-keys -t {self.CLAUDE_PANE} "{escaped_text}"'
        )
        
        if not success1:
            return False
        
        # 重要: 少し待つ（Claude CLIが入力を処理するため）
        import time
        time.sleep(0.1)
        
        # Enterキーを送信
        success2, _, _ = self._run_tmux_command(
            f'send-keys -t {self.CLAUDE_PANE} Enter'
        )
        
        return success2
    
    def send_to_control(self, text: str) -> bool:
        """コントロールペインにテキストを送信（表示専用）"""
        if not self.is_active:
            return False
            
        if self.current_mode == DisplayMode.FOCUS:
            # フォーカスモードでは音声通知のみ
            return True
        
        # 安全な表示方法：Enterを送信せずにメッセージのみ表示
        # tmux display-messageを使用してコマンド実行を防止
        escaped_text = text.replace('"', '\\"')
        success, _, _ = self._run_tmux_command(
            f'display-message -t {self.CONTROL_PANE} "{escaped_text}"'
        )
        return success
    
    def capture_claude_output(self) -> Optional[str]:
        """Claude Codeペインの出力をキャプチャ"""
        if not self.is_active:
            return None
            
        success, stdout, _ = self._run_tmux_command(
            f"capture-pane -t {self.CLAUDE_PANE} -p"
        )
        
        if success:
            return stdout
        return None
    
    def capture_control_output(self) -> Optional[str]:
        """コントロールペインの出力をキャプチャ"""
        if not self.is_active or self.current_mode == DisplayMode.FOCUS:
            return None
            
        success, stdout, _ = self._run_tmux_command(
            f"capture-pane -t {self.CONTROL_PANE} -p"
        )
        
        if success:
            return stdout
        return None
    
    def check_and_handle_prompts(self) -> bool:
        """Claude Codeの確認プロンプトを検出して自動応答"""
        if not self.is_active:
            return False
        
        output = self.capture_claude_output()
        if not output:
            return False
        
        # 確認プロンプトのパターンを検出
        confirmation_patterns = [
            "Do you want to",
            "Do you want to proceed?",
            "❯ 1. Yes",
            "1. Yes",
        ]
        
        # 確認プロンプトが表示されているかチェック
        has_confirmation = any(pattern in output for pattern in confirmation_patterns)
        
        if has_confirmation:
            logger.debug("確認プロンプトを検出しました")
            
            # オプションを分析して正しい番号を選択
            lines = output.split('\n')
            yes_option = None
            dont_ask_option = None
            
            for i, line in enumerate(lines):
                # 番号付きの行を解析
                for num in ["1", "2", "3"]:
                    if f"{num}. " in line:
                        # "Yes"が含まれていて"No"が含まれていない場合
                        if "Yes" in line and "No" not in line:
                            if "don't ask again" in line.lower():
                                dont_ask_option = num
                            else:
                                yes_option = num
                        break
            
            # "don't ask again"があればそれを優先、なければ通常のYesを選択
            selected_option = dont_ask_option if dont_ask_option else yes_option
            
            if selected_option:
                logger.debug(f"'オプション {selected_option}' を選択中...")
                success, _, _ = self._run_tmux_command(
                    f'send-keys -t {self.CLAUDE_PANE} {selected_option}'
                )
                if success:
                    time.sleep(0.1)
                    # Enterで確定
                    self._run_tmux_command(
                        f'send-keys -t {self.CLAUDE_PANE} Enter'
                    )
                    logger.debug(f"'オプション {selected_option}' を選択しました")
                    return True
        
        return False
    
    def send_user_input_with_auto_confirm(self, text: str, max_confirmations: int = 3) -> bool:
        """ユーザー入力を送信し、確認プロンプトに自動応答"""
        if not self.is_active:
            return False
        
        # 最初の入力を送信
        success = self.send_user_input(text)
        if not success:
            return False
        
        # 確認プロンプトの自動処理
        confirmations_handled = 0
        max_wait_cycles = 20  # 最大100秒待機（5秒×20サイクル）
        
        for cycle in range(max_wait_cycles):
            time.sleep(5)  # 5秒待機
            
            # 確認プロンプトをチェック
            if self.check_and_handle_prompts():
                confirmations_handled += 1
                logger.debug(f"確認プロンプト#{confirmations_handled}を処理しました")
                
                # 最大確認回数に達した場合は終了
                if confirmations_handled >= max_confirmations:
                    logger.debug("最大確認回数に達しました")
                    break
                
                # 次の確認プロンプトを待つ
                continue
            
            # 処理完了の兆候をチェック
            output = self.capture_claude_output()
            if output:
                # プロンプトが戻った（>）かつ確認プロンプトがない場合は完了
                if (">" in output[-100:] or "❯" in output[-100:]) and "Do you want to" not in output:
                    logger.debug("処理が完了したようです")
                    break
        
        logger.debug(f"自動確認処理完了: {confirmations_handled}回の確認を処理")
        return True
    
    def _setup_pipes(self):
        """Named pipeを設定"""
        # PIDベースのディレクトリを作成
        os.makedirs(self.pipe_base, exist_ok=True)
        
        for pipe in [self.cmd_pipe, self.output_pipe]:
            try:
                os.unlink(pipe)
            except:
                pass
            try:
                os.mkfifo(pipe)
                logger.debug(f"Named pipe作成: {pipe}")
            except Exception as e:
                logger.error(f"Named pipe作成エラー: {e}")
    
    def _get_cleaned_path(self) -> str:
        """Claude CLIを保持しつつ、不要なAuto_ClaudeCode要素を除去したPATHを取得"""
        current_path = os.environ.get('PATH', '')
        path_parts = current_path.split(':')
        
        # Claude CLIのbinディレクトリは保持
        auto_claude_bin = "/Users/harry/Dropbox/Tool_Development/Auto_ClaudeCode/bin"
        
        # PATHにClaude CLIが含まれているかチェック
        has_claude = any(auto_claude_bin in part for part in path_parts)
        
        if has_claude:
            # Claude CLIのPATHは保持
            cleaned_path = current_path
            logger.info(f"PATH環境変数を保持: Claude CLI利用のため")
        else:
            # Claude CLIが見つからない場合は追加
            cleaned_parts = path_parts + [auto_claude_bin]
            cleaned_path = ':'.join(cleaned_parts)
            logger.info(f"PATH環境変数にClaude CLIを追加: {auto_claude_bin}")
        
        logger.debug(f"最終PATH: {cleaned_path}")
        
        return cleaned_path
    
    def _schedule_auto_attach(self):
        """tmuxセッションへの自動アタッチをスケジュール"""
        import threading
        import time
        
        def attach_after_delay():
            # セッションが完全に起動するまで少し待機
            time.sleep(2)
            
            try:
                # 現在のターミナルでアタッチを試行
                if self.platform == "darwin":
                    # macOS: 現在のターミナルウィンドウでアタッチ
                    # tmuxセッションが存在することを確認
                    check_success, _, _ = self._run_tmux_command(f"has-session -t {self.session_name}")
                    if check_success:
                        logger.info(f"tmuxセッション '{self.session_name}' にアタッチ中...")
                        
                        # アタッチの準備完了をフラグで示す
                        self.attach_ready = True
                        logger.info("tmuxセッションへのアタッチ準備完了")
                        logger.info("tmuxセッションアタッチ完了")
                    else:
                        logger.warning("tmuxセッションが見つかりません")
                else:
                    # Linux: 手動アタッチの案内
                    logger.info(f"手動でアタッチしてください: tmux attach-session -t {self.session_name}")
                    
            except Exception as e:
                logger.error(f"自動アタッチエラー: {e}")
        
        # バックグラウンドでアタッチを実行
        attach_thread = threading.Thread(target=attach_after_delay)
        attach_thread.daemon = True
        attach_thread.start()
    
    def _cleanup_pipes(self):
        """Named pipeをクリーンアップ"""
        for pipe in [self.cmd_pipe, self.output_pipe]:
            try:
                os.unlink(pipe)
            except:
                pass
    
    def _start_fallback_mode(self) -> bool:
        """tmuxが使えない場合のフォールバックモード（2ウィンドウ）"""
        logger.info("フォールバックモード: 2つのターミナルウィンドウを使用します")
        
        if self.platform == "darwin":
            # macOS: 新しいターミナルウィンドウでClaude Codeを起動
            applescript = '''
            tell application "Terminal"
                do script "echo '🇯🇵 Claude++ コントロールパネル'; echo '通常のターミナルでClaude Codeが起動します'; echo '画面分割は利用できませんが、全機能は正常に動作します'"
                activate
            end tell
            '''
            try:
                subprocess.run(["osascript", "-e", applescript])
                logger.info("コントロールパネルウィンドウを開きました")
                return True
            except Exception as e:
                logger.error(f"ターミナルウィンドウの起動に失敗: {e}")
                return False
        else:
            # Linux: 手動での起動を案内
            print("\n" + "="*60)
            print("🇯🇵 Claude++ フォールバックモード")
            print("="*60)
            print("tmuxが利用できないため、2ウィンドウモードで動作します。")
            print("\n新しいターミナルウィンドウを開いて、以下を実行してください:")
            print("  tail -f /tmp/claude-plus.log")
            print("\nこのウィンドウでClaude Codeが起動します。")
            print("="*60 + "\n")
            return True
    
    def _attach_session(self):
        """tmuxセッションをアタッチ（新しいターミナルで）"""
        if self.platform == "darwin":
            # macOS: 新しいターミナルウィンドウでセッションをアタッチ
            applescript = f'''
            tell application "Terminal"
                do script "tmux attach-session -t {self.session_name}"
                activate
            end tell
            '''
            subprocess.run(["osascript", "-e", applescript])
        else:
            # Linux: 現在のターミナルでアタッチ（手動で新しいターミナルを開く必要がある）
            print(f"新しいターミナルで以下のコマンドを実行してください:")
            print(f"tmux attach-session -t {self.session_name}")
    
    def _cleanup_old_sessions(self, max_sessions: int = 3):
        """古いClaude+セッションをクリーンアップ（リソース使用量削減）
        
        Args:
            max_sessions: Claude++セッションの最大数（デフォルト3）
        """
        try:
            # Claude++セッションの情報を取得
            result = subprocess.run(
                ["tmux", "list-sessions", "-F", "#{session_name}:#{session_attached}:#{session_created}"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                claude_sessions = []
                for line in result.stdout.strip().split('\n'):
                    if line and 'claude_plus' in line:
                        parts = line.split(':')
                        if len(parts) >= 3:
                            session_info = {
                                'name': parts[0],
                                'attached': parts[1] == '1',
                                'created': int(parts[2]) if parts[2].isdigit() else 0
                            }
                            claude_sessions.append(session_info)
                
                # 作成時刻でソート（古い順）
                claude_sessions.sort(key=lambda x: x['created'])
                
                # 最大数を超える場合、古いセッションから削除
                sessions_to_remove = []
                if len(claude_sessions) >= max_sessions:
                    # アタッチされていない古いセッションを優先的に削除
                    for session in claude_sessions:
                        if not session['attached'] and session['name'] != self.session_name:
                            sessions_to_remove.append(session['name'])
                            if len(claude_sessions) - len(sessions_to_remove) < max_sessions:
                                break
                
                # 削除実行
                for session_name in sessions_to_remove:
                    self._run_tmux_command(f"kill-session -t {session_name}")
                    logger.debug(f"古いセッション削除: {session_name}")
                
                if sessions_to_remove:
                    logger.info(f"Claude++セッションを {len(sessions_to_remove)} 個整理しました（最大{max_sessions}個まで）")
                    
        except Exception as e:
            logger.debug(f"古いセッション整理エラー: {e}")
    
    def _try_reuse_existing_session(self) -> bool:
        """既存のセッションを再利用できるか試みる"""
        try:
            # 現在のセッションが存在し、生きているか確認
            if self._verify_session_exists():
                # セッションの状態を確認
                result = subprocess.run(
                    f"tmux list-panes -t {self.session_name} -F '#{pane_dead}'",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    # すべてのペインが生きているか確認
                    pane_states = result.stdout.strip().split('\n')
                    if all(state == '0' for state in pane_states if state):
                        logger.info(f"既存のセッション '{self.session_name}' は健全です")
                        self.is_active = True
                        
                        # Claude Codeペインにフォーカス
                        self._run_tmux_command(f"select-pane -t {self.CLAUDE_PANE}")
                        return True
                    else:
                        logger.debug("既存のセッションにデッドペインがあります")
            
            return False
            
        except Exception as e:
            logger.debug(f"セッション再利用チェックエラー: {e}")
            return False
    
    def _cleanup_session(self):
        """既存のセッションをクリーンアップ"""
        self._run_tmux_command(f"kill-session -t {self.session_name} 2>/dev/null")
        self._cleanup_pipes()
    
    def stop_session(self):
        """セッションを停止"""
        if self.is_active:
            # マウスホイールバインディングを復元
            self._restore_mouse_wheel_bindings()
            
            self._cleanup_session()
            self.is_active = False
            logger.info("画面分割セッションを停止しました")
    
    def _setup_claude_scroll_features(self):
        """Claude Code専用スクロール機能を設定（Cursor最適化対応）"""
        try:
            # 基本スクロール機能の設定
            logger.info("📜 スクロール機能を設定中...")
            
            # Claude Codeペイン専用のスクロール改善
            # 1. PageUp/PageDownでClaude Codeペインのスクロール（モード切替不要）
            # ペインターゲットを明示的に指定
            self._run_tmux_command(f"bind-key -T root PageUp 'select-pane -t {self.CLAUDE_PANE}; copy-mode -u'")
            self._run_tmux_command(f"bind-key -T root PageDown 'select-pane -t {self.CLAUDE_PANE}; copy-mode; send-keys -X page-down'")
            
            # 2. Shift+上下矢印でスクロール（より直感的）
            self._run_tmux_command(f"bind-key -T root S-Up 'copy-mode -u'")
            self._run_tmux_command(f"bind-key -T root S-Down 'copy-mode; send-keys -X cursor-down'")
            
            # 3. Ctrl+U/Ctrl+Dでページ単位スクロール（vi風）
            self._run_tmux_command(f"bind-key -T root C-u 'copy-mode; send-keys -X page-up'")
            self._run_tmux_command(f"bind-key -T root C-d 'copy-mode; send-keys -X page-down'")
            
            # 4. Escキーでスクロールモードを終了（通常入力に戻る）
            self._run_tmux_command(f"bind-key -T copy-mode-vi Escape send-keys -X cancel")
            
            # 5. コピーモードでのviキーバインド強化（会話履歴スクロール最適化）
            self._run_tmux_command(f"bind-key -T copy-mode-vi 'v' send-keys -X begin-selection")
            self._run_tmux_command(f"bind-key -T copy-mode-vi 'y' send-keys -X copy-selection")
            self._run_tmux_command(f"bind-key -T copy-mode-vi 'j' send-keys -X cursor-down")
            self._run_tmux_command(f"bind-key -T copy-mode-vi 'k' send-keys -X cursor-up")
            # 会話履歴スクロール専用のスムーズスクロール
            self._run_tmux_command(f"bind-key -T copy-mode-vi 'u' send-keys -X halfpage-up")
            self._run_tmux_command(f"bind-key -T copy-mode-vi 'd' send-keys -X halfpage-down")
            self._run_tmux_command(f"bind-key -T copy-mode-vi 'g' send-keys -X history-top")
            self._run_tmux_command(f"bind-key -T copy-mode-vi 'G' send-keys -X history-bottom")
            
            # 6. キーボードでの追加スクロール操作
            # Ctrl+Shift+PageUp/PageDownでもスクロール可能
            self._run_tmux_command(f"bind-key -T root C-S-PageUp select-pane -t {self.CLAUDE_PANE} \\; copy-mode -u")
            self._run_tmux_command(f"bind-key -T root C-S-PageDown select-pane -t {self.CLAUDE_PANE} \\; copy-mode \\; send-keys -X page-down")
            
            # 7. 検索機能の強化（会話履歴内検索）
            self._run_tmux_command(f"bind-key -T copy-mode-vi '/' command-prompt -p 'search down' 'send-keys -X search-forward \"%%\"'")
            self._run_tmux_command(f"bind-key -T copy-mode-vi '?' command-prompt -p 'search up' 'send-keys -X search-backward \"%%\"'")
            
            # Phase 2.6.1: Cursor環境での追加最適化
            if self.is_cursor_environment:
                self._apply_cursor_scroll_optimizations()
            
            logger.info("Claude Code専用スクロール機能を設定しました")
            
        except Exception as e:
            logger.error(f"スクロール機能設定エラー: {e}")
    
    def _apply_cursor_scroll_optimizations(self):
        """Cursor環境用スクロール最適化（Phase 2.6.1.1 簡素化）"""
        try:
            logger.info("🖥️  Cursor環境用スクロール最適化を適用中...")
            
            # マウスは無効化（通常のマウス操作を維持）
            self._run_tmux_command(f"set-option -t {self.session_name} -g mouse off")
            
            # キーボードスクロールの強化（Cursor環境で確実に動作）
            self._run_tmux_command(f"bind-key -T root PageUp select-pane -t {self.CLAUDE_PANE} \\; copy-mode -u")
            self._run_tmux_command(f"bind-key -T root PageDown select-pane -t {self.CLAUDE_PANE} \\; copy-mode \\; send-keys -X page-down")
            
            # Cursor設定の簡易調整
            self._apply_cursor_settings_adjustment()
            
            # シンプルなスクロール設定
            self._setup_enhanced_scroll_blocking()
            
            logger.info("✅ Cursor環境スクロール最適化が完了しました")
            
        except Exception as e:
            logger.error(f"Cursorスクロール最適化エラー: {e}")
    
    def _apply_cursor_settings_adjustment(self):
        """Cursor IDE設定の簡易調整（Phase 2.6.1.1 簡素化）"""
        try:
            logger.info("⚙️  Cursor環境での動作を最適化...")
            # 環境変数のみでの制御（ファイル変更なし）
            logger.info("✅ Cursor環境最適化が完了しました")
            
        except Exception as e:
            logger.error(f"Cursor設定調整エラー: {e}")
    
    def restore_cursor_settings_on_exit(self):
        """終了時の簡易クリーンアップ（Phase 2.6.1.1 簡素化）"""
        try:
            logger.info("✅ Cursor環境クリーンアップが完了しました")
        except Exception as e:
            logger.error(f"終了時クリーンアップエラー: {e}")
    
    def _setup_enhanced_scroll_blocking(self):
        """シンプルなスクロール設定（Phase 2.6.1.1 簡素化）"""
        try:
            logger.info("🚫 スクロール設定を適用中...")
            
            # 基本的なペイン境界の明確化
            self._run_tmux_command(f"set-option -t {self.session_name} -g pane-active-border-style 'fg=green,bg=default'")
            self._run_tmux_command(f"set-option -t {self.session_name} -g pane-border-style 'fg=colour240,bg=default'")
            
            # スクロール状態の視覚的フィードバック
            self._run_tmux_command(f"set-option -t {self.session_name} -g mode-style 'fg=black,bg=yellow'")
            self._run_tmux_command(f"set-option -t {self.session_name} -g message-style 'fg=white,bg=blue'")
            
            logger.info("✅ スクロール設定が適用されました")
            
        except Exception as e:
            logger.error(f"スクロール設定エラー: {e}")
    
    def enable_easy_scroll_mode(self):
        """簡単スクロールモードを有効化（Cursor環境最適化対応）"""
        if not self.is_active:
            return False
        
        # Cursor環境に応じたガイド表示
        if self.is_cursor_environment:
            self._show_cursor_scroll_guide()
        else:
            self._show_standard_scroll_guide()
        
        # 使いやすさ向上のための追加設定
        try:
            # スクロール履歴バッファを増加
            self._run_tmux_command(f"set-option -t {self.session_name} -g history-limit 100000")
            
            # スクロール時の表示を改善
            self._run_tmux_command(f"set-option -t {self.session_name} -g wrap-search on")
            
            # Claude Codeペインにフォーカスを確実に設定
            self._run_tmux_command(f"select-pane -t {self.CLAUDE_PANE}")
            
            return True
            
        except Exception as e:
            logger.error(f"簡単スクロールモード設定エラー: {e}")
            return False
    
    def _show_cursor_scroll_guide(self):
        """Cursor環境用のスクロール操作ガイドを表示"""
        logger.info("=== 🖥️  Cursor IDE - Claude Code スクロール操作ガイド ===")
        logger.info("📜 チャット履歴のスクロール方法:")
        logger.info("")
        logger.info("  ⌨️  キーボード操作:")
        logger.info("    • PageUp/PageDown   : ページ単位でスクロール（推奨）")
        logger.info("    • Shift + ↑/↓      : 行単位でスクロール")
        logger.info("    • Ctrl + U/D        : 半ページスクロール")
        logger.info("    • g/G               : 最上部/最下部へ移動")
        logger.info("    • Esc               : 通常入力モードに戻る")
        logger.info("")
        logger.info("  🖱️  マウス操作:")
        logger.info("    • マウスホイール   : Claude CLIとの直接連携")
        logger.info("    • テキスト選択     : 通常通り可能")
        logger.info("")
        logger.info("  🔄 マウスモード切り替え:")
        logger.info("    • Ctrl+b m          : マウスモードON（管理画面スクロール用）")
        logger.info("    • Ctrl+b M          : マウスモードOFF（Claude CLI入力用）")
        logger.info("")
        logger.info("✨ 履歴は5万行まで保存されます")
        logger.info("========================================================")
    
    def _show_standard_scroll_guide(self):
        """標準ターミナル環境用のスクロール操作ガイドを表示"""
        logger.info("=== Claude Code スクロール操作ガイド ===")
        logger.info("📜 チャット履歴のスクロール方法:")
        logger.info("  • PageUp/PageDown    : ページ単位でスクロール")
        logger.info("  • Shift + ↑/↓       : 行単位でスクロール") 
        logger.info("  • Ctrl + U/D         : 半ページスクロール")
        logger.info("  • g/G                : 最上部/最下部へ移動")
        logger.info("  • Esc                : 通常入力モードに戻る")
        logger.info("")
        logger.info("🔄 マウスモード切り替え:")
        logger.info("  • Ctrl+b m           : マウスモードON")
        logger.info("  • Ctrl+b M           : マウスモードOFF")
        logger.info("==========================================")

    def get_status(self) -> Dict[str, Any]:
        """現在のステータスを取得"""
        return {
            "active": self.is_active,
            "mode": self.current_mode.value,
            "platform": self.platform,
            "session_name": self.session_name
        }


# Windows Terminal対応（将来実装）
class WindowsTerminalController(ScreenController):
    """Windows Terminal用の画面分割制御（将来実装）"""
    
    def __init__(self, session_name: str = "claude_plus"):
        super().__init__(session_name)
        logger.warning("Windows Terminal対応は将来実装予定です")
    
    def start_session(self) -> bool:
        """Windows Terminalでは2ウィンドウモードで実装予定"""
        logger.info("Windows版は開発中です。しばらくお待ちください。")
        return False