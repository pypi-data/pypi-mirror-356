# Claude++ System トラブルシューティングガイド

## 🚨 緊急時の対応

### 緊急リセット（最優先）
```bash
# 全てが動かない場合
claude-plus --emergency-reset

# 最新の安全な状態に復旧
claude-plus --restore-latest

# 完全クリーンアップ（最終手段）
rm -rf ~/.claude-plus && curl -fsSL https://claude-plus.dev/install.sh | sh
```

### 作業データの緊急保護
```bash
# 現在の作業を即座に保存
claude-plus --emergency-save

# 作業ディレクトリのバックアップ
claude-plus --backup-current-work

# 復旧ポイント一覧確認
claude-plus --show-recovery-points
```

---

## 🔍 診断コマンド

### システム状態の確認
```bash
# 完全診断レポート生成
claude-plus --diagnose

# システム健全性チェック
claude-plus --health-check

# 設定検証
claude-plus --validate-config

# パフォーマンス測定
claude-plus --performance-test
```

### ログの確認方法
```bash
# リアルタイムログ表示
tail -f ~/.claude-plus/logs/claude-plus.log

# エラーログのみ表示
grep "ERROR" ~/.claude-plus/logs/claude-plus.log

# 直近1時間のログ
find ~/.claude-plus/logs -mmin -60 -type f -exec cat {} \;

# デバッグモードでの詳細ログ
claude-plus --debug --verbose
```

---

## 💻 インストール関連の問題

### インストール失敗のトラブルシューティング

#### Python 関連エラー
```bash
# エラー: "Python 3.13+ required"
python3 --version
# 3.13未満の場合は Python をアップデート

# 仮想環境での隔離インストール
python3 -m venv claude-plus-env
source claude-plus-env/bin/activate
curl -fsSL https://claude-plus.dev/install.sh | sh
```

#### 権限エラー
```bash
# エラー: "Permission denied"
sudo chown -R $USER ~/.claude-plus
chmod -R 755 ~/.claude-plus

# 管理者権限が必要な場合
sudo curl -fsSL https://claude-plus.dev/install.sh | sh
```

#### ネットワーク関連エラー
```bash
# プロキシ環境での設定
export http_proxy=your-proxy:port
export https_proxy=your-proxy:port
curl -fsSL https://claude-plus.dev/install.sh | sh

# オフライン環境での手動インストール
wget https://github.com/claude-plus/claude-plus/archive/main.zip
unzip main.zip && cd claude-plus-main
./install.sh --offline
```

---

## 🎮 実行時の問題

### 起動エラー

#### "Command not found: claude"
```bash
# PATH 確認
echo $PATH | grep claude

# Claude CLI の再インストール
claude-plus --reinstall-claude-cli

# 手動パス設定
export PATH="$PATH:~/.claude-plus/bin"
echo 'export PATH="$PATH:~/.claude-plus/bin"' >> ~/.bashrc
```

#### "ModuleNotFoundError"
```bash
# 依存関係の再インストール
cd ~/.claude-plus && pip install -r requirements.txt

# 環境変数の確認
echo $PYTHONPATH
export PYTHONPATH="$PYTHONPATH:~/.claude-plus"

# 仮想環境の確認
which python3
```

#### 設定ファイルエラー
```bash
# 設定ファイルの初期化
claude-plus --reset-config

# 設定ファイルの手動修復
cp ~/.claude-plus/config.yaml.backup ~/.claude-plus/config.yaml

# デフォルト設定での起動
claude-plus --default-config
```

### 実行中のエラー

#### プロセスが応答しない
```bash
# プロセス確認
ps aux | grep claude-plus

# 強制終了
pkill -f claude-plus

# 安全な再起動
claude-plus --safe-restart
```

#### メモリ不足エラー
```bash
# 軽量モードでの起動
claude-plus --lite-mode

# メモリクリーンアップ
claude-plus --cleanup-memory

# 設定での自動最適化
claude-plus-config --memory-optimize
```

#### CPU 使用率が高い
```bash
# 処理の一時停止
claude-plus --pause

# パフォーマンス調整
claude-plus --reduce-cpu-usage

# プロセス監視
top -p $(pgrep claude-plus)
```

---

## 🖥️ 画面分割関連の問題

### tmux が動作しない
```bash
# tmux インストール確認
which tmux || brew install tmux  # macOS
which tmux || sudo apt install tmux  # Linux

# tmux セッションの確認
tmux list-sessions

# セッションの強制終了
tmux kill-session -t claude_plus_*

# フォールバックモードでの起動
claude-plus --no-tmux
```

### 画面レイアウトが崩れる
```bash
# レイアウトのリセット
claude-plus --reset-layout

# ターミナルサイズの確認
echo "COLUMNS=$COLUMNS LINES=$LINES"

# 手動レイアウト調整
tmux resize-pane -t claude_plus:0.0 -y 70%
tmux resize-pane -t claude_plus:0.1 -y 30%
```

### コントロールパネルが表示されない
```bash
# コントロールパネルの再起動
claude-plus --restart-control-panel

# 手動でのパネル起動
python3 ~/.claude-plus/core/control_panel.py

# ログでの確認
grep "control.panel" ~/.claude-plus/logs/claude-plus.log
```

