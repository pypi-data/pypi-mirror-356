# 🔧 開発環境での通知システム確認方法

## 🚀 クイックスタート（1分で確認）

### 1. 基本動作確認
```bash
# 開発環境で起動
python scripts/test_notification_complete.py
```

### 2. 個別通知テスト
```bash
# Pythonインタラクティブモードで確認
python -c "
from core.notifications import info, success, warning, error
info('テスト', 'インフォメーション通知')
success('成功', '成功通知のテスト')
warning('警告', '警告通知のテスト')  
error('エラー', 'エラー通知のテスト')
"
```

## 🎯 段階別確認手順

### Phase 1: 基本機能確認（30秒）

```bash
# 1. 通知システム基本テスト
python -c "
from core.notifications import get_notification_system
system = get_notification_system()
system.initialize({})
print('✅ 通知システム初期化完了')
result = system.info('テスト通知', 'システムが正常に動作しています')
print(f'✅ 通知送信結果: {result}')
"
```

### Phase 2: 音声通知確認（30秒）

```bash
# 2. 音声通知テスト（音量を調整してください）
python -c "
from core.sound_player import SoundPlayer
print('🔊 成功音テスト...')
SoundPlayer.play_success()
print('🔊 警告音テスト...')  
SoundPlayer.play_warning()
print('🔊 エラー音テスト...')
SoundPlayer.play_error()
print('✅ 音声通知テスト完了')
"
```

### Phase 3: Claude Code統合確認（1分）

```bash
# 3. 実際のClaude++開発環境で起動
claude-plus-dev
```

**期待される動作**:
- 🔔 起動時に「Claude++ System Ready」通知
- 🎵 各種音声通知が正常に再生
- 📱 macOS通知センターに表示（macOSの場合）

## 🔍 詳細確認方法

### 統計・ログ確認

```bash
# 通知システムの詳細統計確認
python -c "
from core.notifications import get_notification_system
import json

system = get_notification_system()
system.initialize({})

# テスト通知送信
system.info('統計テスト', 'テスト通知1')
system.success('統計テスト', 'テスト通知2')
system.warning('統計テスト', 'テスト通知3')

# 統計表示
stats = system.get_stats()
print('📊 通知システム統計:')
print(json.dumps(stats, indent=2, ensure_ascii=False))
"
```

### パフォーマンステスト

```bash
# パフォーマンス確認（高速通知テスト）
python -c "
import time
from core.notifications import get_notification_system

system = get_notification_system()
system.initialize({'notifications': {'sound': False, 'visual': False}})

print('⚡ パフォーマンステスト開始...')
start_time = time.time()

for i in range(100):
    system.info(f'テスト{i}', f'パフォーマンステストメッセージ{i}')

duration = time.time() - start_time
throughput = 100 / duration

print(f'✅ 100通知を{duration:.3f}秒で処理')
print(f'📈 スループット: {throughput:.0f}通知/秒')
"
```

## 🧪 個別コンポーネントテスト

### 1. daemon.py統合テスト

```bash
# daemon.pyの通知機能確認
python -c "
from core.daemon import ClaudePlusDaemon

daemon = ClaudePlusDaemon()
print('🔧 daemon通知システム確認...')

# 通知メソッドテスト
daemon._play_notification_sound('success')
daemon._trigger_completion_notification()
daemon._trigger_waiting_notification('テストパターン')
daemon._trigger_error_notification('テストエラー')

print('✅ daemon通知統合完了')
"
```

### 2. claude_integration.py統合テスト

```bash
# claude_integration.pyの通知機能確認
python -c "
from core.claude_integration import ClaudeIntegration
from unittest.mock import patch

# モックで安全にテスト
with patch('core.claude_integration.ScreenController'):
    with patch('core.claude_integration.ControlPanel'):
        with patch('core.claude_integration.InputRouter'):
            integration = ClaudeIntegration({})
            print('🔧 claude_integration通知システム確認...')
            
            integration._initialize_notification_system()
            print('✅ claude_integration通知統合完了')
"
```

### 3. 重複排除テスト

```bash
# 重複排除機能確認
python -c "
from core.notifications import get_notification_system
import time

system = get_notification_system()
system.initialize({})

print('🔄 重複排除テスト開始...')

# 同じ通知を連続送信
for i in range(3):
    result = system.info('重複テスト', '同じメッセージ')
    print(f'  送信{i+1}: {result}')

print(f'📊 履歴件数: {len(system.history)}')
print('✅ 重複排除テスト完了')
"
```

## ⚙️ 設定カスタマイズテスト

### カスタム設定での動作確認

