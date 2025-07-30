# Claude++ 設定ファイル統一化ガイド

## 概要

Claude++の設定管理をシンプルにするため、これまでの3ファイル構成から1ファイル構成に移行しました。

## 変更内容

### 従来の構成（3ファイル）
- `config/config.yaml` - 基本設定
- `config/development.yaml` - 開発環境設定
- `config/production.yaml` - 本番環境設定

### 新しい構成（1ファイル）
- `config/config.yaml` - 統一設定（環境変数で制御）

## 環境変数による制御

以下の環境変数で開発/本番を切り替えます：

| 環境変数 | 説明 | デフォルト値 |
|---------|------|------------|
| `CLAUDE_PLUS_ENV` | 環境（development/production） | production |
| `CLAUDE_PLUS_DEBUG` | デバッグモード | false |
| `CLAUDE_PLUS_LOG_LEVEL` | ログレベル | INFO |
| `CLAUDE_PLUS_LOG_FILE` | ログファイルパス | /tmp/claude-plus.log |
| `CLAUDE_PLUS_AUTO_RELOAD` | 自動リロード | false |
| `CLAUDE_PLUS_DEVELOPMENT_MODE` | 開発モードフラグ | false |

## 開発環境の設定方法

### 方法1: 環境変数を直接設定
```bash
export CLAUDE_PLUS_ENV=development
export CLAUDE_PLUS_DEBUG=true
export CLAUDE_PLUS_LOG_LEVEL=DEBUG
export CLAUDE_PLUS_LOG_FILE=/tmp/claude-plus-dev.log
export CLAUDE_PLUS_AUTO_RELOAD=true
export CLAUDE_PLUS_DEVELOPMENT_MODE=true

claude-plus
```

### 方法2: スクリプトを使用（推奨）
```bash
source scripts/set_dev_env.sh
claude-plus
```

### 方法3: 環境変数を一時的に設定
```bash
CLAUDE_PLUS_ENV=development CLAUDE_PLUS_DEBUG=true claude-plus
```

## 設定ファイルの書き方

config.yamlでは環境変数を以下の形式で参照できます：

```yaml
system:
  debug: ${CLAUDE_PLUS_DEBUG:-false}  # 環境変数CLAUDE_PLUS_DEBUGを使用、未設定ならfalse
  
logging:
  level: ${CLAUDE_PLUS_LOG_LEVEL:-INFO}  # 環境変数を使用、未設定ならINFO
```

## 移行完了

- **2025年1月**: 環境別ファイル（development.yaml, production.yaml）を削除
- **現在**: config.yamlのみを使用（環境変数で制御）

## メリット

1. **設定の一貫性**: 環境間の設定差異が最小限に
2. **メンテナンス性**: 1ファイルのみ管理
3. **エラー削減**: 設定の不整合によるエラーを防止
4. **デプロイ簡素化**: 環境変数で簡単に切り替え

## 注意事項

- 環境変数が設定されていない場合、デフォルト値（本番環境用）が使用されます
- `claude-plus-dev`コマンドは引き続き開発環境として動作します
- 環境別ファイルは削除されたため、全ての設定はconfig.yamlで管理されます