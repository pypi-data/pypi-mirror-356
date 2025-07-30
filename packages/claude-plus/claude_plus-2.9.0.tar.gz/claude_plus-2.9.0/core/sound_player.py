#!/usr/bin/env python3
"""
音声再生モジュール（統合通知システム対応版）
新しいNotificationSystemと統合されたシンプルな音声再生インターフェース
"""

import logging
from typing import Optional
from .notifications import get_notification_system, NotificationType

logger = logging.getLogger(__name__)


class SoundPlayer:
    """音声再生クラス（統合通知システム使用）"""
    
    # 旧互換性のための音声タイプマッピング
    SOUND_TYPE_MAPPING = {
        'success': NotificationType.SUCCESS,
        'warning': NotificationType.WARNING,
        'error': NotificationType.ERROR,
        'info': NotificationType.INFO,
        'complete': NotificationType.TASK_COMPLETE
    }
    
    @staticmethod
    def play(sound_type: str = 'success', wait: bool = True) -> bool:
        """
        音声を再生する（新統合通知システム使用）
        
        Args:
            sound_type: 音声の種類
            wait: 再生完了まで待つかどうか（現在は無視 - 同期実行）
            
        Returns:
            bool: 再生成功かどうか
        """
        try:
            # 統合通知システムを取得
            notification_system = get_notification_system()
            
            # 音声タイプを通知タイプにマッピング
            notif_type = SoundPlayer.SOUND_TYPE_MAPPING.get(
                sound_type, 
                NotificationType.INFO
            )
            
            # 統合通知システムで音声通知を送信（音声のみ、視覚通知なし）
            success = notification_system.notify(
                notif_type=notif_type,
                title=f"Audio Notification",
                message=f"Playing {sound_type} sound",
                visual=False,  # 音声のみ
                sound=True
            )
            
            if success:
                logger.info(f"Sound played successfully: {sound_type}")
            else:
                logger.warning(f"Failed to play sound: {sound_type}")
            
            return success
            
        except Exception as e:
            logger.error(f"Sound playback error: {e}")
            return False
    
    @staticmethod
    def play_success(wait: bool = True) -> bool:
        """成功音を再生"""
        return SoundPlayer.play('success', wait)
    
    @staticmethod
    def play_warning(wait: bool = True) -> bool:
        """警告音を再生"""
        return SoundPlayer.play('warning', wait)
    
    @staticmethod
    def play_error(wait: bool = True) -> bool:
        """エラー音を再生"""
        return SoundPlayer.play('error', wait)
    
    @staticmethod
    def play_info(wait: bool = True) -> bool:
        """情報音を再生"""
        return SoundPlayer.play('info', wait)
    
    @staticmethod
    def play_complete(wait: bool = True) -> bool:
        """完了音を再生"""
        return SoundPlayer.play('complete', wait)


# 旧互換性のための関数インターフェース
def play_sound(sound_type: str = 'success', wait: bool = True) -> bool:
    """音声再生の関数インターフェース（旧互換性）"""
    return SoundPlayer.play(sound_type, wait)


def play_success_sound(wait: bool = True) -> bool:
    """成功音再生の関数インターフェース（旧互換性）"""
    return SoundPlayer.play_success(wait)


def play_warning_sound(wait: bool = True) -> bool:
    """警告音再生の関数インターフェース（旧互換性）"""
    return SoundPlayer.play_warning(wait)


def play_error_sound(wait: bool = True) -> bool:
    """エラー音再生の関数インターフェース（旧互換性）"""
    return SoundPlayer.play_error(wait)


if __name__ == "__main__":
    # テスト実行
    import time
    
    print("Testing unified sound player...")
    
    test_sounds = ['success', 'warning', 'error', 'info', 'complete']
    
    for sound in test_sounds:
        print(f"Playing {sound} sound...")
        result = SoundPlayer.play(sound)
        print(f"Result: {'Success' if result else 'Failed'}")
        time.sleep(1)
    
    print("Sound player test completed.")