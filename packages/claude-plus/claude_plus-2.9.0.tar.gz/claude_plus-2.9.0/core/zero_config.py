#!/usr/bin/env python3
"""
Claude++ ゼロ設定システム
ユーザーが何も設定しなくても最適な動作を自動提供する完全自動化システム
"""

import asyncio
import os
import json
import logging
import platform
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import re


class ProjectType(Enum):
    """プロジェクトタイプ"""
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    TYPESCRIPT = "TypeScript"
    WEB = "Web"
    DATA_SCIENCE = "データサイエンス"
    DOCUMENTATION = "ドキュメント"
    CONFIG = "設定ファイル"
    MIXED = "複合プロジェクト"
    UNKNOWN = "不明"


class UserLevel(Enum):
    """ユーザーレベル"""
    BEGINNER = "初心者"
    INTERMEDIATE = "中級者"
    ADVANCED = "上級者"


class WorkPattern(Enum):
    """作業パターン"""
    FREQUENT_SHORT = "頻繁な短時間作業"
    LONG_SESSION = "長時間集中作業"
    EXPERIMENTAL = "実験的作業"
    MAINTENANCE = "保守・修正作業"
    COLLABORATIVE = "協調作業"


@dataclass
class ProjectProfile:
    """プロジェクトプロファイル"""
    project_type: ProjectType
    languages: List[str]
    frameworks: List[str]
    tools: List[str]
    file_count: int
    main_files: List[str]
    has_tests: bool
    has_docs: bool
    estimated_complexity: str


@dataclass
class UserProfile:
    """ユーザープロファイル"""
    user_level: UserLevel
    work_pattern: WorkPattern
    preferred_language: str
    session_frequency: float  # sessions per day
    average_session_duration: float  # minutes
    commit_frequency: float  # commits per session
    error_recovery_success_rate: float
    last_updated: datetime


@dataclass
class OptimalConfig:
    """最適化された設定"""
    auto_save_interval: int  # minutes
    backup_frequency: int  # minutes
    protection_level: str
    notification_verbosity: str
    auto_commit_threshold: int  # changes count
    conflict_resolution_style: str
    help_message_frequency: str


