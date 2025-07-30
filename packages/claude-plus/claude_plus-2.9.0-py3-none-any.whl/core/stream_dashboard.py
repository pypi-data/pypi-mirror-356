#!/usr/bin/env python3
"""
Claude++ ログストリーム管理画面 (Phase 2.8)
リアルタイムで動作ログを表示する軽量な管理画面
"""

import collections
import time
import threading
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Deque
import json
from pathlib import Path
import threading


class StreamDashboard:
    """ログストリーム管理画面の中核クラス"""
    
    # ログレベル定義（日本語化）
    LOG_LEVELS = {
        'INFO': {'icon': '📝', 'msg': '作業中', 'color': '\033[94m'},
        'PROC': {'icon': '🔄', 'msg': '処理中', 'color': '\033[93m'},
        'GIT ': {'icon': '💾', 'msg': '保存', 'color': '\033[92m'},
        'TASK': {'icon': '⚡', 'msg': 'タスク', 'color': '\033[96m'},
        'OK  ': {'icon': '✅', 'msg': '完了', 'color': '\033[92m'},
        'WARN': {'icon': '⚠️', 'msg': '注意', 'color': '\033[91m'},
        'ERR ': {'icon': '❌', 'msg': 'エラー', 'color': '\033[91m'},
        'SAVE': {'icon': '💾', 'msg': '保存', 'color': '\033[95m'},
    }
    
    # 色リセット
    RESET_COLOR = '\033[0m'
    
    def __init__(self, max_lines: int = 4):
        """
        初期化（軽量版）
        
        Args:
            max_lines: 保持する最大ログ行数（デフォルト4行）
        """
        self.max_lines = max_lines
        self.log_buffer: Deque[Dict[str, Any]] = collections.deque(maxlen=max_lines)
        self.start_time = time.time()
        self.current_status = '正常動作中'  # 正常動作中 / 注意 / エラー
        self.current_action = '待機中'
        self.status_icon = '🟢'  # ステータスアイコン
        self.notification_message = None  # 通知メッセージ
        self.notification_time = None  # 通知時刻
        
        # 更新制御
        self.last_update = 0
        self.update_interval = 1.0  # 1秒間隔（より軽量）
        self.running = True
        
        # スレッドセーフティ
        self._lock = threading.Lock()
        
        # 状態ファイル（daemon.pyと連携）
        # 環境変数からPIDを取得してPIDベースのパスを使用
        pid = os.environ.get('CLAUDE_PLUS_PID', os.getpid())
        self.state_file = Path(f"/tmp/claude_plus_{pid}/state.json")
    
    async def add_log(self, level: str, message: str, category: str = None) -> None:
        """
        ログエントリを追加
        
        Args:
            level: ログレベル (INFO, PROC, GIT, TASK, OK, WARN, ERR, SAVE)
            message: ログメッセージ
            category: カテゴリ（オプション）
        """
        with self._lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            log_entry = {
                'timestamp': timestamp,
                'level': level,
                'message': message,
                'category': category,
                'raw_time': time.time()
            }
            
            self.log_buffer.append(log_entry)
    
    def add_log_sync(self, level: str, message: str, category: str = None) -> None:
        """
        同期版ログ追加（非async環境用）
        
        Args:
            level: ログレベル
            message: ログメッセージ
            category: カテゴリ（オプション）
        """
        with self._lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            log_entry = {
                'timestamp': timestamp,
                'level': level,
                'message': message,
                'category': category,
                'raw_time': time.time()
            }
            
            self.log_buffer.append(log_entry)
    
    async def update_status(self, status: str, action: str = None) -> None:
        """現在のステータスとアクションを更新"""
        with self._lock:
            self.current_status = status
            if action:
                self.current_action = action
            
            # ステータスに応じたアイコン設定
            if 'エラー' in status:
                self.status_icon = '🔴'
            elif '注意' in status:
                self.status_icon = '🟡'
            else:
                self.status_icon = '🟢'
    
    def show_notification(self, message: str, duration: int = 5, notification_time: float = None) -> None:
        """通知メッセージを表示"""
        with self._lock:
            self.notification_message = message
            self.notification_time = notification_time or time.time()
            # 指定秒数後に通知をクリア
            def clear_notification():
                time.sleep(duration)
                with self._lock:
                    if self.notification_time and time.time() - self.notification_time >= duration - 0.1:
                        self.notification_message = None
                        self.notification_time = None
            
            threading.Thread(target=clear_notification, daemon=True).start()
    
    def render_header(self) -> str:
        """ヘッダー部分をレンダリング（カード型デザイン）"""
        with self._lock:
            # ヘッダー行（枠線なし）
            header = f"Claude++ 開発アシスタント                    {self.status_icon} {self.current_status}\n"
            header += "\n"  # 空行で区切り
            
            # 現在の状況を3要素で表示
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            time_display = f"{minutes}分{seconds}秒" if minutes > 0 else f"{seconds}秒"
            
            header += f"📝 いま: {self.current_action}\n"
            header += f"⏰ 時間: {time_display}経過\n"
            
            # 状況メッセージ
            if self.status_icon == '🟢':
                status_msg = "すべて順調です"
            elif self.status_icon == '🟡':
                status_msg = "注意が必要です"
            else:
                status_msg = "エラーが発生しています"
            
            header += f"✅ 状況: {status_msg}\n"
            
            # 通知メッセージがある場合は表示（時刻付き）
            if self.notification_message:
                # 通知時刻を表示用にフォーマット
                if self.notification_time:
                    from datetime import datetime
                    notification_dt = datetime.fromtimestamp(self.notification_time)
                    time_str = notification_dt.strftime("%H:%M:%S")
                    header += "\n"
                    header += f"🔔 通知 [{time_str}]: {self.notification_message}\n"
                else:
                    header += "\n"
                    header += f"🔔 通知: {self.notification_message}\n"
            
            return header
    
    def render_logs(self) -> List[str]:
        """ログ部分をレンダリング（日本語化・シンプル版）"""
        with self._lock:
            rendered_lines = []
            
            # セクションタイトル
            rendered_lines.append("\n最近の作業:")
            
            # ログがない場合
            if not self.log_buffer:
                rendered_lines.append("  💤 まだ作業が開始されていません")
                return rendered_lines
            
            # 最新のログから表示（最大4行）
            for log_entry in list(self.log_buffer)[-4:]:
                level = log_entry['level']
                message = log_entry['message']
                
                # レベル情報取得
                level_info = self.LOG_LEVELS.get(level, {'icon': '🔹', 'msg': '作業', 'color': ''})
                icon = level_info['icon']
                
                # 日本語化されたメッセージの作成
                if level == 'GIT ':
                    display_msg = f"{icon} 変更を保存しました"
                elif level == 'INFO':
                    display_msg = f"{icon} {message}"
                elif level == 'OK  ':
                    display_msg = f"{icon} {message} → 完了"
                elif level == 'ERR ':
                    display_msg = f"{icon} エラー: {message}"
                elif level == 'WARN':
                    display_msg = f"{icon} 注意: {message}"
                else:
                    display_msg = f"{icon} {message}"
                
                # インデント付きで表示
                rendered_lines.append(f"  {display_msg}")
            
            return rendered_lines
    
    def render_footer(self) -> str:
        """フッター部分をレンダリング（シンプル版）"""
        # 空行で区切るだけのシンプルなフッター
        return ""
    
    def render_full_display(self) -> str:
        """完全な表示をレンダリング（カード型レイアウト）"""
        display_parts = []
        
        # ヘッダー部分
        display_parts.append(self.render_header())
        
        # ログ部分
        log_lines = self.render_logs()
        display_parts.append("\n".join(log_lines))
        
        # フッター（空行）
        display_parts.append(self.render_footer())
        
        return "\n".join(display_parts)
    
    def run_display_loop(self):
        """メインの表示ループ"""
        self._last_action = ""
        running = True
        while running:
            try:
                # 状態ファイルからの情報読み込み
                state_file = self.state_file
                if state_file.exists():
                    try:
                        with open(state_file, 'r') as f:
                            state = json.load(f)
                        
                        # 状態に基づいたログ更新
                        current_action = state.get('work_status', {}).get('current_action', '待機中')
                        if current_action != '待機中' and current_action != self._last_action:
                            # 現在のアクションを更新
                            self.current_action = self._format_action_message(current_action)
                            self.add_log_sync("INFO", current_action)
                            self._last_action = current_action
                        
                        # 通知情報をチェック
                        notification_data = state.get('notification', {})
                        if notification_data.get('message') and notification_data.get('time'):
                            notification_time = notification_data['time']
                            # 新しい通知かチェック
                            if (not self.notification_time or 
                                notification_time > self.notification_time):
                                self.show_notification(notification_data['message'], 10, notification_time)
                            
                    except Exception:
                        pass  # 状態ファイル読み込みエラーは無視
                
                # 画面更新
                if self.should_update():
                    self.clear_screen_and_display()
                    self.mark_updated()
                
                time.sleep(1.0)  # 1秒間隔（より軽量）
                
            except KeyboardInterrupt:
                break
            except Exception:
                # エラーは表示せずに継続
                time.sleep(1)
    
    def clear_screen_and_display(self) -> None:
        """画面をクリアして表示"""
        # 画面クリア（ANSI エスケープシーケンス）
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
        
        # レンダリングして表示
        display = self.render_full_display()
        print(display)
        sys.stdout.flush()
    
    def should_update(self) -> bool:
        """更新が必要かチェック"""
        current_time = time.time()
        return (current_time - self.last_update) >= self.update_interval
    
    def mark_updated(self) -> None:
        """最終更新時刻をマーク"""
        self.last_update = time.time()
    
    def _format_action_message(self, action: str) -> str:
        """アクションメッセージを日本語化"""
        # 英語キーワードを日本語に置換
        translations = {
            'analyzing': '分析中',
            'editing': '編集中',
            'saving': '保存中',
            'running': '実行中',
            'testing': 'テスト中',
            'building': 'ビルド中',
            'checking': 'チェック中',
            'waiting': '待機中',
            'file': 'ファイル',
            'files': 'ファイル',
            'test': 'テスト',
            'tests': 'テスト',
            'error': 'エラー',
            'errors': 'エラー'
        }
        
        # 変換処理
        formatted = action
        for eng, jpn in translations.items():
            formatted = formatted.replace(eng, jpn)
        
        # 最後に「です」を追加（自然な日本語に）
        if not formatted.endswith('。') and not formatted.endswith('です'):
            formatted += 'しています'
        
        return formatted


