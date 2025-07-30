# Claude++ System インストールガイド

Claude CLIを究極の自動化システムに変身させるClaude++システムのインストール手順です。

## 🚀 クイックインストール（推奨）

### 方法1: ワンラインインストール
```bash
curl -fsSL https://claude-plus.jp/install | bash
```

### 方法2: pip インストール
```bash
pip install claude-plus
```

## 📋 システム要件

- **Python**: 3.10以上
- **OS**: macOS, Linux, Windows (WSL2推奨)
- **Claude Code**: 自動インストール可能
- **Git**: バージョン管理機能で必要
- **tmux**: 画面分割機能で推奨（自動インストール可能）

## 🔧 詳細なインストール方法

### 方法1: curl | bash インストール（最も簡単）
```bash
# インストーラーを実行
curl -fsSL https://claude-plus.jp/install | bash

# または、GitHubから直接
curl -fsSL https://raw.githubusercontent.com/claude-plus/claude-plus/main/deployment/online_installer.sh | bash
```

このインストーラーは以下を自動で行います：
- 依存関係のチェックと自動インストール
- Claude Codeのインストール（必要な場合）
- 仮想環境の作成と設定
- シェル設定の自動更新

### 方法2: pip インストール（Python環境がある場合）
```bash
# 最新版をインストール
pip install claude-plus

# または、ユーザーディレクトリにインストール
pip install --user claude-plus

# 特定バージョンをインストール
pip install claude-plus==2.9.0
```

### 方法3: 開発版インストール（開発者向け）
```bash
# リポジトリをクローン
git clone https://github.com/claude-plus/claude-plus.git
cd claude-plus

# 仮想環境を作成（推奨）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 開発モードでインストール
pip install -e .

# 開発用依存関係もインストール
pip install -e ".[dev]"
```

## 🔍 インストール前の確認

### Python環境の確認
```bash
python3 --version  # 3.10以上であることを確認
pip3 --version     # pipが利用可能であることを確認
```

### Claude Codeの確認（オプション）
```bash
# Claude Codeがインストールされているか確認
claude --version

# インストールされていない場合は、インストーラーが自動でインストール
```

## 3. 初期設定

### 自動セットアップの実行
```bash
# 日本語でセットアップ
claude-plus-setup --language japanese

# 英語でセットアップ
claude-plus-setup --language english
```

### 手動設定（必要に応じて）
```bash
# 設定の変更・確認
claude-plus-config
```

## 4. 動作確認

### 基本動作テスト
```bash
# Claude++システムの起動
claude-plus --help

# バージョン確認
claude-plus --version

# テスト実行
claude-plus "Hello, this is a test"
```

### 統合動作テスト
```bash
# Claude統合テスト（既存のclaudeコマンドの置き換え確認）
claude --help  # Claude++が起動することを確認
```

## 5. 使用方法

### 基本的な使い方
```bash
# Claude++システムでClaudeを起動
claude-plus

# ファイルを指定して起動
claude-plus myfile.py

# プロジェクトディレクトリで起動（Git統合有効）
cd my-project
claude-plus
```

### 自動化機能
- **自動Yes応答**: 確認プロンプトに自動で応答
- **透明Git保護**: 作業内容を自動でバックアップ
- **日本語UI**: 技術用語を分かりやすく表示
- **通知システム**: 重要な操作を音声・視覚で通知

## 6. 設定ファイル

### メイン設定ファイル
```
~/.claude-plus/config.yaml
```

### ログファイル
```
~/.claude-plus/logs/claude-plus.log
```

### バックアップディレクトリ
```
~/.claude-plus/backups/
```

## 7. トラブルシューティング

### Claude CLIが見つからない場合
```bash
# パスを確認
which claude

# 手動でパスを指定
claude-plus-config  # 設定でClaudeのパスを修正
```

### 権限エラーの場合
```bash
# ディレクトリの権限を確認
ls -la ~/.claude-plus/

# 必要に応じて権限を修正
chmod -R 755 ~/.claude-plus/
```

### 依存関係エラーの場合
```bash
# 依存関係を再インストール
pip3 install -r requirements.txt --force-reinstall

# 仮想環境での実行を推奨
python3 -m venv claude-plus-env
source claude-plus-env/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```

### Git統合の問題
```bash
# Gitリポジトリの初期化
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Git LFS（大きなファイル用）の設定
git lfs install  # 必要に応じて
```

## 8. アンインストール

```bash
# パッケージの削除
pip3 uninstall claude-plus

# 設定ファイルも削除する場合
rm -rf ~/.claude-plus/

# シェル設定からエイリアスを削除
# ~/.zshrc または ~/.bashrc からclaude-plus関連の行を削除
```

## 9. アップデート

### 開発版の場合
```bash
cd claude-plus
git pull origin main
pip3 install -r requirements.txt --upgrade
pip3 install -e . --upgrade
```

### PyPI版の場合（将来リリース予定）
```bash
pip3 install claude-plus --upgrade
```

## 10. サポート

### ログの確認
```bash
# システムログを確認
tail -f ~/.claude-plus/logs/claude-plus.log

# デバッグモードで実行
claude-plus-config  # デバッグモードを有効化
claude-plus --debug
```

### 問題の報告
1. ログファイルを確認
2. 再現手順を記録
3. GitHubのIssuesに報告

## 11. 上級者向け設定

### カスタムパターンの追加
```yaml
# ~/.claude-plus/config.yaml
auto_yes:
  patterns:
    - "Your custom pattern"
    - "カスタムパターン"
```

### 高度なGit設定
```yaml
git:
  intelligent_commits: true
  auto_branch: true
  conflict_assistance: true
```

### パフォーマンス調整
```yaml
process:
  buffer_size: 16384  # デフォルト: 8192
  max_retries: 5      # デフォルト: 3
```

---

**注意**: このシステムはClaude CLIを拡張するもので、Claude CLIの機能を置き換えるものではありません。既存のClaude CLIの全機能に加えて、自動化と保護機能を提供します。