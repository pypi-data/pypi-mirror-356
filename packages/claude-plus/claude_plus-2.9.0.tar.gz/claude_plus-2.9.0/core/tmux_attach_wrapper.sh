#!/bin/bash
# tmuxセッションアタッチ用ラッパー
# 現在のターミナルでtmuxセッションにアタッチする

SESSION_NAME="${1:-claude_plus}"

# tmuxセッションが存在するか確認
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    # 現在のターミナルでセッションにアタッチ
    exec tmux attach-session -t "$SESSION_NAME"
else
    echo "エラー: tmuxセッション '$SESSION_NAME' が見つかりません"
    exit 1
fi