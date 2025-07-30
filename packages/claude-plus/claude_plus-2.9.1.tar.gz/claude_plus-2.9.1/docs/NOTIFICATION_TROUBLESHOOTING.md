# 🔔 Claude++ 通知システム トラブルシューティングガイド

## 問題と解決方法

### 🔇 音が鳴らない

1. **音量確認**
   ```bash
   # macOSの音量を確認
   osascript -e "output volume of (get volume settings)"
   ```

2. **音声ファイル確認**
   ```bash
   python scripts/diagnose_notifications.py
   ```

3. **afplayテスト**
   ```bash
   afplay /System/Library/Sounds/Glass.aiff
   ```

### 📵 通知が表示されない

1. **権限修正**
   ```bash
   python scripts/fix_notification_permission.py
   ```

2. **手動で権限設定**
   - システム環境設定 → 通知とフォーカス
   - Terminal.appの通知を許可
   - Script Editorの通知を許可

3. **おやすみモード確認**
   - メニューバーの通知センターアイコンをクリック
   - おやすみモードがオフであることを確認

### 🔊 音が鳴り続ける

この問題は新しい実装で解決されているはずですが、もし発生した場合：

1. **プロセス確認**
   ```bash
   ps aux | grep afplay
   ```

2. **強制終了**
   ```bash
   killall afplay
   ```

3. **診断実行**
   ```bash
   python scripts/diagnose_notifications.py
   ```

## 開発環境でのテスト方法

### 🚀 claude-plus-dev（推奨）

```bash
# 起動時に自動で通知テストが実行されます
source venv/bin/activate
claude-plus-dev
```

期待される動作：
1. 4つの通知音（情報・成功・警告・エラー）
2. 4つの視覚通知が通知センターに表示
3. 継続音なし

### 🧪 個別テスト

```bash
# クイックテスト
python scripts/test_notifications_quick.py

# 包括的テスト
python scripts/test_pro_notifications.py

# 診断ツール
python scripts/diagnose_notifications.py
```

## プロのエンジニアによる実装詳細

### ✅ ベストプラクティス

1. **osascript引数分離**
   ```python
   # プロの方法：引数を完全に分離
   script = '''
   on run argv
       display notification (item 2 of argv) with title "Claude++" subtitle (item 1 of argv)
   end run
   '''
   subprocess.run(['osascript', '-e', script, title, message])
   ```

2. **シンプルなafplay**
   ```python
   # subprocess.runでタイムアウト管理
   subprocess.run(['afplay', sound_file], timeout=3)
   ```

3. **権限チェック**
   - 初回のみチェックしてキャッシュ
   - フォールバック機能

### ❌ 避けるべき実装

1. 文字列埋め込みでのエスケープ処理
2. 複雑なプロセス管理（Popen + killpg）
3. 過度なログ出力

## よくある質問

### Q: なぜ通知が表示されない？
A: macOS 10.14以降、通知権限が厳格化されました。Terminal.appとScript Editorの両方に権限を付与する必要があります。

### Q: なぜ音が継続する？
A: プロセス管理の問題です。新実装では`subprocess.run`を使用し、タイムアウトで自動終了します。

### Q: terminal-notifierは使わないの？
A: 追加依存を避け、macOS標準機能のみで実装しています。必要に応じて将来追加可能です。

## サポート

問題が解決しない場合は、以下の情報と共に報告してください：

1. `python scripts/diagnose_notifications.py`の出力
2. macOSバージョン
3. エラーメッセージ（あれば）