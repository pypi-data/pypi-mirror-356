# TestPyPI アップロードガイド

## 📋 現在の準備状況

✅ **完了済み**
- パッケージビルド（claude_plus-2.9.0）
- 必要なツールのインストール（twine, wheel）
- .pypirc.sample設定テンプレート準備
- dist/ディレクトリにアップロード用ファイル準備完了

⏳ **残りのステップ**
1. TestPyPIアカウント作成
2. APIトークン生成
3. ~/.pypirc設定
4. TestPyPIへアップロード

## 🚀 TestPyPIアカウント作成手順

### 1. アカウント作成
1. ブラウザで https://test.pypi.org/account/register/ にアクセス
2. 以下の情報を入力：
   - Username: お好きなユーザー名
   - Email: メールアドレス
   - Password: 安全なパスワード
3. メール認証を完了

### 2. APIトークン生成
1. ログイン後、右上のユーザー名をクリック
2. 「Account settings」を選択
3. スクロールして「API tokens」セクションを探す
4. 「Add API token」ボタンをクリック
5. トークン設定：
   - Token name: `claude-plus-testpypi`
   - Scope: `Entire account (all projects)`
6. 「Add token」をクリック
7. **重要**: 表示されたトークンをコピー（`pypi-`で始まる長い文字列）
   - このトークンは二度と表示されません！

### 3. ~/.pypirc設定
```bash
# 設定ファイルをコピー
cp .pypirc.sample ~/.pypirc

# セキュリティのため権限を設定
chmod 600 ~/.pypirc

# エディタで開いて編集
nano ~/.pypirc  # または好きなエディタ
```

以下の部分を編集：
```ini
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-API-TOKEN-HERE  # ← ここにコピーしたトークンを貼り付け
```

## 📤 TestPyPIへのアップロード

準備が整ったら、以下のコマンドでアップロード：

```bash
# スクリプトを使用する場合
./deployment/publish_pypi.sh --skip-tests --test

# または直接twineを使用
python -m twine upload --repository testpypi dist/*
```

## 🧪 インストールテスト

アップロード成功後、別の環境でテスト：

```bash
# 新しい仮想環境を作成
python3 -m venv test_install
source test_install/bin/activate

# TestPyPIからインストール
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple claude-plus

# 動作確認
claude-plus --help  # または実際に起動してテスト
```

## ⚠️ 注意事項

1. **TestPyPIの制限**
   - 依存パッケージが見つからない場合があるため、`--extra-index-url`で本番PyPIも参照
   - アップロードしたパッケージは削除できません（ただしTestPyPIなので問題なし）

2. **トークンの管理**
   - APIトークンは絶対に公開しない
   - Gitにコミットしない（.gitignoreで ~/.pypirc を除外済み）

3. **次のステップ**
   - TestPyPIで問題なく動作確認できたら、本番PyPIへのアップロードを検討

## 🆘 トラブルシューティング

### アップロードエラー
- 「403 Forbidden」: APIトークンが正しくない、または権限不足
- 「400 Bad Request」: パッケージ名が既に使用されている
- ネットワークエラー: プロキシ設定を確認

### インストールエラー
- 依存関係エラー: `--extra-index-url https://pypi.org/simple`を追加
- バージョン競合: 仮想環境をクリーンに作成

## 📝 現在の状態

- パッケージ名: `claude-plus`
- バージョン: `2.9.0`
- ビルド済みファイル:
  - `dist/claude_plus-2.9.0-py3-none-any.whl`
  - `dist/claude_plus-2.9.0.tar.gz`

TestPyPIアカウントを作成してAPIトークンを取得したら、すぐにアップロードできる状態です！