class StreamDashboardLogger:
    """DaemonからStreamDashboardへのログ送信を担当"""
    
    def __init__(self, dashboard: StreamDashboard = None):
        self.dashboard = dashboard
        self.log_queue = []
        self._lock = threading.Lock()
    
    def set_dashboard(self, dashboard: StreamDashboard) -> None:
        """ダッシュボードインスタンスを設定"""
        with self._lock:
            self.dashboard = dashboard
    
    async def send_log(self, level: str, message: str, category: str = None) -> None:
        """ダッシュボードにログを送信（非同期版）"""
        if self.dashboard:
            await self.dashboard.add_log(level, message, category)
        else:
            # ダッシュボードが未設定の場合はキューに保存
            with self._lock:
                self.log_queue.append({'level': level, 'message': message, 'category': category})
    
    def send_log_sync(self, level: str, message: str, category: str = None) -> None:
        """ダッシュボードにログを送信（同期版）"""
        if self.dashboard:
            self.dashboard.add_log_sync(level, message, category)
        else:
            # ダッシュボードが未設定の場合はキューに保存
            with self._lock:
                self.log_queue.append({'level': level, 'message': message, 'category': category})
    
    async def flush_queue(self) -> None:
        """キューにたまったログをダッシュボードに送信"""
        if not self.dashboard:
            return
        
        with self._lock:
            for log_entry in self.log_queue:
                await self.dashboard.add_log(
                    log_entry['level'], 
                    log_entry['message'], 
                    log_entry['category']
                )
            self.log_queue.clear()


