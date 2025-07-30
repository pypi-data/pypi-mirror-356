#!/usr/bin/env python3
"""
設定ファイルユーティリティ
環境変数の展開をサポートする設定ローダー
"""

import os
import re
import yaml
from typing import Any, Dict

def expand_env_vars(value: Any) -> Any:
    """
    環境変数を展開する
    ${VAR_NAME:-default_value} 形式をサポート
    """
    if isinstance(value, str):
        # 環境変数パターンを検索
        pattern = r'\$\{([^}]+)\}'
        matches = re.findall(pattern, value)
        
        for match in matches:
            # デフォルト値の処理
            if ':-' in match:
                var_name, default_value = match.split(':-', 1)
                env_value = os.environ.get(var_name, default_value)
            else:
                var_name = match
                env_value = os.environ.get(var_name, '')
            
            # 文字列の置換
            value = value.replace(f'${{{match}}}', env_value)
            
        # 型変換の試行
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        
    elif isinstance(value, dict):
        # 辞書の再帰処理
        return {k: expand_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        # リストの再帰処理
        return [expand_env_vars(item) for item in value]
    
    return value

def load_config_with_env(config_path: str) -> Dict[str, Any]:
    """
    環境変数の展開をサポートする設定ファイルローダー
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 環境変数を展開
    return expand_env_vars(config)

def get_environment() -> str:
    """
    現在の環境を取得（開発/本番）
    """
    return os.environ.get('CLAUDE_PLUS_ENV', 'production')

def is_development() -> bool:
    """
    開発環境かどうかを判定
    """
    return get_environment() == 'development'

def setup_dev_environment():
    """
    開発環境の環境変数を設定
    """
    os.environ['CLAUDE_PLUS_ENV'] = 'development'
    os.environ['CLAUDE_PLUS_DEBUG'] = 'true'
    os.environ['CLAUDE_PLUS_LOG_LEVEL'] = 'DEBUG'
    os.environ['CLAUDE_PLUS_LOG_FILE'] = '/tmp/claude-plus-dev.log'
    os.environ['CLAUDE_PLUS_AUTO_RELOAD'] = 'true'
    os.environ['CLAUDE_PLUS_DEVELOPMENT_MODE'] = 'true'