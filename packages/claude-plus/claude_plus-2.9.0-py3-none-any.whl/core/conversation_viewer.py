#!/usr/bin/env python3
"""
Claude++ 会話履歴ビューアー / 安心ダッシュボード
上部ペイン（Claude Code CLI）の内容をリアルタイムで表示・スクロール可能
--dashboard オプションで安心ダッシュボードモードで起動
Phase 2.8: ログストリーム管理画面対応
"""

import sys
import time
import os
import subprocess
from datetime import datetime
import signal
import threading
import select
from pathlib import Path

class ConversationViewer:
    """会話履歴ビューアークラス"""
    
    def __init__(self, session_name=None, dashboard_mode=False):
        # 環境変数からPIDを取得
        self.pid = os.environ.get('CLAUDE_PLUS_PID', os.getpid())
        
        self.session_name = session_name or self._find_active_session()
        self.claude_pane = f"{self.session_name}:0.0"
        self.running = True
        self.display_lines = []
        self.scroll_offset = 0
        
        # Phase 2.8: ダッシュボードモード対応
        self.dashboard_mode = dashboard_mode
        self.stream_dashboard = None
        
        # ダッシュボードモードの場合はStreamDashboardを初期化
        if dashboard_mode:
            try:
                import sys
                from pathlib import Path
                # プロジェクトルートをpathに追加
                project_root = Path(__file__).parent.parent
                if str(project_root) not in sys.path:
                    sys.path.append(str(project_root))
                
                from core.stream_dashboard import StreamDashboard
                self.stream_dashboard = StreamDashboard(max_lines=25)  # 画面分割用に削減
            except ImportError as e:
                print(f"Warning: StreamDashboard import failed: {e}")
                self.dashboard_mode = False
        
        # 画面サイズを取得
        self.screen_height = self._get_screen_height()
        
        # シグナルハンドラ設定
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _find_active_session(self):
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
    
    def _get_screen_height(self):
        """画面の高さを取得"""
        try:
            result = subprocess.run(
                ["tmux", "display-message", "-p", "#{pane_height}"],
                capture_output=True, text=True
            )
            return max(10, int(result.stdout.strip()) - 5)  # ヘッダー分を引く
        except:
            return 15
    
    def _signal_handler(self, signum, frame):
        """シグナルハンドラ"""
        self.running = False
        sys.exit(0)
    
    def capture_conversation(self):
        """Claude Code CLIの会話内容をキャプチャ"""
        try:
            result = subprocess.run(
                ["tmux", "capture-pane", "-t", self.claude_pane, "-p", "-S", "-"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                # 空行を除去し、実際の会話内容のみを抽出
                lines = result.stdout.split('\n')
                conversation_lines = []
                
                for line in lines:
                    # Claude Code CLIの会話パターンを検出
                    stripped = line.strip()
                    if stripped and not stripped.startswith('cwd:'):
                        conversation_lines.append(line.rstrip())
                
                return conversation_lines
            
            return []
        except Exception as e:
            return [f"エラー: {e}"]
    
    def display_content(self):
        """会話内容を表示"""
        # Phase 2.8: ダッシュボードモードの場合は専用表示
        if self.dashboard_mode and self.stream_dashboard:
            self.stream_dashboard.clear_screen_and_display()
            return
        
        # 従来の会話履歴表示
        # 画面をクリア
        os.system('clear')
        
        # ヘッダーを表示
        print("═" * 70)
        print("             Claude++ 会話履歴ビューアー")
        print(f"             セッション: {self.session_name}")
        print("═" * 70)
        print("⌨️  操作: j/k=スクロール | Space/b=ページ移動 | Tab=上部ペインに戻る | q=終了")
        print("─" * 70)
        
        # 会話内容を表示（スクロール考慮）
        total_lines = len(self.display_lines)
        start_idx = max(0, total_lines - self.screen_height + self.scroll_offset)
        end_idx = min(total_lines, start_idx + self.screen_height)
        
        displayed_lines = self.display_lines[start_idx:end_idx]
        
        for line in displayed_lines:
            print(line)
        
        # フッターを表示
        if total_lines > self.screen_height:
            scroll_info = f"[{start_idx + 1}-{end_idx}/{total_lines}行]"
            print("─" * 70)
            print(f"📜 {scroll_info} スクロール: j(下) k(上) Space(次ページ) b(前ページ)")
        
        # リアルタイム更新インジケーター
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"🔄 最終更新: {current_time}")
    
    def handle_keyboard_input(self):
        """キーボード入力を処理"""
        try:
            # 非ブロッキング入力設定
            import tty, termios
            old_settings = termios.tcgetattr(sys.stdin)
            tty.raw(sys.stdin.fileno())
            
            while self.running:
                # 0.1秒のタイムアウトで入力をチェック
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    char = sys.stdin.read(1)
                    
                    if char == 'q':
                        self.running = False
                        break
                    elif char == 'j':  # 下にスクロール
                        if self.scroll_offset > -(len(self.display_lines) - self.screen_height):
                            self.scroll_offset -= 1
                    elif char == 'k':  # 上にスクロール
                        if self.scroll_offset < 0:
                            self.scroll_offset += 1
                    elif char == ' ':  # 次のページ
                        self.scroll_offset -= self.screen_height
                        self.scroll_offset = max(self.scroll_offset, -(len(self.display_lines) - self.screen_height))
                    elif char == 'b':  # 前のページ
                        self.scroll_offset += self.screen_height
                        self.scroll_offset = min(self.scroll_offset, 0)
                    elif char == '\t':  # Tabキー：上部ペインに戻る
                        subprocess.run([
                            "tmux", "select-pane", "-t", self.claude_pane
                        ], capture_output=True)
                    
                    # 表示を更新
                    self.display_content()
                
                time.sleep(0.1)
                
        except Exception as e:
            pass
        finally:
            # ターミナル設定を復元
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except:
                pass
    
    def start_viewer(self):
        """ビューアーを開始"""
        # Phase 2.8: ダッシュボードモードの場合は専用メッセージ
        if self.dashboard_mode:
            print("📊 Claude++ ログストリーム管理画面を開始しています...")
            
            # ダッシュボード用の初期ログ追加
            if self.stream_dashboard:
                self.stream_dashboard.add_log_sync("INFO", "Claude++ ログストリーム画面を開始")
                self.stream_dashboard.add_log_sync("PROC", "システム初期化中...")
                self.stream_dashboard.add_log_sync("INFO", "リアルタイム監視を開始")
        else:
            print("🎬 Claude++ 会話履歴ビューアーを開始しています...")
        
        time.sleep(1)
        
        # Phase 2.8: ダッシュボードモード専用の更新ロジック
        if self.dashboard_mode and self.stream_dashboard:
            def update_dashboard():
                while self.running:
                    try:
                        # 状態ファイルからの情報読み込み
                        state_file = Path("/tmp/claude_plus_state.json")
                        if state_file.exists():
                            try:
                                import json
                                with open(state_file, 'r') as f:
                                    state = json.load(f)
                                
                                # 状態に基づいたログ更新
                                current_action = state.get('work_status', {}).get('current_action', '待機中')
                                if hasattr(self, '_last_action') and current_action != self._last_action:
                                    if current_action != '待機中':
                                        self.stream_dashboard.add_log_sync("TASK", current_action)
                                    self._last_action = current_action
                                
                                # プロセス数更新（非同期でも動作）
                                stats = state.get('statistics', {})
                                process_count = 1 if current_action != '待機中' else 0
                                import asyncio
                                try:
                                    loop = asyncio.get_event_loop()
                                    if loop.is_running():
                                        asyncio.ensure_future(self.stream_dashboard.update_process_count(process_count))
                                except:
                                    pass  # asyncioが利用できない場合は無視
                                        
                            except Exception:
                                pass  # 状態ファイル読み込みエラーは無視
                        
                        # 画面更新
                        if self.stream_dashboard.should_update():
                            self.stream_dashboard.clear_screen_and_display()
                            self.stream_dashboard.mark_updated()
                        
                        time.sleep(0.5)  # 0.5秒間隔
                        
                    except Exception:
                        time.sleep(1)
            
            # ダッシュボード更新スレッドを開始
            self._last_action = '初期化中'
            update_thread = threading.Thread(target=update_dashboard, daemon=True)
            update_thread.start()
            
            # 初回表示
            self.display_content()
            
            # キーボード入力処理
            self.handle_keyboard_input()
            
        else:
            # 従来の会話履歴ビューアーロジック
            def update_conversation():
                while self.running:
                    new_content = self.capture_conversation()
                    if new_content != self.display_lines:
                        self.display_lines = new_content
                        # 最新のメッセージを表示するため、スクロールをリセット
                        if self.scroll_offset == 0:
                            self.display_content()
                    time.sleep(2)  # 2秒ごとに更新
            
            # 更新スレッドを開始
            update_thread = threading.Thread(target=update_conversation, daemon=True)
            update_thread.start()
            
            # 初回表示
            self.display_lines = self.capture_conversation()
            self.display_content()
            
            # キーボード入力処理
            self.handle_keyboard_input()

    def create_panes_layout(self) -> bool:
        """
        tmuxペイン分割レイアウトを作成
        Phase 2.8: ダッシュボード表示用のペイン作成
        """
        try:
            # 既存のpane分割が存在するかチェック
            result = subprocess.run(
                ["tmux", "list-panes", "-t", self.session_name],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                panes = result.stdout.strip().split('\n')
                if len(panes) >= 2:
                    return True  # 既に分割済み
            
            # 下部にダッシュボード用ペインを作成（20%の高さ - ミニカードデザイン用）
            split_result = subprocess.run([
                "tmux", "split-window", "-t", self.session_name, 
                "-v", "-p", "20", "-c", os.getcwd()
            ], capture_output=True)
            
            if split_result.returncode != 0:
                return False
            
            # 下部ペインでダッシュボードを実行
            if self.dashboard_mode:
                # Phase 2.8: StreamDashboard を下部ペインで実行
                dashboard_command = self._get_dashboard_command()
                
                send_result = subprocess.run([
                    "tmux", "send-keys", "-t", f"{self.session_name}:0.1",
                    dashboard_command, "Enter"
                ], capture_output=True)
                
                return send_result.returncode == 0
            
            return True
            
        except Exception as e:
            print(f"ペイン作成エラー: {e}")
            return False
    
    def _get_dashboard_command(self) -> str:
        """ダッシュボード実行用のコマンドを生成"""
        # Python実行コマンドの生成
        python_exec = sys.executable
        script_path = Path(__file__).parent / "stream_dashboard.py"
        
        # StreamDashboard実行用のコマンド
        return f"{python_exec} -c \"{self._get_dashboard_inline_code()}\""
    
    def _get_dashboard_inline_code(self) -> str:
        """ダッシュボード実行用のインラインコードを生成"""
        from core.stream_dashboard import create_dashboard_process_code
        return create_dashboard_process_code().replace('"', '\\"').replace('\n', '\\n')


def main():
    """メイン関数"""
    # プロジェクトルートをpathに追加（共通処理）
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
    
    # コマンドライン引数をチェック
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--dashboard":
            # 従来のダッシュボードモード（後方互換性）
            try:
                
                from core.dashboard import ClaudeDashboard
                dashboard = ClaudeDashboard()
                dashboard.run()
            except ImportError:
                print("エラー: ダッシュボードモジュールが見つかりません")
                print("通常のビューアーモードで起動します...")
                viewer = ConversationViewer()
                viewer.start_viewer()
            except KeyboardInterrupt:
                print("\n\n👋 Claude++ 安心ダッシュボードを終了します...")
            except Exception as e:
                print(f"\nエラーが発生しました: {e}")
                
        elif arg == "--logstream":
            # Phase 2.8: 新しいログストリーム管理画面モード
            try:
                from core.stream_dashboard import StreamDashboard
                dashboard = StreamDashboard()
                # ログサンプルを追加
                dashboard.add_log_sync("INFO", "Claude++ ログストリーム管理画面を開始")
                dashboard.add_log_sync("PROC", "システム初期化中...")
                dashboard.add_log_sync("OK  ", "システム準備完了")
                
                # メインループ
                dashboard.run_display_loop()
            except ImportError as e:
                print("エラー: ログストリームモジュールが見つかりません")
                print(f"詳細: {e}")
                print("通常のビューアーモードで起動します...")
                viewer = ConversationViewer()
                viewer.start_viewer()
            except KeyboardInterrupt:
                print("\n\n👋 Claude++ ログストリーム管理画面を終了します...")
            except Exception as e:
                print(f"\nエラーが発生しました: {e}")
        else:
            # 引数が不明の場合は通常モード
            viewer = ConversationViewer()
            viewer.start_viewer()
    else:
        # 通常のビューアーモードで起動
        try:
            viewer = ConversationViewer()
            viewer.start_viewer()
        except KeyboardInterrupt:
            print("\n\n👋 Claude++ 会話履歴ビューアーを終了します...")
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
        finally:
            sys.exit(0)

if __name__ == "__main__":
    main()