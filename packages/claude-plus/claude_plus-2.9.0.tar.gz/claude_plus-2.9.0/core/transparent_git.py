#!/usr/bin/env python3
"""
Claude++ 透明作業保護システム
Git操作を完全に隠蔽し、分かりやすい日本語で作業を自動保護します。
"""

import asyncio
import os
import time
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# 既存のGit Proエンジンを活用
try:
    from engines.git_pro import GitProEngine, GitContext
except ImportError:
    GitProEngine = None
    GitContext = None


class WorkState(Enum):
    """作業状態の分類"""
    FIRST_TIME = "初回作業"
    CONTINUING = "作業継続" 
    EXPERIMENTING = "実験中"
    COMPLETING = "作業完了"
    PROTECTING = "緊急保護"
    RECOVERING = "復旧中"


@dataclass
class WorkSession:
    """作業セッション情報"""
    session_id: str
    start_time: datetime
    last_save: Optional[datetime] = None
    work_folder: str = ""  # ブランチ名を「作業フォルダ」として表現
    files_changed: int = 0
    auto_saves: int = 0
    state: WorkState = WorkState.FIRST_TIME


class TransparentGitEngine:
    """Git操作を完全に透明化する自動作業保護エンジン"""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.transparent_git')
        self.config = {}
        self.enabled = True
        self.git_pro = None
        self.notifications = None
        
        # 作業セッション管理
        self.current_session = None
        self.auto_save_interval = 30  # 分
        self.auto_save_task = None
        
        # 日本語メッセージ
        self.messages = {
            'work_start': "新しい作業を開始しました ✨",
            'work_continue': "前回の続きから開始します 🔄",
            'work_save': "作業内容を保存しました 💾",
            'work_backup': "クラウドにバックアップしました ☁️",
            'work_protect': "作業を安全に保護しました 🛡️",
            'work_complete': "作業が完了しました 🎉",
            'work_folder_ready': "新しい作業フォルダを準備しました 📁",
            'emergency_save': "緊急保存を実行しました ⚡",
            'recovery_success': "前の安全な状態に戻しました 🔄",
            'network_check': "インターネット接続を確認中... 🌐",
            'conflict_resolved': "ファイルの重複を自動で解決しました 🔧"
        }
        
        # 統計情報
        self.stats = {
            'sessions_started': 0,
            'auto_saves_performed': 0,
            'emergency_protections': 0,
            'successful_recoveries': 0,
            'work_folders_created': 0,
            'backups_completed': 0
        }
        
    async def initialize(self, config: Dict, git_pro_engine=None, notifications=None):
        """透明Git エンジンの初期化"""
        self.config = config.get('transparent_git', {})
        self.enabled = self.config.get('enabled', True)
        self.auto_save_interval = self.config.get('auto_save_interval', 30)
        
        # Git Proエンジンの設定
        self.git_pro = git_pro_engine
        self.notifications = notifications
        
        if not self.git_pro and GitProEngine:
            self.git_pro = GitProEngine()
            await self.git_pro.initialize(config)
            
        if not self.enabled:
            return
            
        # 作業ディレクトリの確認
        if not await self._is_work_directory():
            await self._setup_work_directory()
            
        self.logger.info("透明作業保護システムが初期化されました")
        
    async def start_work(self, task_description: str = "", repo_path: str = ".") -> bool:
        """作業開始 - 自動で適切な作業環境を準備"""
        if not self.enabled or not self.git_pro:
            return False
            
        try:
            # 現在の状況を分析
            work_state = await self._analyze_work_situation(repo_path)
            
            # セッション開始
            self.current_session = WorkSession(
                session_id=f"work_{int(time.time())}",
                start_time=datetime.now(),
                state=work_state
            )
            
            # 状況に応じた処理
            if work_state == WorkState.FIRST_TIME:
                success = await self._start_new_work(task_description, repo_path)
                message = self.messages['work_start']
            elif work_state == WorkState.CONTINUING:
                success = await self._continue_work(repo_path)
                message = self.messages['work_continue']
            else:
                success = await self._start_new_work(task_description, repo_path)
                message = self.messages['work_start']
                
            if success:
                # 自動保存タスクの開始
                await self._start_auto_save_task(repo_path)
                
                # 通知送信（同期版）
                if self.notifications:
                    self.notifications.info("作業開始", message)
                    
                self.stats['sessions_started'] += 1
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"作業開始エラー: {e}")
            await self._emergency_protection(repo_path)
            return False
            
    async def _analyze_work_situation(self, repo_path: str) -> WorkState:
        """現在の作業状況を分析"""
        try:
            context = await self.git_pro.get_git_context(repo_path)
            if not context:
                return WorkState.FIRST_TIME
                
            # メインブランチにいる場合
            if context.current_branch in ['main', 'master']:
                if context.is_dirty:
                    return WorkState.CONTINUING  # 未保存の作業あり
                else:
                    return WorkState.FIRST_TIME  # 新規作業
                    
            # 作業ブランチにいる場合
            else:
                return WorkState.CONTINUING
                
        except Exception as e:
            self.logger.error(f"状況分析エラー: {e}")
            return WorkState.FIRST_TIME
            
    async def _start_new_work(self, task_description: str, repo_path: str) -> bool:
        """新しい作業の開始"""
        try:
            # 作業フォルダ（ブランチ）の作成
            if task_description:
                # タスクから作業フォルダ名を生成
                folder_name = await self._generate_work_folder_name(task_description)
            else:
                # 汎用的な作業フォルダ名
                timestamp = datetime.now().strftime("%Y%m%d-%H%M")
                folder_name = f"work/{timestamp}"
                
            # Git Proエンジンでブランチ作成
            success = await self.git_pro.create_branch(folder_name, repo_path)
            
            if success:
                self.current_session.work_folder = folder_name
                self.stats['work_folders_created'] += 1
                
                # ユーザーフレンドリーな通知（同期版）
                if self.notifications:
                    self.notifications.success(
                        "作業フォルダ準備完了",
                        self.messages['work_folder_ready']
                    )
                return True
            else:
                # 既存フォルダで継続
                return await self._continue_work(repo_path)
                
        except Exception as e:
            self.logger.error(f"新規作業開始エラー: {e}")
            return False
            
    async def _continue_work(self, repo_path: str) -> bool:
        """既存作業の継続"""
        try:
            context = await self.git_pro.get_git_context(repo_path)
            if context:
                self.current_session.work_folder = context.current_branch
                return True
            return False
        except Exception as e:
            self.logger.error(f"作業継続エラー: {e}")
            return False
            
    async def _generate_work_folder_name(self, task_description: str) -> str:
        """タスクから分かりやすい作業フォルダ名を生成"""
        # 日本語を含む場合の処理
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', task_description):
            # 日本語を英語に簡略化
            if "実装" in task_description or "作成" in task_description:
                prefix = "feat"
            elif "修正" in task_description or "バグ" in task_description:
                prefix = "fix"
            elif "テスト" in task_description:
                prefix = "test"
            elif "実験" in task_description or "試す" in task_description:
                prefix = "exp"
            else:
                prefix = "work"
        else:
            # 英語の場合は既存ロジックを使用
            if self.git_pro and hasattr(self.git_pro, '_determine_branch_prefix'):
                prefix = self.git_pro._determine_branch_prefix(task_description, None)
            else:
                prefix = "work"
                
        # タイムスタンプ追加
        timestamp = datetime.now().strftime("%m%d-%H%M")
        return f"{prefix}/{timestamp}"
        
    async def _start_auto_save_task(self, repo_path: str):
        """自動保存タスクの開始"""
        if self.auto_save_task:
            self.auto_save_task.cancel()
            
        self.auto_save_task = asyncio.create_task(
            self._auto_save_loop(repo_path)
        )
        
    async def _auto_save_loop(self, repo_path: str):
        """自動保存のループ処理"""
        try:
            while self.current_session and self.enabled:
                await asyncio.sleep(self.auto_save_interval * 60)  # 分を秒に変換
                
                if self.current_session:
                    await self.auto_save(repo_path)
                    
        except asyncio.CancelledError:
            self.logger.info("自動保存タスクが停止されました")
        except Exception as e:
            self.logger.error(f"自動保存ループエラー: {e}")
            
    async def auto_save(self, repo_path: str = ".") -> bool:
        """自動保存の実行"""
        if not self.enabled or not self.git_pro or not self.current_session:
            return False
            
        try:
            context = await self.git_pro.get_git_context(repo_path)
            if not context:
                return False
                
            # 変更があるか、新しいファイルがあるかチェック
            has_changes = (context.is_dirty or 
                          context.untracked_files or 
                          context.staged_files or 
                          context.modified_files)
            
            if not has_changes:
                return False  # 何も変更がない場合はスキップ
                
            # 作業内容を自動保存（コミット）
            save_message = await self._generate_auto_save_message(context)
            
            # Git Proエンジンで自動コミット
            success = await self._safe_auto_commit(save_message, repo_path)
            
            if success:
                self.current_session.last_save = datetime.now()
                self.current_session.auto_saves += 1
                self.stats['auto_saves_performed'] += 1
                
                # ユーザーへの通知（同期版）
                if self.notifications:
                    self.notifications.info(
                        "自動保存",
                        self.messages['work_save']
                    )
                    
                self.logger.info("作業内容を自動保存しました")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"自動保存エラー: {e}")
            await self._emergency_protection(repo_path)
            return False
            
    async def _generate_auto_save_message(self, context) -> str:
        """自動保存用のメッセージ生成"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # すべての変更ファイルをカウント
        modified_count = len(context.modified_files) if context.modified_files else 0
        staged_count = len(context.staged_files) if context.staged_files else 0
        untracked_count = len(context.untracked_files) if context.untracked_files else 0
        
        total_count = modified_count + staged_count + untracked_count
        
        if total_count == 1:
            return f"作業中: {timestamp} - 1個のファイルを更新"
        else:
            return f"作業中: {timestamp} - {total_count}個のファイルを更新"
            
    async def _safe_auto_commit(self, message: str, repo_path: str) -> bool:
        """安全な自動コミットの実行"""
        try:
            # まず変更をステージング
            result = await asyncio.create_subprocess_exec(
                'git', 'add', '.',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            if result.returncode != 0:
                return False
                
            # コミット実行
            result = await asyncio.create_subprocess_exec(
                'git', 'commit', '-m', message,
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            return result.returncode == 0
            
        except Exception as e:
            self.logger.error(f"安全コミットエラー: {e}")
            return False
            
    async def complete_work(self, repo_path: str = ".") -> bool:
        """作業完了時の処理"""
        if not self.enabled or not self.current_session:
            return False
            
        try:
            # 自動保存タスクの停止
            if self.auto_save_task:
                self.auto_save_task.cancel()
                
            # 最終保存
            await self.auto_save(repo_path)
            
            # クラウドバックアップ（プッシュ）
            backup_success = await self._backup_to_cloud(repo_path)
            
            # セッション完了
            if self.current_session:
                self.current_session.state = WorkState.COMPLETING
                
            # 統計更新
            if backup_success:
                self.stats['backups_completed'] += 1
                
            # 通知（同期版）
            if self.notifications:
                if backup_success:
                    self.notifications.success(
                        "作業完了",
                        self.messages['work_complete']
                    )
                    self.notifications.info(
                        "バックアップ完了", 
                        self.messages['work_backup']
                    )
                else:
                    self.notifications.warning(
                        "作業完了",
                        "ローカル保存は完了しました（バックアップは後で実行されます）"
                    )
                    
            self.logger.info("作業完了処理が実行されました")
            self.current_session = None
            
            return True
            
        except Exception as e:
            self.logger.error(f"作業完了エラー: {e}")
            await self._emergency_protection(repo_path)
            return False
            
    async def _backup_to_cloud(self, repo_path: str) -> bool:
        """クラウドへのバックアップ（プッシュ）"""
        try:
            context = await self.git_pro.get_git_context(repo_path)
            if not context or not context.current_branch:
                return False
                
            # リモートの存在確認
            result = await asyncio.create_subprocess_exec(
                'git', 'remote', 'get-url', 'origin',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            if result.returncode != 0:
                self.logger.info("リモートリポジトリが設定されていません")
                return False
                
            # プッシュ実行
            result = await asyncio.create_subprocess_exec(
                'git', 'push', '-u', 'origin', context.current_branch,
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            return result.returncode == 0
            
        except Exception as e:
            self.logger.error(f"クラウドバックアップエラー: {e}")
            return False
            
    async def _emergency_protection(self, repo_path: str):
        """緊急時の作業保護"""
        try:
            self.stats['emergency_protections'] += 1
            
            # 緊急バックアップ作成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            emergency_branch = f"emergency_save_{timestamp}"
            
            # 現在の状態を緊急保存
            await asyncio.create_subprocess_exec(
                'git', 'add', '.',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await asyncio.create_subprocess_exec(
                'git', 'commit', '-m', f"緊急保存: {timestamp}",
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # 緊急通知（同期版）
            if self.notifications:
                self.notifications.warning(
                    "緊急保護",
                    self.messages['emergency_save']
                )
                
            self.logger.info(f"緊急保護を実行しました: {emergency_branch}")
            
        except Exception as e:
            self.logger.error(f"緊急保護エラー: {e}")
            
    async def _is_work_directory(self) -> bool:
        """作業ディレクトリかどうかの確認"""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'rev-parse', '--git-dir',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            return result.returncode == 0
        except Exception:
            return False
            
    async def _setup_work_directory(self):
        """作業ディレクトリのセットアップ"""
        try:
            # Git初期化
            result = await asyncio.create_subprocess_exec(
                'git', 'init',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            if result.returncode == 0:
                self.logger.info("新しい作業ディレクトリを設定しました")
            else:
                self.logger.warning("作業ディレクトリの設定に失敗しました")
                
        except Exception as e:
            self.logger.error(f"作業ディレクトリ設定エラー: {e}")
            
    def get_current_session_info(self) -> Optional[Dict]:
        """現在のセッション情報を取得"""
        if not self.current_session:
            return None
            
        return {
            'session_id': self.current_session.session_id,
            'start_time': self.current_session.start_time.isoformat(),
            'work_folder': self.current_session.work_folder,
            'auto_saves': self.current_session.auto_saves,
            'state': self.current_session.state.value
        }
        
    def get_stats(self) -> Dict:
        """統計情報を取得"""
        return self.stats.copy()
        
    async def cleanup(self):
        """リソースのクリーンアップ"""
        if self.auto_save_task:
            self.auto_save_task.cancel()
            
        if self.current_session:
            self.logger.info(f"セッション終了: {self.current_session.session_id}")
            
        self.logger.info(f"透明作業保護システム終了 - 統計: {self.stats}")


# 使用例とテスト
async def test_transparent_git():
    """透明Gitエンジンのテスト"""
    engine = TransparentGitEngine()
    
    # テスト設定
    config = {
        'transparent_git': {
            'enabled': True,
            'auto_save_interval': 1  # 1分（テスト用）
        }
    }
    
    await engine.initialize(config)
    
    print("透明作業保護システムのテスト:")
    print("-" * 40)
    
    # 作業開始のテスト
    success = await engine.start_work("テスト機能を実装")
    print(f"作業開始: {'成功' if success else '失敗'}")
    
    # セッション情報の表示
    info = engine.get_current_session_info()
    if info:
        print(f"セッション情報: {info}")
        
    # 統計情報の表示
    stats = engine.get_stats()
    print(f"統計: {stats}")
    
    await engine.cleanup()


if __name__ == "__main__":
    asyncio.run(test_transparent_git())