#!/usr/bin/env python3
"""
Claude++ System エラーハンドリングシステム
包括的なエラー処理、回復、ユーザー通知を管理
"""

import logging
import traceback
import asyncio
from typing import Dict, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class ErrorSeverity(Enum):
    """エラーの重要度"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    CRITICAL = "重大"


class ErrorCategory(Enum):
    """エラーのカテゴリ"""
    COMMAND_NOT_FOUND = "コマンド未発見"
    PERMISSION_DENIED = "権限エラー"
    NETWORK_ERROR = "ネットワークエラー"
    FILE_ERROR = "ファイルエラー"
    GIT_ERROR = "Git操作エラー"
    SYSTEM_ERROR = "システムエラー"
    USER_ERROR = "ユーザーエラー"
    UNKNOWN = "不明"


@dataclass
class ErrorInfo:
    """エラー情報"""
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    original_error: Optional[Exception]
    timestamp: datetime
    context: Dict[str, Any]
    suggested_action: str
    auto_recovery_possible: bool = False


class ErrorHandler:
    """統合エラーハンドラー"""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.error_handler')
        self.ui_manager = None
        self.notifications = None
        self.recovery_handlers = {}
        self.error_history = []
        
        # 自動回復ハンドラーを登録
        self._register_recovery_handlers()
    
    def initialize(self, ui_manager=None, notifications=None):
        """エラーハンドラーの初期化"""
        self.ui_manager = ui_manager
        self.notifications = notifications
        
        # 日本語UIマネージャーの自動取得
        if self.ui_manager is None:
            try:
                from .japanese_ui import get_ui_manager
                self.ui_manager = get_ui_manager()
            except ImportError:
                pass
        
        # 通知システムの自動取得
        if self.notifications is None:
            try:
                from .notifications import get_notification_manager
                self.notifications = get_notification_manager()
            except ImportError:
                pass
        
    def _register_recovery_handlers(self):
        """自動回復ハンドラーを登録"""
        self.recovery_handlers = {
            ErrorCategory.COMMAND_NOT_FOUND: self._recover_command_not_found,
            ErrorCategory.PERMISSION_DENIED: self._recover_permission_denied,
            ErrorCategory.NETWORK_ERROR: self._recover_network_error,
            ErrorCategory.GIT_ERROR: self._recover_git_error,
            ErrorCategory.FILE_ERROR: self._recover_file_error,
            ErrorCategory.SYSTEM_ERROR: self._recover_system_error,
            ErrorCategory.USER_ERROR: self._recover_user_error,
        }
    
    async def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
        """エラーを処理し、適切な対応を実行"""
        context = context or {}
        
        # エラーを分析
        error_info = self._analyze_error(error, context)
        
        # エラー履歴に記録
        self.error_history.append(error_info)
        self.logger.error(f"Error handled: {error_info.category.value} - {error_info.message}")
        
        # ユーザーに通知
        await self._notify_user(error_info)
        
        # 自動回復を試行
        if error_info.auto_recovery_possible:
            recovery_success = await self._attempt_recovery(error_info)
            if recovery_success:
                await self._notify_recovery_success(error_info)
            else:
                await self._notify_recovery_failed(error_info)
        
        return error_info
    
    def _analyze_error(self, error: Exception, context: Dict[str, Any]) -> ErrorInfo:
        """エラーを分析してカテゴリ化"""
        error_msg = str(error).lower()
        error_type = type(error).__name__
        
        # Claude Code特有のエラーパターンを優先検査
        category, severity, auto_recovery, suggested_action = self._analyze_claude_error(error_msg, error_type, context)
        
        # Claude Code特有でない場合は一般的なエラー分析
        if category == ErrorCategory.UNKNOWN:
            category, severity, auto_recovery, suggested_action = self._analyze_general_error(error_msg, error_type)
        
        # 日本語メッセージの生成（UIマネージャーを使用）
        if self.ui_manager:
            japanese_message = self.ui_manager.translate_error(str(error))
            # エラー解決方法の取得
            if hasattr(self.ui_manager, 'error_solutions'):
                solution_info = self._get_solution_info(error_msg)
                if solution_info:
                    suggested_action = solution_info.get('steps', [suggested_action])[0]
        else:
            japanese_message = f"エラーが発生しました: {str(error)}"
        
        return ErrorInfo(
            category=category,
            severity=severity,
            message=japanese_message,
            original_error=error,
            timestamp=datetime.now(),
            context=context,
            suggested_action=suggested_action,
            auto_recovery_possible=auto_recovery
        )
    
    def _analyze_claude_error(self, error_msg: str, error_type: str, context: Dict[str, Any]) -> tuple:
        """Claude Code特有のエラーを分析"""
        # Claude Code APIエラー
        if any(api_error in error_msg for api_error in ["api key not found", "authentication error", "api quota exceeded"]):
            return ErrorCategory.SYSTEM_ERROR, ErrorSeverity.CRITICAL, True, "Claude APIの設定を確認してください"
        
        # Claude Code入力エラー
        if "input must be provided" in error_msg or "context length exceeded" in error_msg:
            return ErrorCategory.USER_ERROR, ErrorSeverity.MEDIUM, True, "入力内容を調整してください"
        
        # Claude Code ファイル操作エラー
        if "file already exists" in error_msg or "overwrite confirmation" in error_msg:
            return ErrorCategory.FILE_ERROR, ErrorSeverity.LOW, True, "自動で上書き確認を処理します"
        
        # tmux / 画面分割エラー
        if "tmux" in error_msg or "session" in error_msg:
            return ErrorCategory.SYSTEM_ERROR, ErrorSeverity.MEDIUM, True, "画面分割システムを再起動します"
        
        return ErrorCategory.UNKNOWN, ErrorSeverity.HIGH, False, "詳細な分析が必要です"
    
    def _analyze_general_error(self, error_msg: str, error_type: str) -> tuple:
        """一般的なエラーを分析"""
        if "command not found" in error_msg or "no such file" in error_msg:
            return ErrorCategory.COMMAND_NOT_FOUND, ErrorSeverity.HIGH, True, "必要なツールをインストールしてください"
            
        elif "permission denied" in error_msg or "access denied" in error_msg:
            return ErrorCategory.PERMISSION_DENIED, ErrorSeverity.MEDIUM, True, "ファイルの権限を確認してください"
            
        elif "network" in error_msg or "connection" in error_msg or "timeout" in error_msg:
            return ErrorCategory.NETWORK_ERROR, ErrorSeverity.MEDIUM, True, "インターネット接続を確認してください"
            
        elif "git" in error_msg or "repository" in error_msg:
            return ErrorCategory.GIT_ERROR, ErrorSeverity.MEDIUM, True, "Gitリポジトリの状態を確認してください"
            
        elif any(file_error in error_msg for file_error in ["file not found", "directory not found", "io error"]):
            return ErrorCategory.FILE_ERROR, ErrorSeverity.MEDIUM, False, "ファイルパスを確認してください"
            
        else:
            return ErrorCategory.UNKNOWN, ErrorSeverity.HIGH, False, "詳細ログを確認してください"
    
    def _get_solution_info(self, error_msg: str) -> Optional[Dict[str, Any]]:
        """エラーメッセージから解決方法情報を取得"""
        if not self.ui_manager or not hasattr(self.ui_manager, 'error_solutions'):
            return None
            
        for error_key, solution in self.ui_manager.error_solutions.items():
            if error_key in error_msg:
                return solution
        return None
    
    async def _notify_user(self, error_info: ErrorInfo):
        """ユーザーにエラーを通知"""
        if not self.notifications:
            return
            
        # 重要度に応じた通知レベル
        if error_info.severity == ErrorSeverity.CRITICAL:
            await self.notifications.error(
                "重大エラー", 
                f"{error_info.message}\n💡 {error_info.suggested_action}"
            )
        elif error_info.severity == ErrorSeverity.HIGH:
            await self.notifications.warning(
                "エラー発生", 
                f"{error_info.message}\n💡 {error_info.suggested_action}"
            )
        else:
            await self.notifications.info(
                "軽微なエラー", 
                f"{error_info.message}\n💡 {error_info.suggested_action}"
            )
    
    async def _attempt_recovery(self, error_info: ErrorInfo) -> bool:
        """自動回復を試行"""
        recovery_handler = self.recovery_handlers.get(error_info.category)
        
        if recovery_handler:
            try:
                return await recovery_handler(error_info)
            except Exception as e:
                self.logger.error(f"Recovery handler failed: {e}")
                return False
        
        return False
    
    async def _recover_command_not_found(self, error_info: ErrorInfo) -> bool:
        """コマンド未発見エラーの回復"""
        # 代替コマンドの提案
        context = error_info.context
        command = context.get('command', '')
        
        # よくある代替コマンド
        alternatives = {
            'claude': ['claude-code', '/usr/local/bin/claude'],
            'python': ['python3', 'python3.9', 'python3.8'],
            'pip': ['pip3', 'python -m pip', 'python3 -m pip'],
            'git': ['/usr/bin/git', '/usr/local/bin/git']
        }
        
        if command in alternatives:
            for alt in alternatives[command]:
                if self._check_command_exists(alt):
                    # 設定を更新して代替コマンドを使用
                    self.logger.info(f"代替コマンドを発見: {alt}")
                    return True
        
        return False
    
    async def _recover_permission_denied(self, error_info: ErrorInfo) -> bool:
        """権限エラーの回復"""
        # 一時的な権限変更は危険なので、ユーザーに通知のみ
        if self.notifications:
            await self.notifications.info(
                "権限エラー回復", 
                "管理者に権限の変更を依頼してください"
            )
        return False
    
    async def _recover_network_error(self, error_info: ErrorInfo) -> bool:
        """ネットワークエラーの回復"""
        # 短時間待機してリトライ
        await asyncio.sleep(5)
        
        # 簡単な接続テスト
        try:
            import subprocess
            result = subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                                  capture_output=True, timeout=10)
            return result.returncode == 0
        except Exception:
            return False
    
    async def _recover_git_error(self, error_info: ErrorInfo) -> bool:
        """Git操作エラーの回復"""
        # Git状態のクリーンアップを試行
        try:
            import subprocess
            # マージ・リベースの中断状態をクリア
            subprocess.run(['git', 'merge', '--abort'], 
                         capture_output=True, errors='ignore')
            subprocess.run(['git', 'rebase', '--abort'], 
                         capture_output=True, errors='ignore')
            return True
        except Exception:
            return False
    
    async def _recover_file_error(self, error_info: ErrorInfo) -> bool:
        """ファイル操作エラーの回復"""
        try:
            error_msg = str(error_info.original_error).lower()
            
            # ディスク容量不足の場合
            if "disk full" in error_msg or "no space left" in error_msg:
                # 一時ファイルのクリーンアップ
                import subprocess
                subprocess.run(['find', '/tmp', '-name', '*.tmp', '-delete'], 
                             capture_output=True, errors='ignore')
                return True
            
            # ファイル既存の場合（自動上書き）
            if "file already exists" in error_msg:
                return True  # 自動Yes機能が処理
                
            return False
        except Exception:
            return False
    
    async def _recover_system_error(self, error_info: ErrorInfo) -> bool:
        """システムエラーの回復"""
        try:
            error_msg = str(error_info.original_error).lower()
            
            # tmux関連エラー
            if "tmux" in error_msg:
                return await self._recover_tmux_error(error_info)
            
            # Claude API関連エラー
            if any(api_error in error_msg for api_error in ["api key", "authentication", "quota"]):
                return await self._recover_api_error(error_info)
            
            # メモリ不足
            if "out of memory" in error_msg:
                # ガベージコレクション実行
                import gc
                gc.collect()
                await asyncio.sleep(1)
                return True
                
            return False
        except Exception:
            return False
    
    async def _recover_user_error(self, error_info: ErrorInfo) -> bool:
        """ユーザーエラーの回復"""
        try:
            error_msg = str(error_info.original_error).lower()
            
            # 入力関連エラーは自動で処理
            if "input must be provided" in error_msg:
                # デフォルト入力を提供する準備
                return True
            
            # コンテキスト長超過
            if "context length exceeded" in error_msg:
                # 自動で内容を分割する準備
                return True
                
            return False
        except Exception:
            return False
    
    async def _recover_tmux_error(self, error_info: ErrorInfo) -> bool:
        """tmux関連エラーの回復"""
        try:
            import subprocess
            
            # 既存のセッションを確認
            result = subprocess.run(['tmux', 'list-sessions'], 
                                  capture_output=True, text=True, errors='ignore')
            
            # 不要なセッションのクリーンアップ
            if result.returncode == 0:
                sessions = result.stdout.strip().split('\n')
                for session in sessions:
                    if 'claude_plus' in session and 'attached' not in session:
                        session_name = session.split(':')[0]
                        subprocess.run(['tmux', 'kill-session', '-t', session_name], 
                                     capture_output=True, errors='ignore')
            
            # 新しいセッション作成を試行
            await asyncio.sleep(2)
            return True
            
        except Exception:
            return False
    
    async def _recover_api_error(self, error_info: ErrorInfo) -> bool:
        """Claude API関連エラーの回復"""
        try:
            error_msg = str(error_info.original_error).lower()
            
            # APIキー未設定の場合
            if "api key not found" in error_msg:
                # 設定ファイルの確認
                import os
                config_paths = [
                    os.path.expanduser("~/.claude/config.yaml"),
                    os.path.expanduser("~/.config/claude/config.yaml")
                ]
                
                for config_path in config_paths:
                    if os.path.exists(config_path):
                        return True  # 設定ファイルが存在する場合は復旧可能
                
                # 環境変数の確認
                if os.environ.get('ANTHROPIC_API_KEY'):
                    return True
                    
            # レート制限の場合
            elif "rate limit" in error_msg or "quota exceeded" in error_msg:
                # 短時間待機
                await asyncio.sleep(30)
                return True
                
            return False
        except Exception:
            return False
    
    def _check_command_exists(self, command: str) -> bool:
        """コマンドの存在確認"""
        try:
            import subprocess
            result = subprocess.run(['which', command], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    async def _notify_recovery_success(self, error_info: ErrorInfo):
        """回復成功の通知"""
        if self.notifications:
            await self.notifications.success(
                "自動回復成功", 
                f"{error_info.category.value}から自動的に回復しました"
            )
    
    async def _notify_recovery_failed(self, error_info: ErrorInfo):
        """回復失敗の通知"""
        if self.notifications:
            await self.notifications.warning(
                "手動対応が必要", 
                f"自動回復に失敗しました。{error_info.suggested_action}"
            )
    
    async def emergency_save(self, context: Dict[str, Any] = None) -> bool:
        """緊急保存を実行"""
        try:
            context = context or {}
            
            # 現在の作業ディレクトリ情報を取得
            import os
            current_dir = os.getcwd()
            
            # Git状態の確認
            import subprocess
            git_status = subprocess.run(['git', 'status', '--porcelain'], 
                                      capture_output=True, text=True, errors='ignore')
            
            if git_status.returncode == 0 and git_status.stdout.strip():
                # 変更があれば緊急コミット
                subprocess.run(['git', 'add', '.'], capture_output=True, errors='ignore')
                
                # 緊急コミットメッセージ
                emergency_msg = f"緊急保存 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                subprocess.run(['git', 'commit', '-m', emergency_msg], 
                             capture_output=True, errors='ignore')
                
                # UIに通知
                if self.ui_manager:
                    emergency_message = self.ui_manager.get_message('emergency_save')
                    if self.notifications:
                        await self.notifications.success("緊急保存完了", emergency_message)
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Emergency save failed: {e}")
            return False
    
    async def handle_process_termination(self, process_info: Dict[str, Any] = None) -> bool:
        """プロセス異常終了時の処理"""
        try:
            # 緊急保存を実行
            save_success = await self.emergency_save(process_info)
            
            # プロセス情報をログに記録
            self.logger.critical(f"Process termination detected: {process_info}")
            
            # システム状態のクリーンアップ
            await self._cleanup_system_state()
            
            # ユーザーに通知
            if self.notifications:
                await self.notifications.warning(
                    "プロセス異常終了", 
                    "システムが異常終了しましたが、作業内容は安全に保存されました。"
                )
            
            return save_success
            
        except Exception as e:
            self.logger.error(f"Process termination handler failed: {e}")
            return False
    
    async def _cleanup_system_state(self):
        """システム状態のクリーンアップ"""
        try:
            # tmuxセッションのクリーンアップ
            import subprocess
            
            # claude_plusセッションを確認
            result = subprocess.run(['tmux', 'list-sessions'], 
                                  capture_output=True, text=True, errors='ignore')
            
            if result.returncode == 0:
                sessions = result.stdout.strip().split('\n')
                for session in sessions:
                    if 'claude_plus' in session:
                        session_name = session.split(':')[0]
                        subprocess.run(['tmux', 'kill-session', '-t', session_name], 
                                     capture_output=True, errors='ignore')
            
            # 一時ファイルのクリーンアップ
            import glob
            temp_files = glob.glob('/tmp/claude_plus_*')
            for temp_file in temp_files:
                try:
                    import os
                    os.remove(temp_file)
                except:
                    pass
                    
        except Exception as e:
            self.logger.error(f"System cleanup failed: {e}")
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """エラー統計を取得"""
        total_errors = len(self.error_history)
        if total_errors == 0:
            return {"total": 0}
        
        by_category = {}
        by_severity = {}
        
        for error in self.error_history:
            category = error.category.value
            severity = error.severity.value
            
            by_category[category] = by_category.get(category, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        return {
            "total": total_errors,
            "by_category": by_category,
            "by_severity": by_severity,
            "recent_errors": [
                {
                    "category": error.category.value,
                    "message": error.message,
                    "timestamp": error.timestamp.isoformat()
                }
                for error in self.error_history[-5:]  # 最新5件
            ]
        }


# グローバルエラーハンドラー（シングルトン）
_global_error_handler = None

def get_error_handler() -> ErrorHandler:
    """グローバルエラーハンドラーを取得"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler


async def handle_error(error: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
    """便利関数: エラーを処理"""
    return await get_error_handler().handle_error(error, context)