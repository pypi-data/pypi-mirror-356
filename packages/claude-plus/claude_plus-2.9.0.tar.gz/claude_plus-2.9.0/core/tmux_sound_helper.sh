#!/bin/bash
# tmux終了時に音声を再生するヘルパースクリプト

# 引数: sound_type (success/warning/error)
SOUND_TYPE=${1:-success}

# 音声ファイルのマッピング
case "$SOUND_TYPE" in
    "success")
        SOUND_FILE="/System/Library/Sounds/Glass.aiff"
        ;;
    "warning")
        SOUND_FILE="/System/Library/Sounds/Ping.aiff"
        ;;
    "error")
        SOUND_FILE="/System/Library/Sounds/Sosumi.aiff"
        ;;
    *)
        SOUND_FILE="/System/Library/Sounds/Glass.aiff"
        ;;
esac

# 音声を再生（バックグラウンドで）
afplay "$SOUND_FILE" &

# 少し待つ（音声再生のため）
sleep 1

exit 0