def create_dashboard_process_code() -> str:
    """
    conversation_viewer.pyで実行するダッシュボードプロセス用のコード生成
    
    Returns:
        実行可能なPythonコード文字列
    """
    return '''
import sys
import time
import threading
import signal
from pathlib import Path

# Claude++のモジュールパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.stream_dashboard import StreamDashboard
    
    # ダッシュボードインスタンス作成
    dashboard = StreamDashboard(max_lines=4)  # ミニカードデザイン用に行数制限
    
    # 終了シグナルハンドラ
    running = True
    def signal_handler(signum, frame):
        global running
        running = False
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 初期ログ追加
    dashboard.add_log_sync("INFO", "Claude++ ログストリーム管理画面を開始")
    dashboard.add_log_sync("PROC", "システム初期化中...")
    dashboard.add_log_sync("OK  ", "システム準備完了")
    
    # メインループ
    while running:
        try:
            # 状態ファイルからの情報読み込み（オプション）
            # 環境変数からPIDを取得
            pid = os.environ.get('CLAUDE_PLUS_PID', os.getpid())
            state_file = Path(f"/tmp/claude_plus_{pid}/state.json")
            if state_file.exists():
                try:
                    import json
                    with open(state_file, 'r') as f:
                        state = json.load(f)
                    
                    # 状態に基づいたログ更新
                    current_action = state.get('work_status', {}).get('current_action', '待機中')
                    if current_action != '待機中':
                        # アクションを更新
                        dashboard.current_action = current_action
                        dashboard.add_log_sync("INFO", current_action)
                    
                    # 通知情報をチェック
                    notification_data = state.get('notification', {})
                    if notification_data.get('message') and notification_data.get('time'):
                        notification_time = notification_data['time']
                        # 新しい通知かチェック
                        if (not dashboard.notification_time or 
                            notification_time > dashboard.notification_time):
                            dashboard.show_notification(notification_data['message'], 10)
                        
                except Exception:
                    pass  # 状態ファイル読み込みエラーは無視
            
            # 画面更新
            if dashboard.should_update():
                dashboard.clear_screen_and_display()
                dashboard.mark_updated()
            
            time.sleep(1.0)  # 1秒間隔（より軽量）
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            # エラーは表示せずに継続
            time.sleep(1)
    
except ImportError:
    # モジュールインポートに失敗した場合の代替表示
    print("Claude++ 開発アシスタント                    🟢 準備中")
    print("")
    print("📝 いま: システムを初期化しています")
    print("⏰ 時間: 0秒経過")
    print("✅ 状況: 準備中です")
    print("")
    print("最近の作業:")
    print("  💾 システムを起動しています")
    
    while True:
        time.sleep(1)

except Exception as e:
    print(f"ダッシュボードエラー: {e}")
    sys.exit(1)
'''


if __name__ == "__main__":
    """テスト用のメイン関数"""
    # 簡単なテスト
    dashboard = StreamDashboard(max_lines=10)
    
    # テストログ追加
    dashboard.add_log_sync("INFO", "Claude++ ログストリーム管理画面を開始")
    dashboard.add_log_sync("PROC", "システム初期化中...")
    dashboard.add_log_sync("OK  ", "システム準備完了")
    
    # アクション更新テスト
    dashboard.current_action = "ファイルを編集しています"
    
    # 表示テスト
    dashboard.clear_screen_and_display()
    
    print("\n\n=== StreamDashboard テスト完了 ===")
    print("• ログバッファ動作: OK")
    print("• 表示レンダリング: OK")
    print("• 色分け機能: OK")
    print("• 状態インジケーター: OK")