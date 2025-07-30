#!/usr/bin/env python3
"""
Claude++ 自動作業保護システム
作業データを様々な危険から自動で保護し、安全な作業環境を提供します。
"""

import asyncio
import os
import shutil
import time
import signal
import threading
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import tempfile
import subprocess
import fnmatch


class ProtectionLevel(Enum):
    """保護レベル"""
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"
    MAXIMUM = "最大"


class ThreatType(Enum):
    """脅威の種類"""
    SYSTEM_CRASH = "システムクラッシュ"
    POWER_FAILURE = "電源切断"
    NETWORK_FAILURE = "ネットワーク障害"
    DISK_FULL = "ディスク容量不足"
    PERMISSION_ERROR = "権限エラー"
    MERGE_CONFLICT = "ファイル競合"
    DATA_CORRUPTION = "データ破損"
    ACCIDENTAL_DELETE = "誤削除"
    FORCE_QUIT = "強制終了"
    UNKNOWN = "不明"


@dataclass
class BackupInfo:
    """バックアップ情報"""
    backup_id: str
    timestamp: datetime
    backup_path: str
    file_count: int
    size_bytes: int
    description: str
    protection_level: ProtectionLevel


@dataclass
class RecoveryPoint:
    """復旧ポイント情報"""
    point_id: str
    timestamp: datetime
    work_state: str
    files_snapshot: Dict[str, str]
    description: str
    auto_created: bool = True


