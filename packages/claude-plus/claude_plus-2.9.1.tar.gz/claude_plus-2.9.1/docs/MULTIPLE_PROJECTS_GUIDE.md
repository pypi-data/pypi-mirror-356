# 複数プロジェクト同時開発ガイド

Claude++で複数のプロジェクトを同時に開発する方法を説明します。

## 🎯 概要

Claude++はPIDベース分離システムにより、複数のプロジェクトを完全に独立して同時に実行できます。

## 🚀 基本的な使い方

### 1. 複数プロジェクトの起動

**プロジェクトA（ターミナル1）:**
```bash
cd /path/to/your/project_a
claude-plus
```

**プロジェクトB（ターミナル2）:**
```bash  
cd /path/to/your/project_b
claude-plus
```

**プロジェクトC（ターミナル3）:**
```bash
cd /path/to/your/project_c
claude-plus
```

### 2. 確認方法

各プロジェクトは完全に独立して動作します：

- 🖥️ **画面**: 各ターミナルで独立したClaude++画面
- 📁 **作業ディレクトリ**: 正しいプロジェクトディレクトリ
- 🔔 **通知**: プロジェクト別の通知表示
- 📊 **状態管理**: 独立した作業状態

## ✅ 利点

### 完全な独立性
- ✅ 一つのプロジェクトがクラッシュしても他に影響なし
- ✅ 各プロジェクトで異なる設定・操作が可能
- ✅ Git操作も完全に独立

### 効率的な開発
- ✅ プロジェクト切り替えのオーバーヘッドなし
- ✅ 複数のコードベースを同時に確認・編集
- ✅ 比較開発や参照作業が簡単

### リソース最適化
- ✅ 使用する分だけリソースを消費
- ✅ 不要なプロジェクトは終了してリソース節約
- ✅ 起動時間は単独実行と同等

## 🔍 動作の仕組み

### PIDベース分離
```
プロジェクトA (PID: 1234)
└── /tmp/claude_plus_1234/
    ├── state.json
    ├── cmd (通信パイプ)
    └── output (通信パイプ)

プロジェクトB (PID: 5678)  
└── /tmp/claude_plus_5678/
    ├── state.json
    ├── cmd (通信パイプ)
    └── output (通信パイプ)
```

### tmuxセッション分離
```
tmux list-sessions:
claude_plus_1234: (プロジェクトA用)
claude_plus_5678: (プロジェクトB用)
```

## 💡 おすすめの使用パターン

### パターン1: フロントエンド・バックエンド開発
```bash
# ターミナル1: フロントエンド
cd ~/projects/my-app-frontend
claude-plus

# ターミナル2: バックエンドAPI
cd ~/projects/my-app-backend  
claude-plus
```

### パターン2: メイン・実験プロジェクト
```bash
# ターミナル1: メインプロジェクト
cd ~/projects/main-project
claude-plus

# ターミナル2: 実験・検証用
cd ~/experiments/new-feature-test
claude-plus
```

### パターン3: 複数クライアント案件
```bash
# ターミナル1: クライアントA
cd ~/work/client-a-project
claude-plus

# ターミナル2: クライアントB
cd ~/work/client-b-project
claude-plus
```

## 🛠️ 管理方法

### アクティブなプロジェクトの確認

**PIDディレクトリで確認:**
```bash
ls /tmp/claude_plus_*/
# 出力例:
# /tmp/claude_plus_1234/state.json
# /tmp/claude_plus_5678/state.json
```

**tmuxセッションで確認:**
```bash
tmux list-sessions | grep claude_plus
# 出力例:
# claude_plus_1234: 2 windows
# claude_plus_5678: 2 windows
```

### プロジェクトの終了

各ターミナルで通常通り`Ctrl+C`で終了するか、ターミナルを閉じるだけです。

```bash
# 通常の終了
Ctrl+C

# または強制終了
pkill -f "claude-plus.*PID"
```

## 🚨 注意事項

### リソース使用量
- 各プロジェクトは独立したプロセスとして動作
- メモリ使用量は実行プロジェクト数に比例
- 不要なプロジェクトは終了してリソース節約

### ポート競合
- 同じポートを使用するプロジェクトは注意
- 開発サーバーのポート設定を確認

### Git操作
- 各プロジェクトのGit操作は完全に独立
- 間違ったプロジェクトでコミットしないよう注意

## 🔧 トラブルシューティング

### Q: プロジェクトが起動しない
**A:** 既存のプロセスを確認して終了してください
```bash
ps aux | grep claude-plus
kill PID
```

### Q: 古いPIDディレクトリが残っている
**A:** 手動で削除するか、新しいclaude-plusを起動すると自動削除されます
```bash
rm -rf /tmp/claude_plus_*
```

### Q: tmuxセッションが残っている
**A:** 手動で削除してください
```bash
tmux kill-session -t claude_plus_PID
```

## 📊 システム要件

- **OS**: macOS, Linux
- **メモリ**: プロジェクトあたり約50MB
- **ディスク**: 一時ファイル用に数KB
- **CPU**: 追加の負荷は最小限

## 🎉 まとめ

Claude++の複数プロジェクト同時開発機能により：

1. **効率的**: 複数のコードベースを同時に扱える
2. **安全**: 完全に独立した動作で相互影響なし  
3. **簡単**: 従来と同じ`claude-plus`コマンドを使用
4. **柔軟**: 必要な分だけプロジェクトを起動

これで複数のプロジェクトを並行して効率的に開発できます！