---

## 🔧 Git 統合の問題

### Git 操作エラー
```bash
# Git 設定確認
git config --global user.name
git config --global user.email

# リポジトリの状態確認
git status
git log --oneline -10

# Git 統合のリセット
claude-plus --reset-git-integration
```

### ブランチ作成エラー
```bash
# 現在のブランチ確認
git branch -a

# ブランチクリーンアップ
git branch -d $(git branch | grep work/)

# 手動ブランチ作成
git checkout -b work/$(date +%Y%m%d-%H%M)
```

### 自動コミットの問題
```bash
# 自動コミット設定確認
claude-plus-config --show | grep auto_commit

# 手動でのコミット
git add . && git commit -m "手動保存: $(date)"

# 自動コミットの無効化
claude-plus-config --set auto_commit false
```

---

## 🌐 ネットワーク・API の問題

### Claude API エラー
```bash
# API キーの確認
echo $ANTHROPIC_API_KEY | head -c 20

# API 接続テスト
curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages

# API 設定のリセット
claude-plus --reset-api-config
```

### 接続タイムアウト
```bash
# タイムアウト設定の確認
claude-plus-config --show | grep timeout

# タイムアウト値の増加
claude-plus-config --set network_timeout 60

# リトライ設定の調整
claude-plus-config --set max_retries 5
```

### プロキシ設定
```bash
# プロキシ設定の確認
env | grep -i proxy

# Claude++ でのプロキシ設定
claude-plus-config --set proxy_url "http://proxy:port"

# 認証付きプロキシ
claude-plus-config --set proxy_url "http://user:pass@proxy:port"
```

---

## 📊 パフォーマンスの問題

### 起動が遅い
```bash
# 起動時間の測定
time claude-plus --version

# 軽量起動モード
claude-plus --fast-start

# 不要なモジュールの無効化
claude-plus-config --disable-modules "notifications,animations"
```

### 応答が遅い
```bash
# パフォーマンス測定
claude-plus --benchmark

# キャッシュのクリア
claude-plus --clear-cache

# 並列処理の調整
claude-plus-config --set max_workers 4
```

### メモリリーク
```bash
# メモリ使用量監視
watch -n 5 'ps -o pid,ppid,cmd,%mem,%cpu -p $(pgrep claude-plus)'

# メモリ使用量の制限
ulimit -m 512000  # 512MB制限

# ガベージコレクションの強制実行
claude-plus --force-gc
```

---

## 🛡️ セキュリティ関連の問題

### ファイル権限エラー
```bash
# 権限の確認
ls -la ~/.claude-plus/

# 権限の修復
find ~/.claude-plus -type f -exec chmod 644 {} \;
find ~/.claude-plus -type d -exec chmod 755 {} \;
chmod +x ~/.claude-plus/bin/claude-plus
```

### API キーの問題
```bash
# API キーの検証
claude-plus --validate-api-key

# API キーの再設定
claude-plus --setup-api-key

# 環境変数での設定
export ANTHROPIC_API_KEY="your-key"
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc
```

---

## 🔧 高度なデバッグ

### ログレベルの調整
```bash
# 詳細ログの有効化
claude-plus-config --set log_level DEBUG

# 特定モジュールのログ
claude-plus-config --set module_log_level.git_pro DEBUG

# ログファイルのローテーション
claude-plus --rotate-logs
```

### プロファイリング
```bash
# パフォーマンスプロファイル
claude-plus --profile

# メモリプロファイル
claude-plus --memory-profile

# CPU プロファイル
claude-plus --cpu-profile
```

### デバッグモード
```bash
# 完全デバッグモード
claude-plus --debug --verbose --trace

# ステップ実行モード
claude-plus --step-by-step

# ブレークポイントの設定
claude-plus --break-on-error
```

---

## 📞 サポートリクエスト

### バグレポートの作成
```bash
# 自動バグレポート生成
claude-plus --generate-bug-report

# システム情報の収集
claude-plus --system-info > system-info.txt

# ログの圧縮
tar -czf claude-plus-logs.tar.gz ~/.claude-plus/logs/
```

### 情報収集コマンド
```bash
# 完全診断レポート
claude-plus --full-diagnostics > diagnostics-$(date +%Y%m%d).txt

# 設定情報のエクスポート
claude-plus-config --export > config-backup.yaml

# 実行環境情報
uname -a && python3 --version && git --version > env-info.txt
```

---

## 🔄 復旧手順

### 段階的復旧プロセス
1. **軽微な復旧**: `claude-plus --soft-reset`
2. **設定復旧**: `claude-plus --reset-config`
3. **完全復旧**: `claude-plus --full-reset`
4. **再インストール**: 完全削除後の新規インストール

### データ保護の確認
```bash
# バックアップの確認
ls -la ~/.claude-plus/backups/

# 作業データの確認
git log --oneline | head -20

# 復旧ポイントの検証
claude-plus --verify-recovery-points
```

---

**🆘 この手順で解決しない場合は、GitHub Issues または Discord でサポートを求めてください。**

最終更新: 2025/01/13