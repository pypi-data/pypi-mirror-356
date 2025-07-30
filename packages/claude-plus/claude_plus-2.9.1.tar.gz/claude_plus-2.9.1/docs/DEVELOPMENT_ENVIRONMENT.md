# Claude++ 開発環境ガイド

## 開発環境での起動方法（Phase 2.7以降）

### 1. venvをアクティベートして使う方法
```bash
cd /Users/harry/Dropbox/Tool_Development/Claude-Plus
source venv/bin/activate
claude-plus-dev  # または claude-plus
```

### 2. venvを直接使う方法（推奨 - 環境を汚さない）
```bash
cd /Users/harry/Dropbox/Tool_Development/Claude-Plus
venv/bin/claude-plus-dev  # または venv/bin/claude-plus
```

### 3. editable installした後の方法
```bash
cd /Users/harry/Dropbox/Tool_Development/Claude-Plus
pip install -e .  # 初回のみ
claude-plus-dev   # システムのどこからでも使える
```

## 本番環境との違い

### 開発環境
- **場所**: プロジェクトディレクトリ内のvenv
- **特徴**: コード変更が即座に反映される（editable install）
- **用途**: Claude++の開発・デバッグ

### 本番環境  
- **場所**: `~/.claude-plus-venv`
- **特徴**: 安定版のみ、どこからでも利用可能
- **用途**: 通常の作業での使用

## トラブルシューティング

### claude-plus-devが動作しない場合
1. editable installを実行:
   ```bash
   pip install -e .
   ```

2. 直接venvから実行:
   ```bash
   venv/bin/claude-plus-dev
   ```

### 古いpipx環境が残っている場合
```bash
# pipx版をアンインストール
pipx uninstall claude-plus

# 本番環境を再セットアップ
./scripts/setup-production.sh
```

## 環境変数による制御

開発/本番の明示的な指定:
```bash
# 開発環境を強制
CLAUDE_PLUS_ENV=development claude-plus

# 本番環境を強制
CLAUDE_PLUS_ENV=production claude-plus
```

通常は自動判定されるため、環境変数の設定は不要です。