class ZeroConfigManager:
    """ゼロ設定管理システム - 完全自動設定"""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.zero_config')
        self.config_dir = Path.home() / ".claude-plus"
        self.config_dir.mkdir(exist_ok=True)
        
        # プロファイルファイル
        self.project_profile_file = self.config_dir / "project_profile.json"
        self.user_profile_file = self.config_dir / "user_profile.json"
        self.learning_data_file = self.config_dir / "learning_data.json"
        
        # 現在のプロファイル
        self.project_profile: Optional[ProjectProfile] = None
        self.user_profile: Optional[UserProfile] = None
        self.optimal_config: Optional[OptimalConfig] = None
        
        # 学習データ
        self.learning_data = {
            'session_history': [],
            'error_patterns': [],
            'success_patterns': [],
            'user_preferences': {}
        }
        
        # 日本語UI
        try:
            from core.japanese_ui import get_ui_manager
            self.ui = get_ui_manager()
        except ImportError:
            self.ui = None
            
    async def initialize(self, work_directory: str = ".") -> Dict[str, Any]:
        """ゼロ設定システムの初期化 - 完全自動"""
        try:
            self.logger.info("ゼロ設定システムを初期化中...")
            
            # 学習データの読み込み
            self._load_learning_data()
            
            # プロジェクト環境の自動検出
            self.project_profile = await self._detect_project_environment(work_directory)
            
            # ユーザープロファイルの自動生成/更新
            self.user_profile = await self._analyze_user_profile()
            
            # 最適設定の自動生成
            self.optimal_config = self._generate_optimal_config()
            
            # 設定の保存
            self._save_profiles()
            
            # 初回セットアップの実行（必要に応じて）
            await self._perform_first_time_setup(work_directory)
            
            # 生成された設定をdict形式で返す
            config_dict = self._generate_config_dict()
            
            self.logger.info("ゼロ設定システムの初期化が完了しました")
            return config_dict
            
        except Exception as e:
            self.logger.error(f"ゼロ設定初期化エラー: {e}")
            # フォールバック: デフォルト設定
            return self._get_default_config()
            
    async def _detect_project_environment(self, work_directory: str) -> ProjectProfile:
        """プロジェクト環境の自動検出"""
        try:
            work_path = Path(work_directory)
            
            # ファイルスキャン
            all_files = []
            for file_path in work_path.rglob("*"):
                if file_path.is_file() and not self._should_ignore_file(file_path):
                    all_files.append(file_path)
                    
            # プログラミング言語の検出
            languages = self._detect_languages(all_files)
            
            # プロジェクトタイプの判定
            project_type = self._determine_project_type(all_files, languages)
            
            # フレームワークの検出
            frameworks = self._detect_frameworks(all_files)
            
            # ツールの検出
            tools = self._detect_tools(all_files)
            
            # メインファイルの特定
            main_files = self._identify_main_files(all_files)
            
            # テスト・ドキュメントの有無
            has_tests = self._has_test_files(all_files)
            has_docs = self._has_documentation(all_files)
            
            # 複雑度の推定
            complexity = self._estimate_complexity(all_files, languages)
            
            profile = ProjectProfile(
                project_type=project_type,
                languages=languages,
                frameworks=frameworks,
                tools=tools,
                file_count=len(all_files),
                main_files=main_files,
                has_tests=has_tests,
                has_docs=has_docs,
                estimated_complexity=complexity
            )
            
            self.logger.info(f"プロジェクト環境を検出: {project_type.value} ({len(languages)}言語)")
            return profile
            
        except Exception as e:
            self.logger.error(f"プロジェクト環境検出エラー: {e}")
            # フォールバック
            return ProjectProfile(
                project_type=ProjectType.UNKNOWN,
                languages=["text"],
                frameworks=[],
                tools=[],
                file_count=0,
                main_files=[],
                has_tests=False,
                has_docs=False,
                estimated_complexity="simple"
            )
            
    def _should_ignore_file(self, file_path: Path) -> bool:
        """無視すべきファイルの判定"""
        ignore_patterns = {
            '.git', '__pycache__', 'node_modules', '.DS_Store',
            '.pytest_cache', '.vscode', '.idea', 'dist', 'build'
        }
        
        # 隠しファイル・ディレクトリをチェック
        for part in file_path.parts:
            if part in ignore_patterns or part.startswith('.'):
                return True
                
        # 大きすぎるファイルを無視
        try:
            if file_path.stat().st_size > 10 * 1024 * 1024:  # 10MB
                return True
        except (OSError, FileNotFoundError):
            return True
            
        return False
        
    def _detect_languages(self, files: List[Path]) -> List[str]:
        """プログラミング言語の検出"""
        language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.dart': 'Dart',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.json': 'JSON',
            '.xml': 'XML',
            '.md': 'Markdown',
            '.tex': 'LaTeX'
        }
        
        detected = {}
        for file_path in files:
            ext = file_path.suffix.lower()
            if ext in language_extensions:
                lang = language_extensions[ext]
                detected[lang] = detected.get(lang, 0) + 1
                
        # ファイル数の多い順にソート
        sorted_languages = sorted(detected.items(), key=lambda x: x[1], reverse=True)
        return [lang for lang, count in sorted_languages if count > 0]
        
    def _determine_project_type(self, files: List[Path], languages: List[str]) -> ProjectType:
        """プロジェクトタイプの判定"""
        file_names = [f.name.lower() for f in files]
        
        # 特定ファイルによる判定
        if 'package.json' in file_names:
            return ProjectType.JAVASCRIPT
        elif 'requirements.txt' in file_names or 'setup.py' in file_names:
            return ProjectType.PYTHON
        elif 'tsconfig.json' in file_names:
            return ProjectType.TYPESCRIPT
        elif any('jupyter' in name or '.ipynb' in name for name in file_names):
            return ProjectType.DATA_SCIENCE
            
        # 言語による判定
        if not languages:
            return ProjectType.UNKNOWN
            
        primary_language = languages[0]
        
        if primary_language == 'Python':
            # データサイエンス的なファイルがあるかチェック
            data_science_indicators = ['pandas', 'numpy', 'matplotlib', 'sklearn', 'tensorflow']
            for file_path in files:
                if file_path.suffix == '.py':
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        if any(indicator in content for indicator in data_science_indicators):
                            return ProjectType.DATA_SCIENCE
                    except Exception:
                        pass
            return ProjectType.PYTHON
            
        elif primary_language in ['JavaScript', 'TypeScript']:
            if 'HTML' in languages or 'CSS' in languages:
                return ProjectType.WEB
            return ProjectType.JAVASCRIPT
            
        elif primary_language == 'Markdown':
            return ProjectType.DOCUMENTATION
            
        elif len(languages) > 3:
            return ProjectType.MIXED
            
        return ProjectType.UNKNOWN
        
    def _detect_frameworks(self, files: List[Path]) -> List[str]:
        """フレームワークの検出"""
        frameworks = set()
        
        for file_path in files:
            name = file_path.name.lower()
            
            # 設定ファイルによる検出
            framework_files = {
                'package.json': ['react', 'vue', 'angular', 'express', 'next'],
                'requirements.txt': ['django', 'flask', 'fastapi', 'pytorch', 'tensorflow'],
                'pom.xml': ['spring'],
                'composer.json': ['laravel', 'symfony'],
                'cargo.toml': ['actix', 'rocket'],
                'go.mod': ['gin', 'echo']
            }
            
            if name in framework_files:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for framework in framework_files[name]:
                        if framework in content.lower():
                            frameworks.add(framework)
                except Exception:
                    pass
                    
        return list(frameworks)
        
    def _detect_tools(self, files: List[Path]) -> List[str]:
        """開発ツールの検出"""
        tools = set()
        
        tool_indicators = {
            'docker': ['dockerfile', 'docker-compose.yml'],
            'git': ['.gitignore', '.gitmodules'],
            'pytest': ['pytest.ini', 'conftest.py'],
            'eslint': ['.eslintrc', 'eslint.config.js'],
            'prettier': ['.prettierrc', 'prettier.config.js'],
            'webpack': ['webpack.config.js'],
            'vite': ['vite.config.js'],
            'makefile': ['makefile'],
            'github_actions': ['.github/workflows'],
            'vscode': ['.vscode/settings.json']
        }
        
        file_paths = [f.name.lower() for f in files] + [str(f).lower() for f in files]
        
        for tool, indicators in tool_indicators.items():
            if any(indicator in path for path in file_paths for indicator in indicators):
                tools.add(tool)
                
        return list(tools)
        
    def _identify_main_files(self, files: List[Path]) -> List[str]:
        """メインファイルの特定"""
        main_files = []
        
        # 優先度の高いファイル名
        priority_names = [
            'main.py', 'app.py', 'index.js', 'main.js', 'app.js',
            'index.html', 'main.html', 'README.md', 'setup.py',
            'package.json', 'requirements.txt', 'Dockerfile'
        ]
        
        file_names = {f.name.lower(): str(f) for f in files}
        
        for priority_name in priority_names:
            if priority_name in file_names:
                main_files.append(file_names[priority_name])
                
        return main_files[:5]  # 最大5個まで
        
    def _has_test_files(self, files: List[Path]) -> bool:
        """テストファイルの有無"""
        test_patterns = ['test_', '_test', 'tests/', 'spec_', '_spec']
        
        for file_path in files:
            path_str = str(file_path).lower()
            if any(pattern in path_str for pattern in test_patterns):
                return True
                
        return False
        
    def _has_documentation(self, files: List[Path]) -> bool:
        """ドキュメントの有無"""
        doc_indicators = ['readme', 'doc', 'docs/', '.md', 'manual', 'guide']
        
        for file_path in files:
            path_str = str(file_path).lower()
            if any(indicator in path_str for indicator in doc_indicators):
                return True
                
        return False
        
    def _estimate_complexity(self, files: List[Path], languages: List[str]) -> str:
        """プロジェクト複雑度の推定"""
        file_count = len(files)
        language_count = len(languages)
        
        # シンプルな複雑度推定
        if file_count < 10 and language_count <= 2:
            return "simple"
        elif file_count < 50 and language_count <= 4:
            return "medium"
        elif file_count < 200:
            return "complex"
        else:
            return "very_complex"
            
    async def _analyze_user_profile(self) -> UserProfile:
        """ユーザープロファイルの分析・生成"""
        try:
            # 既存プロファイルの読み込み
            existing_profile = self._load_user_profile()
            
            if existing_profile:
                # 既存データの更新
                return self._update_user_profile(existing_profile)
            else:
                # 新規プロファイルの生成
                return self._create_new_user_profile()
                
        except Exception as e:
            self.logger.error(f"ユーザープロファイル分析エラー: {e}")
            return self._get_default_user_profile()
            
    def _create_new_user_profile(self) -> UserProfile:
        """新規ユーザープロファイルの生成"""
        # 日本語ユーザー・Git初心者向けデフォルト
        return UserProfile(
            user_level=UserLevel.BEGINNER,
            work_pattern=WorkPattern.FREQUENT_SHORT,
            preferred_language="Japanese",
            session_frequency=2.0,  # 1日2回
            average_session_duration=45.0,  # 45分
            commit_frequency=3.0,  # セッションあたり3回
            error_recovery_success_rate=0.7,  # 70%
            last_updated=datetime.now()
        )
        
    def _get_default_user_profile(self) -> UserProfile:
        """デフォルトユーザープロファイル"""
        return UserProfile(
            user_level=UserLevel.BEGINNER,
            work_pattern=WorkPattern.FREQUENT_SHORT,
            preferred_language="Japanese",
            session_frequency=1.0,
            average_session_duration=30.0,
            commit_frequency=2.0,
            error_recovery_success_rate=0.5,
            last_updated=datetime.now()
        )
        
    def _generate_optimal_config(self) -> OptimalConfig:
        """最適設定の自動生成"""
        try:
            if not self.project_profile or not self.user_profile:
                return self._get_default_optimal_config()
                
            # プロジェクトタイプ別設定
            project_settings = self._get_project_type_settings()
            
            # ユーザーレベル別設定
            user_settings = self._get_user_level_settings()
            
            # 作業パターン別設定
            pattern_settings = self._get_work_pattern_settings()
            
            # 設定の統合
            return OptimalConfig(
                auto_save_interval=max(project_settings['auto_save'], 
                                     user_settings['auto_save'],
                                     pattern_settings['auto_save']),
                backup_frequency=min(project_settings['backup'], 
                                   user_settings['backup']),
                protection_level=max(project_settings['protection'],
                                   user_settings['protection'],
                                   key=lambda x: ['low', 'medium', 'high'].index(x)),
                notification_verbosity=user_settings['notifications'],
                auto_commit_threshold=pattern_settings['commit_threshold'],
                conflict_resolution_style=user_settings['conflict_style'],
                help_message_frequency=user_settings['help_frequency']
            )
            
        except Exception as e:
            self.logger.error(f"最適設定生成エラー: {e}")
            return self._get_default_optimal_config()
            
    def _get_project_type_settings(self) -> Dict[str, Any]:
        """プロジェクトタイプ別設定"""
        project_type = self.project_profile.project_type
        
        settings_map = {
            ProjectType.DATA_SCIENCE: {
                'auto_save': 15,  # データ作業は頻繁に保存
                'backup': 10,
                'protection': 'high'
            },
            ProjectType.WEB: {
                'auto_save': 20,
                'backup': 15,
                'protection': 'medium'
            },
            ProjectType.PYTHON: {
                'auto_save': 30,
                'backup': 20,
                'protection': 'medium'
            },
            ProjectType.DOCUMENTATION: {
                'auto_save': 45,  # ドキュメントは長時間作業
                'backup': 30,
                'protection': 'low'
            }
        }
        
        return settings_map.get(project_type, {
            'auto_save': 30,
            'backup': 20,
            'protection': 'medium'
        })
        
    def _get_user_level_settings(self) -> Dict[str, Any]:
        """ユーザーレベル別設定"""
        user_level = self.user_profile.user_level
        
        settings_map = {
            UserLevel.BEGINNER: {
                'auto_save': 15,  # 初心者は頻繁に保存
                'backup': 10,
                'protection': 'high',
                'notifications': 'verbose',
                'conflict_style': 'safe_auto',
                'help_frequency': 'frequent'
            },
            UserLevel.INTERMEDIATE: {
                'auto_save': 30,
                'backup': 20,
                'protection': 'medium',
                'notifications': 'normal',
                'conflict_style': 'smart_auto',
                'help_frequency': 'occasional'
            },
            UserLevel.ADVANCED: {
                'auto_save': 45,
                'backup': 30,
                'protection': 'medium',
                'notifications': 'minimal',
                'conflict_style': 'manual',
                'help_frequency': 'rare'
            }
        }
        
        return settings_map.get(user_level, settings_map[UserLevel.BEGINNER])
        
    def _get_work_pattern_settings(self) -> Dict[str, Any]:
        """作業パターン別設定"""
        work_pattern = self.user_profile.work_pattern
        
        settings_map = {
            WorkPattern.FREQUENT_SHORT: {
                'auto_save': 20,
                'commit_threshold': 5
            },
            WorkPattern.LONG_SESSION: {
                'auto_save': 45,
                'commit_threshold': 10
            },
            WorkPattern.EXPERIMENTAL: {
                'auto_save': 10,  # 実験は頻繁に保存
                'commit_threshold': 3
            }
        }
        
        return settings_map.get(work_pattern, {
            'auto_save': 30,
            'commit_threshold': 5
        })
        
    def _get_default_optimal_config(self) -> OptimalConfig:
        """デフォルト最適設定"""
        return OptimalConfig(
            auto_save_interval=30,
            backup_frequency=20,
            protection_level="high",
            notification_verbosity="verbose",
            auto_commit_threshold=5,
            conflict_resolution_style="safe_auto",
            help_message_frequency="frequent"
        )
        
    def _generate_config_dict(self) -> Dict[str, Any]:
        """設定辞書の生成"""
        if not self.optimal_config:
            self.optimal_config = self._get_default_optimal_config()
            
        return {
            'system': {
                'name': "Claude++ System",
                'version': "2.5.0-transparent",
                'debug': True,
                'language': "japanese"
            },
            'transparent_git': {
                'enabled': True,
                'auto_save_interval': self.optimal_config.auto_save_interval,
                'auto_branch': True,
                'auto_backup': True,
                'japanese_ui': True
            },
            'auto_yes': {
                'enabled': True,
                'dangerous_operations': False,
                'response': "",  # Enter key
                'delay_ms': 500
            },
            'auto_protection': {
                'enabled': True,
                'protection_level': self.optimal_config.protection_level.upper(),
                'backup_frequency': self.optimal_config.backup_frequency,
                'emergency_protection': True
            },
            'notifications': {
                'enabled': True,
                'sound': True,
                'visual': True,
                'verbosity': self.optimal_config.notification_verbosity,
                'japanese': True,
                'sound_file': "/System/Library/Sounds/Glass.aiff"
            },
            'git': {
                'enabled': True,
                'auto_commit': False,  # 手動確認優先
                'auto_branch': True,
                'intelligent_commits': True,
                'conflict_assistance': True
            },
            'ui': {
                'language': "japanese",
                'hide_technical_terms': True,
                'beginner_friendly': True,
                'help_frequency': self.optimal_config.help_message_frequency
            }
        }
        
    def _get_default_config(self) -> Dict[str, Any]:
        """フォールバック用デフォルト設定"""
        return {
            'system': {'name': "Claude++ System", 'version': "2.5.0", 'debug': True},
            'transparent_git': {'enabled': True, 'auto_save_interval': 30},
            'auto_yes': {'enabled': True, 'response': ""},
            'auto_protection': {'enabled': True, 'protection_level': "HIGH"},
            'notifications': {'enabled': True, 'japanese': True},
            'git': {'enabled': True, 'auto_branch': True},
            'ui': {'language': "japanese", 'beginner_friendly': True}
        }
        
    async def _perform_first_time_setup(self, work_directory: str):
        """初回セットアップの実行"""
        try:
            # Git初期化の確認
            git_dir = Path(work_directory) / ".git"
            if not git_dir.exists():
                await self._initialize_git_repository(work_directory)
                
            # .gitignoreの作成
            await self._create_gitignore(work_directory)
            
            # ユーザー設定の確認
            await self._setup_git_user_config()
            
        except Exception as e:
            self.logger.error(f"初回セットアップエラー: {e}")
            
    async def _initialize_git_repository(self, work_directory: str):
        """Gitリポジトリの初期化"""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'init',
                cwd=work_directory,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            if result.returncode == 0:
                self.logger.info("Gitリポジトリを初期化しました")
            else:
                self.logger.warning("Gitリポジトリの初期化に失敗しました")
                
        except Exception as e:
            self.logger.error(f"Git初期化エラー: {e}")
            
    async def _create_gitignore(self, work_directory: str):
        """適切な.gitignoreファイルの作成"""
        gitignore_path = Path(work_directory) / ".gitignore"
        
        if gitignore_path.exists():
            return  # 既に存在する場合はスキップ
            
        try:
            # プロジェクトタイプに応じた.gitignore内容
            gitignore_content = self._generate_gitignore_content()
            
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
                
            self.logger.info(".gitignoreファイルを作成しました")
            
        except Exception as e:
            self.logger.error(f".gitignore作成エラー: {e}")
            
    def _generate_gitignore_content(self) -> str:
        """プロジェクトタイプに応じた.gitignore内容生成"""
        common_patterns = [
            "# Claude++ System",
            ".claude-plus/",
            "",
            "# OS generated files",
            ".DS_Store",
            "Thumbs.db",
            "",
            "# Editor files",
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo",
            ""
        ]
        
        if self.project_profile:
            if self.project_profile.project_type == ProjectType.PYTHON:
                common_patterns.extend([
                    "# Python",
                    "__pycache__/",
                    "*.pyc",
                    "*.pyo",
                    "*.pyd",
                    ".Python",
                    "build/",
                    "develop-eggs/",
                    "dist/",
                    "downloads/",
                    "eggs/",
                    ".eggs/",
                    "lib/",
                    "lib64/",
                    "parts/",
                    "sdist/",
                    "var/",
                    "wheels/",
                    "*.egg-info/",
                    ".installed.cfg",
                    "*.egg",
                    "MANIFEST",
                    ""
                ])
            elif self.project_profile.project_type in [ProjectType.JAVASCRIPT, ProjectType.WEB]:
                common_patterns.extend([
                    "# Node.js",
                    "node_modules/",
                    "npm-debug.log*",
                    "yarn-debug.log*",
                    "yarn-error.log*",
                    ".npm",
                    ".yarn-integrity",
                    "",
                    "# Build outputs",
                    "dist/",
                    "build/",
                    "*.tgz",
                    ""
                ])
                
        return "\n".join(common_patterns)
        
    async def _setup_git_user_config(self):
        """Git ユーザー設定のセットアップ"""
        try:
            # 既存設定の確認
            result = await asyncio.create_subprocess_exec(
                'git', 'config', '--global', 'user.name',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            if result.returncode != 0:
                # デフォルト設定の適用
                await asyncio.create_subprocess_exec(
                    'git', 'config', '--global', 'user.name', 'Claude++ User',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                await asyncio.create_subprocess_exec(
                    'git', 'config', '--global', 'user.email', 'claude-plus@example.com',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                self.logger.info("Git ユーザー設定を初期化しました")
                
        except Exception as e:
            self.logger.error(f"Git ユーザー設定エラー: {e}")
            
    def _load_learning_data(self):
        """学習データの読み込み"""
        try:
            if self.learning_data_file.exists():
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    self.learning_data = json.load(f)
        except Exception as e:
            self.logger.error(f"学習データ読み込みエラー: {e}")
            
    def _load_user_profile(self) -> Optional[UserProfile]:
        """ユーザープロファイルの読み込み"""
        try:
            if self.user_profile_file.exists():
                with open(self.user_profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return UserProfile(
                        user_level=UserLevel(data['user_level']),
                        work_pattern=WorkPattern(data['work_pattern']),
                        preferred_language=data['preferred_language'],
                        session_frequency=data['session_frequency'],
                        average_session_duration=data['average_session_duration'],
                        commit_frequency=data['commit_frequency'],
                        error_recovery_success_rate=data['error_recovery_success_rate'],
                        last_updated=datetime.fromisoformat(data['last_updated'])
                    )
        except Exception as e:
            self.logger.error(f"ユーザープロファイル読み込みエラー: {e}")
            
        return None
        
    def _update_user_profile(self, existing_profile: UserProfile) -> UserProfile:
        """既存ユーザープロファイルの更新"""
        # 簡単な更新ロジック: 最終更新から1週間以上経過している場合は再評価
        if datetime.now() - existing_profile.last_updated > timedelta(days=7):
            # 学習データに基づく調整
            return existing_profile
        else:
            return existing_profile
            
    def _save_profiles(self):
        """プロファイルの保存"""
        try:
            if self.project_profile:
                # enum値を文字列に変換してからJSON保存
                profile_data = asdict(self.project_profile)
                profile_data['project_type'] = self.project_profile.project_type.value
                
                with open(self.project_profile_file, 'w', encoding='utf-8') as f:
                    json.dump(profile_data, f, ensure_ascii=False, indent=2)
                    
            if self.user_profile:
                profile_data = asdict(self.user_profile)
                profile_data['user_level'] = self.user_profile.user_level.value
                profile_data['work_pattern'] = self.user_profile.work_pattern.value
                profile_data['last_updated'] = self.user_profile.last_updated.isoformat()
                
                with open(self.user_profile_file, 'w', encoding='utf-8') as f:
                    json.dump(profile_data, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            self.logger.error(f"プロファイル保存エラー: {e}")
            
    def get_profile_summary(self) -> Dict[str, Any]:
        """プロファイル情報のサマリー"""
        return {
            'project': {
                'type': self.project_profile.project_type.value if self.project_profile else "不明",
                'languages': self.project_profile.languages if self.project_profile else [],
                'complexity': self.project_profile.estimated_complexity if self.project_profile else "simple"
            },
            'user': {
                'level': self.user_profile.user_level.value if self.user_profile else "初心者",
                'pattern': self.user_profile.work_pattern.value if self.user_profile else "頻繁な短時間作業"
            },
            'config': {
                'auto_save_interval': self.optimal_config.auto_save_interval if self.optimal_config else 30,
                'protection_level': self.optimal_config.protection_level if self.optimal_config else "high"
            }
        }


# テスト用コード
async def test_zero_config():
    """ゼロ設定システムのテスト"""
    manager = ZeroConfigManager()
    
    print("ゼロ設定システムのテスト:")
    print("-" * 40)
    
    # 自動設定の生成
    config = await manager.initialize(".")
    
    print("生成された設定:")
    for section, settings in config.items():
        print(f"  {section}: {settings}")
        
    print()
    print("プロファイル情報:")
    summary = manager.get_profile_summary()
    for category, info in summary.items():
        print(f"  {category}: {info}")


if __name__ == "__main__":
    asyncio.run(test_zero_config())