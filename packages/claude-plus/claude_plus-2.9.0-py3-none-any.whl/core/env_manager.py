#!/usr/bin/env python3
"""
Claude++ Environment Manager
開発・本番環境の自動判定と設定管理
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from .config_utils import expand_env_vars, load_config_with_env

logger = logging.getLogger(__name__)


class EnvironmentManager:
    """環境管理クラス - 開発/本番環境の自動判定と設定管理"""
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent
        self.environment = self._detect_environment()
        self.config = self._load_environment_config()
        
    def _detect_environment(self) -> str:
        """環境を自動判定"""
        # 1. 環境変数による明示的指定
        env = os.environ.get('CLAUDE_PLUS_ENV')
        if env in ['development', 'production']:
            logger.debug(f"環境変数で環境決定: {env}")
            return env
            
        # 2. 開発環境の自動判定
        indicators = [
            '.git',           # Gitリポジトリ
            'pyproject.toml', # Python開発プロジェクト
            '.gitignore',     # 開発ファイル
            'requirements.txt' # 依存関係ファイル
        ]
        
        dev_indicators_found = sum(1 for indicator in indicators 
                                 if (self.project_root / indicator).exists())
        
        # 2つ以上の開発指標があれば開発環境
        if dev_indicators_found >= 2:
            logger.debug(f"開発環境を自動検出 (指標数: {dev_indicators_found})")
            return 'development'
            
        # 3. pipx環境チェック（本番環境の判定）
        if self._is_pipx_environment():
            logger.debug("pipx環境を検出 - 本番環境")
            return 'production'
            
        # 4. デフォルトは本番環境（安全側）
        logger.debug("デフォルト環境: production")
        return 'production'
        
    def _is_pipx_environment(self) -> bool:
        """pipx環境またはvenv本番環境かどうかを判定"""
        try:
            import sys
            
            # 現在のPythonインタープリターのパス（シンボリックリンクをたどらない）
            current_path = str(Path(sys.executable))
            
            # Phase 2.7の新しいvenv本番環境
            venv_production_indicators = [
                '.claude-plus-venv',  # 新しいvenv本番環境
                '.local/pipx/venvs',  # 従来のpipx環境
                'pipx/venvs',
            ]
            
            is_prod_env = any(indicator in current_path for indicator in venv_production_indicators)
            
            # 開発環境の除外（プロジェクトディレクトリ内のvenvは開発環境）
            is_dev_venv = str(self.project_root) in current_path and 'venv' in current_path
            
            return is_prod_env and not is_dev_venv
        except Exception:
            return False
            
    def _load_environment_config(self) -> Dict[str, Any]:
        """統一設定を読み込み（環境変数展開対応）"""
        config_dir = self.project_root / 'config'
        config_file = config_dir / 'config.yaml'
        
        config = {}
        
        # 統一設定を読み込み（環境変数展開対応）
        if config_file.exists():
            try:
                config = load_config_with_env(str(config_file))
                logger.debug(f"統一設定読み込み（環境: {self.environment}）: {config_file}")
            except Exception as e:
                logger.warning(f"設定読み込みエラー: {e}")
                config = {}
        else:
            logger.warning(f"設定ファイルが見つかりません: {config_file}")
            
        return config
        
    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """設定をマージ（深い階層まで対応）"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
                
        return result
        
    def get_config(self, key: Optional[str] = None, default: Any = None) -> Any:
        """設定値を取得"""
        if key is None:
            return self.config
            
        # ドット記法でネストしたキーにアクセス
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def is_development(self) -> bool:
        """開発環境かどうか"""
        return self.environment == 'development'
        
    def is_production(self) -> bool:
        """本番環境かどうか"""
        return self.environment == 'production'
        
    def get_environment_info(self) -> Dict[str, Any]:
        """環境情報を取得"""
        return {
            'environment': self.environment,
            'project_root': str(self.project_root),
            'config_source': f'config/{self.environment}.yaml',
            'is_pipx': self._is_pipx_environment(),
            'indicators': {
                'git': (self.project_root / '.git').exists(),
                'pyproject': (self.project_root / 'pyproject.toml').exists(),
                'requirements': (self.project_root / 'requirements.txt').exists(),
            }
        }
        
    @classmethod
    def setup_environment_configs(cls, project_root: str):
        """環境別設定ファイルのテンプレートを作成"""
        config_dir = Path(project_root) / 'config'
        config_dir.mkdir(exist_ok=True)
        
        # 本番環境設定
        production_config = {
            'system': {
                'debug': False,
                'log_level': 'INFO',
                'auto_reload': False
            },
            'claude': {
                'command': 'claude',
                'args': [],
                'timeout': 300
            },
            'process': {
                'buffer_size': 8192,
                'max_retries': 3
            },
            'logging': {
                'level': 'INFO',
                'file': '/tmp/claude-plus.log',
                'file_level': 'DEBUG'
            }
        }
        
        # 開発環境設定
        development_config = {
            'system': {
                'debug': True,
                'log_level': 'DEBUG',
                'auto_reload': True,
                'development_mode': True
            },
            'claude': {
                'command': 'claude',
                'args': [],
                'timeout': 300
            },
            'process': {
                'buffer_size': 8192,
                'max_retries': 3
            },
            'logging': {
                'level': 'DEBUG',
                'file': '/tmp/claude-plus-dev.log',
                'file_level': 'DEBUG'
            }
        }
        
        # ファイル作成
        production_file = config_dir / 'production.yaml'
        development_file = config_dir / 'development.yaml'
        
        if not production_file.exists():
            with open(production_file, 'w', encoding='utf-8') as f:
                yaml.dump(production_config, f, default_flow_style=False, allow_unicode=True)
            print(f"本番環境設定作成: {production_file}")
            
        if not development_file.exists():
            with open(development_file, 'w', encoding='utf-8') as f:
                yaml.dump(development_config, f, default_flow_style=False, allow_unicode=True)
            print(f"開発環境設定作成: {development_file}")


# グローバルインスタンス
env_manager = EnvironmentManager()


def get_environment() -> str:
    """現在の環境を取得"""
    return env_manager.environment


def get_config(key: Optional[str] = None, default: Any = None) -> Any:
    """設定値を取得"""
    return env_manager.get_config(key, default)


def is_development() -> bool:
    """開発環境かどうか"""
    return env_manager.is_development()


def is_production() -> bool:
    """本番環境かどうか"""
    return env_manager.is_production()


if __name__ == '__main__':
    # テスト用
    print("=== Claude++ Environment Manager ===")
    info = env_manager.get_environment_info()
    for key, value in info.items():
        print(f"{key}: {value}")