```bash
# カスタム設定で動作確認
python -c "
from core.notifications import NotificationSystem

# カスタム設定
config = {
    'notifications': {
        'enabled': True,
        'sound': True,
        'visual': False,  # 視覚通知オフ
        'console': True,
        'sound_files': {
            'success': '/System/Library/Sounds/Glass.aiff'
        }
    }
}

system = NotificationSystem()
system.initialize(config)

print('⚙️ カスタム設定テスト...')
system.success('カスタム設定', '音声のみ通知テスト')
print('✅ カスタム設定確認完了')
"
```

## 🚨 エラーケーステスト

### 異常系動作確認

```bash
# エラーハンドリング確認
python -c "
from core.notifications import NotificationSystem, NotificationType

system = NotificationSystem()
system.initialize({})

print('🚨 エラーケーステスト開始...')

# 1. 長い文字列テスト
long_title = 'A' * 500
long_message = 'B' * 1000
result = system.notify(NotificationType.INFO, long_title, long_message)
print(f'  長文字列テスト: {result}')

# 2. 無効な設定テスト
error_system = NotificationSystem()
error_system.initialize({'notifications': {'enabled': False}})
result = error_system.info('無効テスト', 'これは表示されない')
print(f'  無効化テスト: {result} (Falseが正常)')

# 3. None値テスト
try:
    system.notify(None, None, None)
    print('  None値テスト: 例外未発生（適切に処理）')
except Exception as e:
    print(f'  None値テスト: 例外適切処理 ({type(e).__name__})')

print('✅ エラーケーステスト完了')
"
```

## 📱 環境別確認

### macOS環境

```bash
# macOS特有機能確認
python -c "
from core.notifications import get_notification_system
import subprocess

system = get_notification_system()
system.initialize({})

print('🍎 macOS環境確認...')

# osascript利用可能性確認
try:
    result = subprocess.run(['which', 'osascript'], capture_output=True)
    osascript_available = result.returncode == 0
    print(f'  osascript: {\"✅ 利用可能\" if osascript_available else \"❌ 利用不可\"}')
except:
    print('  osascript: ❌ 確認失敗')

# afplay利用可能性確認  
try:
    result = subprocess.run(['which', 'afplay'], capture_output=True)
    afplay_available = result.returncode == 0
    print(f'  afplay: {\"✅ 利用可能\" if afplay_available else \"❌ 利用不可\"}')
except:
    print('  afplay: ❌ 確認失敗')

# 通知センターテスト
system.info('macOS通知', 'macOS通知センターテスト')
print('✅ macOS環境確認完了')
"
```

## 🎛️ デバッグモード

### 詳細ログ出力での確認

```bash
# デバッグログ付きテスト
python -c "
import logging
from core.notifications import get_notification_system

# ログレベル設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

system = get_notification_system()
system.initialize({})

print('🔍 デバッグモードテスト開始...')
system.info('デバッグ', 'デバッグログ確認用通知')
print('✅ デバッグモードテスト完了')
"
```

## 📊 成功判定基準

### ✅ 正常動作の確認ポイント

1. **通知送信**: すべてのテストでTrueが返される
2. **音声再生**: エラーなく音声が再生される  
3. **視覚通知**: macOS通知センターに表示される（macOSの場合）
4. **コンソール出力**: カラー付きで適切に表示される
5. **パフォーマンス**: 1000通知/秒以上の処理速度
6. **エラーハンドリング**: 異常入力でも例外が発生しない

### ❌ 問題がある場合の対処

```bash
# 問題解決用の診断スクリプト
python -c "
print('🔧 通知システム診断開始...')

# 1. インポート確認
try:
    from core.notifications import NotificationSystem
    print('✅ core.notifications インポート成功')
except ImportError as e:
    print(f'❌ core.notifications インポート失敗: {e}')

# 2. システム依存確認
import subprocess
import os

commands = ['osascript', 'afplay', 'which']
for cmd in commands:
    try:
        result = subprocess.run(['which', cmd], capture_output=True)
        status = '✅ 利用可能' if result.returncode == 0 else '❌ 利用不可'
        print(f'  {cmd}: {status}')
    except:
        print(f'  {cmd}: ❌ 確認失敗')

# 3. 権限確認
print(f'  通知権限: ユーザーが macOS システム環境設定で確認してください')

print('🔧 診断完了')
"
```

## 🎯 実運用確認

### 実際のClaude++セッションでの確認

```bash
# 1. 開発環境起動
claude-plus-dev

# 2. 期待される通知
# - 起動時: "Claude++ System Ready" 
# - Claude Code接続時: 接続成功通知
# - 作業完了時: 完了通知
# - エラー時: エラー通知

# 3. 音声確認
# - 各段階で適切な音声が再生される
# - 音量が適切（うるさすぎない）
# - 音声ファイルが見つからないエラーがない
```

これらの確認手順で、通知システムが正常に動作していることを確認できます。問題がある場合は、診断スクリプトの結果をお知らせください。