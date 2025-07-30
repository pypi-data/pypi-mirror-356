#!/usr/bin/env python3
"""
Claude++ 安心ダッシュボード
システム状態、作業状況、次のアクション提案をリアルタイム表示
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import json
from pathlib import Path

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich import box

class DashboardData:
    """ダッシュボードデータ管理クラス"""
    
    def __init__(self):
        self.system_status = {
            "auto_save": True,
            "notifications": True,
            "auto_confirm": True,
            "split_screen": True
        }
        # start_timeをデフォルトで設定
        self.start_time = datetime.now()
        self.work_status = {
            "current_action": "待機中",
            "working_directory": os.getcwd(),
            "start_time": time.time(),  # timestamp形式で保存
            "elapsed_time": "00:00:00"
        }
        self.suggestions = [
            {"icon": "💡", "text": "プロジェクトの初期化", "command": "git init"},
            {"icon": "📝", "text": "新しいファイルを作成", "command": "ファイル名を教えてください"},
            {"icon": "🔍", "text": "ヘルプを表示", "command": "ヘルプ"}
        ]
        self.statistics = {
            "files_edited": 0,
            "commands_executed": 0,
            "errors_resolved": 0,
            "git_commits": 0
        }
        self.overall_status = "すべて正常"
        self.overall_status_color = "green"
    
    def update_elapsed_time(self):
        """経過時間を更新"""
        # start_timeがtimestampの場合はdatetimeに変換
        if isinstance(self.work_status.get("start_time"), (int, float)):
            start_time = datetime.fromtimestamp(self.work_status["start_time"])
        else:
            start_time = self.start_time
            
        elapsed = datetime.now() - start_time
        hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.work_status["elapsed_time"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_system_status_text(self) -> str:
        """システム状態の総括テキストを取得"""
        active_count = sum(1 for v in self.system_status.values() if v)
        if active_count == 4:
            return ("✨ すべての機能が有効", "green")
        elif active_count >= 2:
            return (f"⚡ {active_count}/4 機能が有効", "yellow")
        else:
            return ("⚠️ 一部機能が無効", "red")
    
    def update_suggestions(self, context: Optional[str] = None):
        """コンテキストに応じた提案を更新"""
        if context == "git":
            self.suggestions = [
                {"icon": "🌿", "text": "新しいブランチを作成", "command": "git checkout -b feature/新機能"},
                {"icon": "💾", "text": "変更をコミット", "command": "git add . && git commit -m 'メッセージ'"},
                {"icon": "🚀", "text": "リモートにプッシュ", "command": "git push origin main"}
            ]
        elif context == "error":
            self.suggestions = [
                {"icon": "🔧", "text": "エラーログを確認", "command": "cat /tmp/claude-plus.log"},
                {"icon": "🔄", "text": "セッションを再起動", "command": "claude-plus"},
                {"icon": "📚", "text": "ドキュメントを確認", "command": "cat README.md"}
            ]
        # デフォルトの提案は初期値のまま


class ClaudeDashboard:
    """Claude++ 安心ダッシュボード"""
    
    def __init__(self, session_name: Optional[str] = None):
        self.session_name = session_name or self._find_active_session()
        self.claude_pane = f"{self.session_name}:0.0"
        self.console = Console()
        self.data = DashboardData()
        self.running = True
        self.update_interval = 1  # 1秒間隔で更新
        
        # 状態ファイルのパス
        self.state_file = Path("/tmp/claude_plus_state.json")
        
    def _find_active_session(self) -> str:
        """アクティブなclaude-plusセッションを探す"""
        try:
            result = subprocess.run(
                ["tmux", "list-sessions", "-F", "#{session_name}"],
                capture_output=True, text=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if 'claude_plus' in line:
                    return line.strip()
            
            return "claude_plus"
        except:
            return "claude_plus"
    
    def _load_state(self):
        """daemon.pyから共有される状態を読み込む"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    
                # システム状態を更新
                if "system_status" in state:
                    self.data.system_status.update(state["system_status"])
                    
                # 作業状態を更新
                if "work_status" in state:
                    self.data.work_status.update(state["work_status"])
                    
                # 統計情報を更新
                if "statistics" in state:
                    self.data.statistics.update(state["statistics"])
                    
        except Exception as e:
            # エラーは静かに処理（ダッシュボードは常に表示継続）
            pass
    
    def _analyze_claude_output(self) -> Optional[str]:
        """Claude Codeの出力を分析してコンテキストを判定"""
        try:
            result = subprocess.run(
                ["tmux", "capture-pane", "-t", self.claude_pane, "-p", "-S", "-10"],
                capture_output=True, text=True, timeout=1
            )
            
            if result.returncode == 0:
                output = result.stdout.lower()
                
                # Git関連の操作を検出
                if any(word in output for word in ["git", "commit", "branch", "merge", "push", "pull"]):
                    return "git"
                
                # エラーを検出
                if any(word in output for word in ["error", "failed", "exception", "エラー"]):
                    return "error"
                
                # ファイル編集を検出
                if any(word in output for word in ["edit", "create", "write", "編集", "作成"]):
                    self.data.work_status["current_action"] = "ファイル編集中"
                    
                # コマンド実行を検出
                if any(word in output for word in ["run", "execute", "実行"]):
                    self.data.work_status["current_action"] = "コマンド実行中"
                
            return None
            
        except Exception:
            return None
    
    def create_system_status_panel(self) -> Panel:
        """システム状態パネルを作成"""
        table = Table.grid(padding=1)
        
        # 各機能の状態を表示
        features = [
            ("自動保存", self.data.system_status["auto_save"], "💾"),
            ("通知", self.data.system_status["notifications"], "🔔"),
            ("確認省略", self.data.system_status["auto_confirm"], "⚡"),
            ("画面分割", self.data.system_status["split_screen"], "🖥️")
        ]
        
        for name, enabled, icon in features:
            status = f"{icon} {name}: " + ("ON" if enabled else "OFF")
            color = "green" if enabled else "red"
            table.add_row(Text(status, style=color))
        
        # 総括メッセージ
        status_text, status_color = self.data.get_system_status_text()
        table.add_row("")  # 空行
        table.add_row(Text(status_text, style=f"bold {status_color}"))
        
        return Panel(
            table,
            title="🛡️ システム状態",
            border_style="cyan",
            box=box.ROUNDED
        )
    
    def create_work_status_panel(self) -> Panel:
        """作業状況パネルを作成"""
        self.data.update_elapsed_time()
        
        table = Table.grid(padding=1)
        table.add_row(
            Text("現在の動作:", style="dim"),
            Text(self.data.work_status["current_action"], style="yellow")
        )
        table.add_row(
            Text("作業ディレクトリ:", style="dim"),
            Text(self.data.work_status["working_directory"], style="blue")
        )
        table.add_row(
            Text("経過時間:", style="dim"),
            Text(self.data.work_status["elapsed_time"], style="magenta")
        )
        
        return Panel(
            table,
            title="⚙️ 作業状況",
            border_style="yellow",
            box=box.ROUNDED
        )
    
    def create_suggestions_panel(self) -> Panel:
        """次のアクション提案パネルを作成"""
        table = Table.grid(padding=1)
        
        for i, suggestion in enumerate(self.data.suggestions, 1):
            table.add_row(
                Text(f"{i}. {suggestion['icon']} {suggestion['text']}", style="cyan"),
                Text(f"→ {suggestion['command']}", style="dim italic")
            )
        
        return Panel(
            table,
            title="💡 次のアクション提案",
            border_style="green",
            box=box.ROUNDED
        )
    
    def create_statistics_panel(self) -> Panel:
        """本日の成果パネルを作成"""
        stats = self.data.statistics
        
        # 絵文字付きの統計表示
        items = [
            f"📝 編集: {stats['files_edited']}",
            f"⚡ 実行: {stats['commands_executed']}",
            f"🔧 解決: {stats['errors_resolved']}",
            f"💾 コミット: {stats['git_commits']}"
        ]
        
        # 総合評価メッセージ
        total = sum(stats.values())
        if total == 0:
            message = "🌟 さあ、始めましょう！"
        elif total < 10:
            message = "💪 順調に進んでいます！"
        elif total < 30:
            message = "🔥 素晴らしいペースです！"
        else:
            message = "🚀 今日は大活躍ですね！"
        
        content = "\n".join(items) + f"\n\n{message}"
        
        return Panel(
            Align.center(Text(content, justify="left")),
            title="📊 本日の成果",
            border_style="magenta",
            box=box.ROUNDED
        )
    
    def create_layout(self) -> Layout:
        """ダッシュボードレイアウトを作成"""
        layout = Layout()
        
        # ヘッダー
        header_text = Text()
        header_text.append("Claude++ 安心ダッシュボード", style="bold white on blue")
        header_text.append("  ")
        header_text.append("[Tab:上部ペイン q:終了]", style="dim white on blue")
        
        header = Panel(
            Align.center(header_text, vertical="middle"),
            height=3,
            box=box.DOUBLE
        )
        
        # メインコンテンツを2x2グリッドで配置
        top_row = Layout()
        top_row.split_row(
            Layout(self.create_system_status_panel(), name="system"),
            Layout(self.create_work_status_panel(), name="work")
        )
        
        bottom_row = Layout()
        bottom_row.split_row(
            Layout(self.create_suggestions_panel(), name="suggestions"),
            Layout(self.create_statistics_panel(), name="statistics")
        )
        
        # 全体レイアウト
        layout.split_column(
            Layout(header, size=3),
            Layout(top_row, name="top"),
            Layout(bottom_row, name="bottom")
        )
        
        return layout
    
    def run(self):
        """ダッシュボードを実行"""
        # キーボード入力用スレッドを開始
        input_thread = threading.Thread(target=self._handle_keyboard_input, daemon=True)
        input_thread.start()
        
        with Live(
            self.create_layout(),
            console=self.console,
            refresh_per_second=2,
            screen=True
        ) as live:
            while self.running:
                try:
                    # 状態を読み込み
                    self._load_state()
                    
                    # Claude出力を分析してコンテキストを更新
                    context = self._analyze_claude_output()
                    if context:
                        self.data.update_suggestions(context)
                    
                    # レイアウトを更新
                    live.update(self.create_layout())
                    
                    time.sleep(self.update_interval)
                    
                except KeyboardInterrupt:
                    self.running = False
                except Exception as e:
                    # エラーが発生してもダッシュボードは継続
                    time.sleep(self.update_interval)
    
    def _handle_keyboard_input(self):
        """キーボード入力を処理（別スレッド）"""
        try:
            import termios
            import tty
            
            # 現在の端末設定を保存
            old_settings = termios.tcgetattr(sys.stdin)
            
            try:
                # Raw モードに設定
                tty.setraw(sys.stdin.fileno())
                
                while self.running:
                    # 非ブロッキング読み取り
                    import select
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        char = sys.stdin.read(1)
                        
                        # キー処理
                        if char == 'q' or char == 'Q':
                            self.running = False
                            break
                        elif char == '\t':  # Tab: Claude Codeペインに切り替え
                            subprocess.run([
                                "tmux", "select-pane", "-t", self.claude_pane
                            ], capture_output=True)
                        elif char == 'v':  # v: 通常ビューアーに切り替え
                            # TODO: 通常ビューアーへの切り替え実装
                            pass
                        elif char == 'r':  # r: リフレッシュ
                            self._load_state()
                        
            finally:
                # 端末設定を復元
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                
        except Exception:
            # 端末操作が利用できない環境では無視
            pass


def main():
    """メイン関数"""
    try:
        dashboard = ClaudeDashboard()
        dashboard.run()
    except KeyboardInterrupt:
        print("\n👋 安心ダッシュボードを終了します...")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()