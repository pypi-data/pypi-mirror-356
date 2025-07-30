# Claude++ Quick Setup Guide

## 修正内容（2025-01-18）

### 1. 管理画面の表示問題を修正
- **問題**: 下部の管理画面に会話履歴ビューアーが表示されていた
- **原因**: `--dashboard`オプションで起動していたため
- **修正**: `--logstream`オプションを使用してPhase 2.8のログストリーム管理画面を表示

変更箇所:
```python
# core/screen_controller.py の620行目
# 変更前: python3 {viewer_path} --dashboard
# 変更後: python3 {viewer_path} --logstream
```

### 2. tmuxセッション管理の改善
- **問題**: `tmux kill-server`は全てのtmuxセッションを終了してしまう（破壊的）
- **改善内容**:
  1. 既存セッションの再利用機能を追加
  2. セッション数制限機能（デフォルト3個まで）
  3. より安全なクリーンアップ処理

新機能:
```python
# 既存セッションの再利用
def _try_reuse_existing_session(self) -> bool:
    """既存のセッションを再利用できるか試みる"""
    # 健全なセッションがあれば再利用

# セッション数制限
def _cleanup_old_sessions(self, max_sessions: int = 3):
    """古いセッションを整理（最大数を超えないように）"""
    # アタッチされていない古いセッションから削除
```

## 期待される効果

1. **正しい管理画面表示**:
   ```
   ╭─ Claude++ 動作ログ [🟢×4] ─────────────────────╮
   │ 🔧設定読込 📋タスク解析 💾自動保存 🔔通知       │
   ├────────────────────────────────────────────────┤
   │ 20:41:22 [INFO] Claude Code 作業完了            │
   │ 20:41:23 [PROC] ファイル解析中...               │
   ╰─ 最終更新: 20:41:23 ────────────────────────────╯
   ```

2. **安全なセッション管理**:
   - 他のtmuxセッションに影響を与えない
   - Claude++のセッションのみを管理
   - 既存の健全なセッションは再利用
   - 最大3個までに制限してリソース使用を抑制

## 確認方法

```bash
# Claude++を起動
claude-plus

# 管理画面が正しく表示されることを確認
# - 上部: Claude Code CLI
# - 下部: ログストリーム管理画面（動作ログ表示）

# tmuxセッション確認
tmux list-sessions | grep claude_plus
# claude_plus_*のセッションが最大3個までになっていることを確認
```

## トラブルシューティング

もし問題が発生した場合:

1. **古いセッションのクリーンアップ**:
   ```bash
   # Claude++のセッションのみを削除
   tmux list-sessions | grep claude_plus | cut -d: -f1 | xargs -I {} tmux kill-session -t {}
   ```

2. **完全リセット（最終手段）**:
   ```bash
   # すべてのtmuxセッションを削除（注意: 他のセッションも削除される）
   tmux kill-server
   ```

3. **開発環境での確認**:
   ```bash
   cd /Users/harry/Dropbox/Tool_Development/Claude-Plus
   ./scripts/setup-dev.sh
   claude-plus-dev  # 開発版で動作確認
   ```

---

## 以前の内容: 通知設定ガイド

### 1️⃣ 通知権限の設定

システム環境設定が開いているので：

1. **左側のリストから「Terminal」を探す**
   - 「通知を許可」をオンにする
   - スタイルを「バナー」に設定

2. **左側のリストから「Script Editor」を探す**  
   - 「通知を許可」をオンにする
   - スタイルを「バナー」に設定

### 2️⃣ 動作確認

```bash
# 仮想環境をアクティベート
source venv/bin/activate

# 通知テスト実行
osascript -e 'display notification "設定完了！" with title "Claude++"'
```

### 3️⃣ Claude++ 開発環境で確認

```bash
# 開発環境起動（自動テスト付き）
claude-plus-dev
```

起動時に4つの通知（情報・成功・警告・エラー）が表示されれば成功！

### ⚠️ それでも通知が出ない場合

1. **おやすみモード確認**
   - メニューバーの右上、コントロールセンター
   - 「おやすみモード」がオフか確認

2. **macOS再起動**
   - 権限設定が反映されない場合は再起動

### 📝 重要

- **pythonコマンドが見つからない場合は必ず `source venv/bin/activate` を実行**
- **音は鳴るけど通知が出ない = 権限問題**
- **音も鳴らない = 音量またはミュート確認**