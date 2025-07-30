"""
入力振り分けシステム
ユーザー入力を解析してClaude Codeに適切に転送
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Context:
    """会話コンテキスト"""
    current_file: Optional[str] = None
    recent_files: List[str] = field(default_factory=list)
    last_command: Optional[str] = None
    last_action: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def update_file(self, filename: str):
        """ファイルコンテキストを更新"""
        self.current_file = filename
        if filename not in self.recent_files:
            self.recent_files.append(filename)
            # 最新5ファイルのみ保持
            if len(self.recent_files) > 5:
                self.recent_files.pop(0)
        self.timestamp = datetime.now()


class InputRouter:
    """入力振り分けルーター"""
    
    # ファイル操作パターン
    FILE_PATTERNS = [
        (r'(.+\.py|.+\.js|.+\.txt|.+\.md|.+\.yaml|.+\.yml|.+\.json)を?(.+)', 'file_operation'),
        (r'(.+)ファイルを?(.+)', 'file_operation'),
        (r'ファイル(.+)を?(.+)', 'file_operation'),
    ]
    
    # アクションキーワード
    ACTION_KEYWORDS = {
        '編集': 'edit',
        '修正': 'edit',
        '変更': 'edit',
        '改良': 'improve',
        '改善': 'improve',
        '最適化': 'optimize',
        '作成': 'create',
        '作って': 'create',
        '書いて': 'write',
        '追加': 'add',
        '削除': 'delete',
        '消して': 'delete',
        '実行': 'run',
        'テスト': 'test',
        '保存': 'save',
        'コミット': 'commit',
        'バックアップ': 'backup',
    }
    
    def __init__(self):
        self.context = Context()
    
    def route_input(self, user_input: str) -> Dict[str, Any]:
        """ユーザー入力をルーティング"""
        
        # コンテキストを考慮した解析
        result = self._analyze_input(user_input)
        
        # Claude Codeへ転送する形式に変換
        claude_command = self._format_for_claude(result)
        
        # コンテキストを更新
        self._update_context(result)
        
        return {
            "original_input": user_input,
            "analysis": result,
            "claude_command": claude_command,
            "context": self._get_context_info()
        }
    
    def _analyze_input(self, user_input: str) -> Dict[str, Any]:
        """入力を解析"""
        analysis = {
            "type": "general",
            "action": None,
            "target": None,
            "details": user_input
        }
        
        # ファイル操作の検出
        for pattern, op_type in self.FILE_PATTERNS:
            match = re.search(pattern, user_input)
            if match:
                analysis["type"] = "file_operation"
                analysis["target"] = match.group(1).strip()
                if len(match.groups()) > 1:
                    analysis["details"] = match.group(2).strip()
                break
        
        # アクションの検出
        for keyword, action in self.ACTION_KEYWORDS.items():
            if keyword in user_input:
                analysis["action"] = action
                break
        
        # コンテキストからの推測
        if not analysis["target"] and analysis["action"] in ['edit', 'improve', 'test']:
            if self.context.current_file:
                analysis["target"] = self.context.current_file
                analysis["inferred"] = True
        
        return analysis
    
    def _format_for_claude(self, analysis: Dict[str, Any]) -> str:
        """Claude Code用にコマンドをフォーマット"""
        
        # ファイル操作の場合
        if analysis["type"] == "file_operation" and analysis["target"]:
            action = analysis.get("action", "edit")
            target = analysis["target"]
            details = analysis.get("details", "")
            
            if action == "create":
                return f"Create a new file {target} with {details}"
            elif action == "edit" or action == "improve":
                return f"Edit {target} to {details}"
            elif action == "test":
                return f"Create tests for {target}"
            elif action == "delete":
                return f"Delete {target}"
            else:
                return f"Work on {target}: {details}"
        
        # 一般的なコマンド
        return analysis.get("details", "")
    
    def _update_context(self, analysis: Dict[str, Any]):
        """コンテキストを更新"""
        if analysis.get("target"):
            self.context.update_file(analysis["target"])
        
        if analysis.get("action"):
            self.context.last_action = analysis["action"]
        
        self.context.last_command = analysis.get("details")
    
    def _get_context_info(self) -> Dict[str, Any]:
        """現在のコンテキスト情報を取得"""
        return {
            "current_file": self.context.current_file,
            "recent_files": self.context.recent_files,
            "last_action": self.context.last_action,
            "age_seconds": (datetime.now() - self.context.timestamp).total_seconds()
        }
    
    def suggest_next_action(self) -> List[str]:
        """次のアクションを提案"""
        suggestions = []
        
        if self.context.current_file:
            base = self.context.current_file.rsplit('.', 1)[0]
            ext = self.context.current_file.rsplit('.', 1)[1] if '.' in self.context.current_file else ''
            
            # 最後のアクションに基づく提案
            if self.context.last_action == "create" or self.context.last_action == "edit":
                suggestions.append(f"テストを作成: test_{base}.{ext}")
                suggestions.append(f"実行: python {self.context.current_file}")
            elif self.context.last_action == "test":
                suggestions.append("テストを実行")
                suggestions.append("カバレッジを確認")
        
        # 一般的な提案
        suggestions.extend([
            "変更を保存",
            "コミット",
            "他のファイルを編集"
        ])
        
        return suggestions[:3]  # 上位3つ
    
    def clear_context(self):
        """コンテキストをクリア"""
        self.context = Context()
        logger.info("コンテキストをクリアしました")