# PyPI 簡単セットアップガイド

## 🎯 最速セットアップ（10分で完了）

### 📌 重要なお知らせ
- **ユーザーは`pip install claude-plus`するだけ**（トークン不要）
- APIトークンは**あなた（配布者）だけ**が必要
- 2024年から2要素認証が必須になりました

## 🚀 ステップ1: アカウント作成（3分）

1. **PyPIアカウント作成**
   - https://pypi.org/account/register/ にアクセス
   - Username、Email、Passwordを入力
   - メールで確認リンクをクリック

2. **2要素認証設定（必須）**
   - ログイン後、Account settings → Add 2FA
   - スマホでGoogle AuthenticatorかAuthyをインストール
   - QRコードをスキャン
   - リカバリーコードを保存（重要！）

## 🔑 ステップ2: APIトークン生成（2分）

1. Account settings → API tokens
2. 「Add API token」クリック
3. 設定：
   - Token name: `claude-plus`
   - Scope: `Project: claude-plus`（まだない場合は`Entire account`）
4. トークンをコピー（`pypi-`で始まる長い文字列）

## ⚡ ステップ3: 環境変数で設定（最も簡単）

```bash
# ターミナルで実行（~/.pypircより簡単で安全）
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-ここにコピーしたトークンを貼り付け
```

## 📤 ステップ4: アップロード（1分）

```bash
# 既にビルド済みなので、そのままアップロード
python -m twine upload dist/*
```

## ✅ 完了！

これで世界中の人が以下でインストールできます：
```bash
pip install claude-plus
```

---

## 🔐 セキュリティについて

**Q: APIトークンのセキュリティは大丈夫？**
A: はい、完全に安全です。
- トークンは**配布時のみ**使用
- パッケージには含まれません
- ユーザーには見えません

**Q: ユーザーに必要なものは？**
A: 何もありません！`pip install claude-plus`だけです。

---

## 🎉 さらに簡単な方法（GitHub Actions）

将来的にGitHub Actionsから自動デプロイしたい場合：
1. PyPIでTrusted Publisher設定
2. GitHub Actionsワークフロー作成
3. トークン不要で自動アップロード！

詳細は別途ご相談ください。

---

## 🆘 トラブルシューティング

**2FAアプリが使えない場合**
- セキュリティキー（YubiKey等）も利用可能
- SMS認証は非推奨（セキュリティ上の理由）

**TestPyPIで練習したい場合**
- https://test.pypi.org で同じ手順
- 本番とは別アカウントが必要

**トークンを忘れた場合**
- 再生成が必要（古いトークンは無効化）
- Account settings → API tokensから削除・再作成