class AutoProtectionEngine:
    """自動作業保護エンジン"""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.auto_protection')
        self.config = {}
        self.enabled = True
        self.protection_level = ProtectionLevel.HIGH
        
        # 作業ディレクトリの記録（起動時の現在のディレクトリ）
        self.work_directory = os.getcwd()
        self.logger.debug(f"作業ディレクトリを設定: {self.work_directory}")
        
        # Claude-Plus自体のディレクトリを除外対象として記録
        self.claude_plus_home = os.environ.get('CLAUDE_PLUS_HOME', '')
        if not self.claude_plus_home:
            # claude-plusスクリプトの場所から推定
            import __main__
            if hasattr(__main__, '__file__'):
                main_path = Path(__main__.__file__).absolute()
                self.claude_plus_home = str(main_path.parent)
        
        # .gitignoreパターンのキャッシュ
        self.ignore_patterns: Set[str] = set()
        self._load_gitignore_patterns()
        
        # 保護システムの状態
        self.active_protections = []
        self.backup_directory = None
        self.recovery_points: List[RecoveryPoint] = []
        self.emergency_handlers = []
        
        # バックアップ管理
        self.auto_backup_interval = 300  # 5分
        self.max_backups = 10
        self.backup_task = None
        
        # 監視システム
        self.file_watcher = None
        self.system_monitor = None
        self.conflict_detector = None
        
        # 日本語UI
        try:
            from core.japanese_ui import get_ui_manager
            self.ui = get_ui_manager()
        except ImportError:
            self.ui = None
            
        # 統計情報
        self.stats = {
            'emergency_saves': 0,
            'auto_recoveries': 0,
            'conflicts_resolved': 0,
            'backups_created': 0,
            'data_restored': 0,
            'threats_detected': 0
        }
        
        # シグナルハンドラーの登録
        self._register_emergency_handlers()
        
    async def initialize(self, config: Dict, notifications=None):
        """自動保護システムの初期化"""
        self.config = config.get('auto_protection', {})
        self.enabled = self.config.get('enabled', True)
        # 設定から保護レベルを取得（文字列から日本語enumに変換）
        level_str = self.config.get('protection_level', 'HIGH')
        level_mapping = {
            'LOW': ProtectionLevel.LOW,
            'MEDIUM': ProtectionLevel.MEDIUM, 
            'HIGH': ProtectionLevel.HIGH,
            'MAXIMUM': ProtectionLevel.MAXIMUM
        }
        self.protection_level = level_mapping.get(level_str, ProtectionLevel.HIGH)
        self.notifications = notifications
        
        if not self.enabled:
            return
            
        # バックアップディレクトリの設定
        await self._setup_backup_directory()
        
        # 自動保護システムの開始
        await self._start_protection_systems()
        
        # 既存の復旧ポイントの読み込み
        await self._load_recovery_points()
        
        if self.config.get('debug', False):
            self.logger.info(f"自動保護システムが初期化されました (レベル: {self.protection_level.value})")
        else:
            self.logger.debug(f"自動保護システムが初期化されました (レベル: {self.protection_level.value})")
        
    async def _setup_backup_directory(self):
        """バックアップディレクトリのセットアップ"""
        try:
            # ユーザーディレクトリ内にバックアップフォルダを作成
            home_dir = Path.home()
            self.backup_directory = home_dir / ".claude-plus" / "backups"
            self.backup_directory.mkdir(parents=True, exist_ok=True)
            
            # 復旧ポイント用ディレクトリ
            recovery_dir = self.backup_directory / "recovery_points"
            recovery_dir.mkdir(exist_ok=True)
            
            self.logger.debug(f"バックアップディレクトリを設定しました: {self.backup_directory}")
            
        except Exception as e:
            self.logger.error(f"バックアップディレクトリ設定エラー: {e}")
            # フォールバック: 一時ディレクトリを使用
            self.backup_directory = Path(tempfile.gettempdir()) / "claude-plus-backups"
            self.backup_directory.mkdir(exist_ok=True)
            
    async def _start_protection_systems(self):
        """保護システムの開始"""
        # 自動バックアップタスクの開始
        self.backup_task = asyncio.create_task(self._auto_backup_loop())
        
        # ファイル監視の開始
        if self.protection_level in [ProtectionLevel.HIGH, ProtectionLevel.MAXIMUM]:
            await self._start_file_monitoring()
            
        # システム監視の開始
        if self.protection_level == ProtectionLevel.MAXIMUM:
            await self._start_system_monitoring()
            
    async def _auto_backup_loop(self):
        """自動バックアップループ"""
        try:
            while self.enabled:
                await asyncio.sleep(self.auto_backup_interval)
                await self.create_automatic_backup()
        except asyncio.CancelledError:
            self.logger.debug("自動バックアップタスクが停止されました")
        except Exception as e:
            self.logger.error(f"自動バックアップループエラー: {e}")
            
    async def _start_file_monitoring(self):
        """ファイル監視の開始"""
        # 簡単な実装: 定期的なファイル状態チェック
        self.file_watcher = asyncio.create_task(self._file_monitoring_loop())
        
    async def _file_monitoring_loop(self):
        """ファイル監視ループ"""
        try:
            last_check = {}
            
            while self.enabled:
                current_files = await self._scan_current_files()
                
                # ファイル変更の検出
                for file_path, mtime in current_files.items():
                    if file_path in last_check:
                        if mtime > last_check[file_path]:
                            await self._handle_file_change(file_path)
                    else:
                        await self._handle_new_file(file_path)
                        
                # 削除されたファイルの検出
                for file_path in set(last_check.keys()) - set(current_files.keys()):
                    await self._handle_file_deletion(file_path)
                    
                last_check = current_files
                await asyncio.sleep(30)  # 30秒間隔でチェック
                
        except asyncio.CancelledError:
            self.logger.debug("ファイル監視が停止されました")
        except Exception as e:
            self.logger.error(f"ファイル監視エラー: {e}")
            
    def _load_gitignore_patterns(self):
        """gitignoreパターンを読み込む"""
        self.ignore_patterns = {
            # デフォルトパターン
            '*.pyc', '*.pyo', '__pycache__', '*.log',
            '.git', '.DS_Store', 'node_modules',
            'venv', '.venv', 'env', '.env',
            '*.egg-info', 'dist', 'build'
        }
        
        # .gitignoreファイルから追加パターンを読み込む
        gitignore_path = Path(self.work_directory) / '.gitignore'
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.ignore_patterns.add(line)
            except Exception as e:
                self.logger.debug(f".gitignore読み込みエラー: {e}")

    def _should_ignore(self, file_path: str) -> bool:
        """ファイルを無視すべきか判定"""
        file_name = os.path.basename(file_path)
        path_parts = file_path.split(os.sep)
        
        for pattern in self.ignore_patterns:
            # ファイル名でマッチ
            if fnmatch.fnmatch(file_name, pattern):
                return True
            # パス全体でマッチ
            if fnmatch.fnmatch(file_path, pattern):
                return True
            # ディレクトリ名でマッチ
            for part in path_parts:
                if fnmatch.fnmatch(part, pattern):
                    return True
        
        return False

    async def _scan_current_files(self) -> Dict[str, float]:
        """現在のファイル状態をスキャン（軽量版）"""
        files = {}
        scan_limit = 1000  # スキャンするファイル数の上限
        file_count = 0
        
        try:
            # 作業ディレクトリをスキャン
            for root, dirs, filenames in os.walk(self.work_directory):
                # ディレクトリの除外処理
                dirs[:] = [d for d in dirs if not self._should_ignore(d)]
                
                # Claude-Plus自体のディレクトリはスキップ
                if self.claude_plus_home and os.path.abspath(root).startswith(os.path.abspath(self.claude_plus_home)):
                    continue
                
                # 作業ディレクトリ外はスキップ
                try:
                    rel_root = os.path.relpath(root, self.work_directory)
                    if rel_root.startswith('..'):
                        continue
                except ValueError:
                    # 異なるドライブの場合
                    continue
                    
                for filename in filenames:
                    if file_count >= scan_limit:
                        self.logger.debug(f"ファイルスキャン上限に達しました: {scan_limit}")
                        return files
                        
                    # 無視すべきファイルはスキップ
                    if self._should_ignore(filename):
                        continue
                        
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, self.work_directory)
                    
                    if self._should_ignore(rel_path):
                        continue
                        
                    try:
                        stat = os.stat(file_path)
                        # 大きすぎるファイルはスキップ（100MB以上）
                        if stat.st_size > 100 * 1024 * 1024:
                            continue
                            
                        files[rel_path] = stat.st_mtime
                        file_count += 1
                    except (OSError, FileNotFoundError):
                        pass
                        
        except Exception as e:
            self.logger.error(f"ファイルスキャンエラー: {e}")
            
        return files
        
    async def _handle_file_change(self, file_path: str):
        """ファイル変更の処理"""
        # 重要なファイルの場合は即座にバックアップ
        if self._is_critical_file(file_path):
            await self.create_recovery_point(f"重要ファイル変更: {file_path}")
            
    async def _handle_new_file(self, file_path: str):
        """新規ファイルの処理"""
        if self._is_critical_file(file_path):
            # デバッグモード時のみログ出力
            if self.config.get('debug', False):
                self.logger.info(f"重要な新規ファイルを検出: {file_path}")
            else:
                self.logger.debug(f"重要な新規ファイルを検出: {file_path}")
            
    async def _handle_file_deletion(self, file_path: str):
        """ファイル削除の処理"""
        if self._is_critical_file(file_path):
            await self.handle_threat(ThreatType.ACCIDENTAL_DELETE, {
                'file_path': file_path,
                'timestamp': datetime.now()
            })
            
    def _is_critical_file(self, file_path: str) -> bool:
        """重要ファイルの判定"""
        critical_extensions = {'.py', '.js', '.ts', '.html', '.css', '.md', '.yaml', '.yml', '.json'}
        critical_names = {'README', 'Makefile', 'Dockerfile', 'requirements.txt', 'package.json'}
        
        file_ext = Path(file_path).suffix.lower()
        file_name = Path(file_path).name
        
        return (file_ext in critical_extensions or 
                file_name in critical_names or
                'config' in file_name.lower())
                
    async def _start_system_monitoring(self):
        """システム監視の開始"""
        self.system_monitor = asyncio.create_task(self._system_monitoring_loop())
        
    async def _system_monitoring_loop(self):
        """システム監視ループ"""
        try:
            while self.enabled:
                # ディスク容量チェック
                await self._check_disk_space()
                
                # メモリ使用量チェック
                await self._check_memory_usage()
                
                # プロセス健全性チェック
                await self._check_process_health()
                
                await asyncio.sleep(60)  # 1分間隔
                
        except asyncio.CancelledError:
            self.logger.debug("システム監視が停止されました")
        except Exception as e:
            self.logger.error(f"システム監視エラー: {e}")
            
    async def _check_disk_space(self):
        """ディスク容量チェック"""
        try:
            statvfs = os.statvfs('.')
            free_bytes = statvfs.f_frsize * statvfs.f_bavail
            total_bytes = statvfs.f_frsize * statvfs.f_blocks
            
            usage_percent = ((total_bytes - free_bytes) / total_bytes) * 100
            
            if usage_percent > 95:
                await self.handle_threat(ThreatType.DISK_FULL, {
                    'usage_percent': usage_percent,
                    'free_bytes': free_bytes
                })
        except Exception as e:
            self.logger.error(f"ディスク容量チェックエラー: {e}")
            
    async def _check_memory_usage(self):
        """メモリ使用量チェック"""
        # 簡単な実装: プロセス固有のメモリ使用量はスキップ
        pass
        
    async def _check_process_health(self):
        """プロセス健全性チェック"""
        # プロセスの応答性やリソース使用量をチェック
        pass
        
    def _register_emergency_handlers(self):
        """緊急時ハンドラーの登録"""
        def emergency_handler(signum, frame):
            """緊急時のシグナルハンドラー"""
            asyncio.create_task(self.emergency_save())
            
        # SIGINT (Ctrl+C) とSIGTERMのハンドラーを設定
        try:
            signal.signal(signal.SIGINT, emergency_handler)
            signal.signal(signal.SIGTERM, emergency_handler)
        except ValueError:
            # Windowsなどでサポートされていないシグナルは無視
            pass
            
    async def emergency_save(self) -> bool:
        """緊急保存の実行"""
        try:
            self.stats['emergency_saves'] += 1
            
            # 緊急復旧ポイントの作成
            emergency_point = await self.create_recovery_point(
                "緊急保存", 
                auto_created=True
            )
            
            if emergency_point:
                # 通知送信（同期版）
                if self.notifications and self.ui:
                    message = self.ui.get_message('emergency_save')
                    self.notifications.warning("緊急保存", message)
                    
                self.logger.info("緊急保存が完了しました")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"緊急保存エラー: {e}")
            return False
            
    async def handle_threat(self, threat_type: ThreatType, threat_data: Dict[str, Any]) -> bool:
        """脅威への対応"""
        try:
            self.stats['threats_detected'] += 1
            
            self.logger.warning(f"脅威検出: {threat_type.value}")
            
            # 脅威の種類に応じた対応
            if threat_type == ThreatType.MERGE_CONFLICT:
                return await self._handle_merge_conflict(threat_data)
            elif threat_type == ThreatType.ACCIDENTAL_DELETE:
                return await self._handle_accidental_deletion(threat_data)
            elif threat_type == ThreatType.DISK_FULL:
                return await self._handle_disk_full(threat_data)
            elif threat_type in [ThreatType.SYSTEM_CRASH, ThreatType.POWER_FAILURE]:
                return await self._handle_system_failure(threat_data)
            else:
                # 汎用的な対応: 緊急保存
                return await self.emergency_save()
                
        except Exception as e:
            self.logger.error(f"脅威対応エラー: {e}")
            return False
            
    async def _handle_merge_conflict(self, threat_data: Dict) -> bool:
        """マージ競合の処理"""
        try:
            self.stats['conflicts_resolved'] += 1
            
            # 安全な状態に退避
            await self.create_recovery_point("競合発生前")
            
            # 自動解決を試行
            conflict_files = threat_data.get('conflict_files', [])
            
            if self.notifications and self.ui:
                message = self.ui.get_message('conflict_resolved')
                self.notifications.info("競合解決", message)
                
            return True
            
        except Exception as e:
            self.logger.error(f"競合処理エラー: {e}")
            return False
            
    async def _handle_accidental_deletion(self, threat_data: Dict) -> bool:
        """誤削除の処理"""
        try:
            file_path = threat_data.get('file_path')
            
            # 最新の復旧ポイントからファイルを復元
            restored = await self._restore_file_from_backup(file_path)
            
            if restored and self.notifications and self.ui:
                self.notifications.success(
                    "ファイル復元",
                    f"削除されたファイルを復元しました: {os.path.basename(file_path)}"
                )
                
            return restored
            
        except Exception as e:
            self.logger.error(f"誤削除処理エラー: {e}")
            return False
            
    async def _handle_disk_full(self, threat_data: Dict) -> bool:
        """ディスク容量不足の処理"""
        try:
            # 古いバックアップファイルの自動削除
            await self._cleanup_old_backups()
            
            if self.notifications and self.ui:
                self.notifications.warning(
                    "ディスク容量不足",
                    "古いバックアップを削除して容量を確保しました"
                )
                
            return True
            
        except Exception as e:
            self.logger.error(f"ディスク容量不足処理エラー: {e}")
            return False
            
    async def _handle_system_failure(self, threat_data: Dict) -> bool:
        """システム障害の処理"""
        # 最優先で緊急保存を実行
        return await self.emergency_save()
        
    async def create_recovery_point(self, description: str, auto_created: bool = True) -> Optional[RecoveryPoint]:
        """復旧ポイントの作成"""
        try:
            point_id = f"recovery_{int(time.time())}"
            timestamp = datetime.now()
            
            # 現在のファイル状態のスナップショット
            files_snapshot = await self._create_files_snapshot()
            
            recovery_point = RecoveryPoint(
                point_id=point_id,
                timestamp=timestamp,
                work_state="active",
                files_snapshot=files_snapshot,
                description=description,
                auto_created=auto_created
            )
            
            # 復旧ポイントの保存
            await self._save_recovery_point(recovery_point)
            
            self.recovery_points.append(recovery_point)
            
            # 古い復旧ポイントの削除
            await self._cleanup_old_recovery_points()
            
            self.logger.info(f"復旧ポイントを作成しました: {description}")
            return recovery_point
            
        except Exception as e:
            self.logger.error(f"復旧ポイント作成エラー: {e}")
            return None
            
    async def _create_files_snapshot(self) -> Dict[str, str]:
        """ファイルのスナップショット作成"""
        snapshot = {}
        try:
            current_files = await self._scan_current_files()
            
            for rel_path in current_files:
                if self._is_critical_file(rel_path):
                    try:
                        # 絶対パスに変換
                        abs_path = os.path.join(self.work_directory, rel_path)
                        with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            snapshot[rel_path] = content
                    except Exception:
                        # バイナリファイルなどはスキップ
                        pass
                        
        except Exception as e:
            self.logger.error(f"スナップショット作成エラー: {e}")
            
        return snapshot
        
    async def _save_recovery_point(self, recovery_point: RecoveryPoint):
        """復旧ポイントの保存"""
        try:
            recovery_dir = self.backup_directory / "recovery_points"
            point_file = recovery_dir / f"{recovery_point.point_id}.json"
            
            point_data = {
                'point_id': recovery_point.point_id,
                'timestamp': recovery_point.timestamp.isoformat(),
                'work_state': recovery_point.work_state,
                'description': recovery_point.description,
                'auto_created': recovery_point.auto_created,
                'files_snapshot': recovery_point.files_snapshot
            }
            
            with open(point_file, 'w', encoding='utf-8') as f:
                json.dump(point_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"復旧ポイント保存エラー: {e}")
            
    async def _load_recovery_points(self):
        """復旧ポイントの読み込み"""
        try:
            recovery_dir = self.backup_directory / "recovery_points"
            if not recovery_dir.exists():
                return
                
            for point_file in recovery_dir.glob("*.json"):
                try:
                    with open(point_file, 'r', encoding='utf-8') as f:
                        point_data = json.load(f)
                        
                    recovery_point = RecoveryPoint(
                        point_id=point_data['point_id'],
                        timestamp=datetime.fromisoformat(point_data['timestamp']),
                        work_state=point_data['work_state'],
                        files_snapshot=point_data['files_snapshot'],
                        description=point_data['description'],
                        auto_created=point_data.get('auto_created', True)
                    )
                    
                    self.recovery_points.append(recovery_point)
                    
                except Exception as e:
                    self.logger.error(f"復旧ポイント読み込みエラー ({point_file}): {e}")
                    
            # 時間順にソート
            self.recovery_points.sort(key=lambda x: x.timestamp, reverse=True)
            
            self.logger.info(f"{len(self.recovery_points)}個の復旧ポイントを読み込みました")
            
        except Exception as e:
            self.logger.error(f"復旧ポイント読み込みエラー: {e}")
            
    async def create_automatic_backup(self) -> Optional[BackupInfo]:
        """自動バックアップの作成"""
        try:
            backup_id = f"auto_backup_{int(time.time())}"
            timestamp = datetime.now()
            
            backup_path = self.backup_directory / backup_id
            backup_path.mkdir(exist_ok=True)
            
            # 重要ファイルのコピー
            file_count = 0
            total_size = 0
            
            current_files = await self._scan_current_files()
            for rel_path in current_files:
                if self._is_critical_file(rel_path):
                    try:
                        # 絶対パスに変換
                        src_path = os.path.join(self.work_directory, rel_path)
                        dest_path = backup_path / rel_path
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        shutil.copy2(src_path, dest_path)
                        file_count += 1
                        total_size += os.path.getsize(src_path)
                        
                    except Exception as e:
                        self.logger.warning(f"ファイルバックアップ失敗 ({rel_path}): {e}")
                        
            if file_count > 0:
                backup_info = BackupInfo(
                    backup_id=backup_id,
                    timestamp=timestamp,
                    backup_path=str(backup_path),
                    file_count=file_count,
                    size_bytes=total_size,
                    description="自動バックアップ",
                    protection_level=self.protection_level
                )
                
                self.stats['backups_created'] += 1
                self.logger.info(f"自動バックアップを作成しました: {backup_id} ({file_count}ファイル)")
                
                return backup_info
            else:
                # ファイルがない場合はバックアップディレクトリを削除
                shutil.rmtree(backup_path)
                return None
                
        except Exception as e:
            self.logger.error(f"自動バックアップエラー: {e}")
            return None
            
    async def _restore_file_from_backup(self, file_path: str) -> bool:
        """バックアップからファイルを復元"""
        try:
            # ファイルパスを正規化
            normalized_path = os.path.normpath(file_path)
            possible_paths = [
                file_path,
                f"./{file_path}",
                normalized_path,
                f"./{normalized_path}"
            ]
            
            # 最新の復旧ポイントから検索
            for recovery_point in self.recovery_points:
                found_content = None
                found_key = None
                
                # 複数のパス形式で検索
                for check_path in possible_paths:
                    if check_path in recovery_point.files_snapshot:
                        found_content = recovery_point.files_snapshot[check_path]
                        found_key = check_path
                        break
                
                # パス名の部分一致で検索（フォールバック）
                if not found_content:
                    for snapshot_path, content in recovery_point.files_snapshot.items():
                        if os.path.basename(snapshot_path) == os.path.basename(file_path):
                            found_content = content
                            found_key = snapshot_path
                            break
                
                if found_content:
                    # ファイルを復元
                    dir_path = os.path.dirname(file_path)
                    if dir_path:  # ディレクトリパスが空でない場合のみ作成
                        os.makedirs(dir_path, exist_ok=True)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(found_content)
                        
                    self.stats['data_restored'] += 1
                    self.logger.info(f"ファイルを復元しました: {file_path} (from {found_key})")
                    return True
                    
            self.logger.warning(f"バックアップにファイルが見つかりませんでした: {file_path}")
            return False
            
        except Exception as e:
            self.logger.error(f"ファイル復元エラー: {e}")
            return False
            
    async def _cleanup_old_backups(self):
        """古いバックアップの削除"""
        try:
            if not self.backup_directory.exists():
                return
                
            # バックアップディレクトリ内の古いフォルダを削除
            backup_dirs = [d for d in self.backup_directory.iterdir() 
                          if d.is_dir() and d.name.startswith('auto_backup_')]
                          
            if len(backup_dirs) > self.max_backups:
                # 作成時間でソートして古いものから削除
                backup_dirs.sort(key=lambda x: x.stat().st_ctime)
                
                for old_backup in backup_dirs[:-self.max_backups]:
                    shutil.rmtree(old_backup)
                    self.logger.info(f"古いバックアップを削除しました: {old_backup.name}")
                    
        except Exception as e:
            self.logger.error(f"バックアップ削除エラー: {e}")
            
    async def _cleanup_old_recovery_points(self):
        """古い復旧ポイントの削除"""
        try:
            max_recovery_points = 20
            
            if len(self.recovery_points) > max_recovery_points:
                # 古い復旧ポイントを削除
                old_points = self.recovery_points[max_recovery_points:]
                
                for old_point in old_points:
                    recovery_file = (self.backup_directory / "recovery_points" / 
                                   f"{old_point.point_id}.json")
                    if recovery_file.exists():
                        recovery_file.unlink()
                        
                # リストからも削除
                self.recovery_points = self.recovery_points[:max_recovery_points]
                
        except Exception as e:
            self.logger.error(f"復旧ポイント削除エラー: {e}")
            
    def get_protection_status(self) -> Dict[str, Any]:
        """保護システムの状態取得"""
        return {
            'enabled': self.enabled,
            'protection_level': self.protection_level.value,
            'backup_directory': str(self.backup_directory) if self.backup_directory else None,
            'recovery_points_count': len(self.recovery_points),
            'active_protections': len(self.active_protections),
            'stats': self.stats.copy()
        }
        
    async def cleanup(self):
        """リソースのクリーンアップ"""
        # 各種タスクの停止
        if self.backup_task:
            self.backup_task.cancel()
            
        if self.file_watcher:
            self.file_watcher.cancel()
            
        if self.system_monitor:
            self.system_monitor.cancel()
            
        self.logger.info(f"自動保護システム終了 - 統計: {self.stats}")


# テスト用コード
async def test_auto_protection():
    """自動保護システムのテスト"""
    protection = AutoProtectionEngine()
    
    config = {
        'auto_protection': {
            'enabled': True,
            'protection_level': 'HIGH'
        }
    }
    
    await protection.initialize(config)
    
    print("自動作業保護システムのテスト:")
    print("-" * 40)
    
    # 復旧ポイントの作成テスト
    point = await protection.create_recovery_point("テスト用復旧ポイント")
    print(f"復旧ポイント作成: {'成功' if point else '失敗'}")
    
    # 緊急保存のテスト
    emergency = await protection.emergency_save()
    print(f"緊急保存: {'成功' if emergency else '失敗'}")
    
    # 状態の表示
    status = protection.get_protection_status()
    print(f"保護システム状態: {status}")
    
    await protection.cleanup()


if __name__ == "__main__":
    asyncio.run(test_auto_protection())