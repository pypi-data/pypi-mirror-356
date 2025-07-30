#!/usr/bin/env python3
"""
Claude++ Professional Notification System
Clean, robust implementation following best practices.
"""

import subprocess
import logging
import os
import sys
import time
from typing import Dict, Optional, List, Callable
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod
import threading


class NotificationType(Enum):
    """Types of notifications."""
    INFO = "info"
    SUCCESS = "success" 
    WARNING = "warning"
    ERROR = "error"
    AUTO_RESPONSE = "auto_response"
    TASK_COMPLETE = "task_complete"
    MANUAL_REQUIRED = "manual_required"
    CLAUDE_CODE_COMPLETE = "claude_code_complete"
    CLAUDE_CODE_WAITING = "claude_code_waiting"
    CLAUDE_CODE_ERROR = "claude_code_error"


@dataclass
class NotificationEvent:
    """Represents a notification event."""
    type: NotificationType
    title: str
    message: str
    timestamp: float = None
    sound_file: str = None
    visual: bool = True
    sound: bool = True
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class NotificationStrategy(ABC):
    """Abstract base class for notification delivery strategies."""
    
    @abstractmethod
    def can_execute(self) -> bool:
        """Check if this strategy can be executed in current environment."""
        pass
    
    @abstractmethod
    def send_notification(self, event: NotificationEvent) -> bool:
        """Send notification using this strategy."""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of this strategy."""
        pass


class MacOSAudioStrategy(NotificationStrategy):
    """macOS audio notification strategy using afplay."""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.notifications.macos_audio')
        self._afplay_path = None
    
    def can_execute(self) -> bool:
        """Check if afplay is available."""
        if self._afplay_path is None:
            try:
                # Use which to find afplay
                result = subprocess.run(
                    ['which', 'afplay'], 
                    capture_output=True, 
                    text=True,
                    timeout=1
                )
                if result.returncode == 0:
                    self._afplay_path = result.stdout.strip()
                else:
                    self._afplay_path = False
            except Exception:
                self._afplay_path = False
        
        return bool(self._afplay_path)
    
    def send_notification(self, event: NotificationEvent) -> bool:
        """Send audio notification using afplay."""
        if not event.sound or not event.sound_file:
            return False
            
        if not os.path.exists(event.sound_file):
            self.logger.debug(f"Sound file not found: {event.sound_file}")
            return False
        
        try:
            # Simple subprocess.run - no complex process management needed
            result = subprocess.run(
                [self._afplay_path, event.sound_file],
                capture_output=True,
                timeout=3  # Reasonable timeout for sound playback
            )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            # If sound takes too long, kill it
            self.logger.debug("Audio playback timed out")
            return False
        except Exception as e:
            self.logger.debug(f"Audio error: {e}")
            return False
    
    def get_strategy_name(self) -> str:
        return "macOS Audio"


class MacOSVisualStrategy(NotificationStrategy):
    """macOS visual notification strategy using osascript."""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.notifications.macos_visual')
        self._osascript_path = None
        self._permission_checked = False
        self._has_permission = None
    
    def can_execute(self) -> bool:
        """Check if osascript is available and we have permission."""
        # Check osascript availability
        if self._osascript_path is None:
            try:
                result = subprocess.run(
                    ['which', 'osascript'], 
                    capture_output=True, 
                    text=True,
                    timeout=1
                )
                if result.returncode == 0:
                    self._osascript_path = result.stdout.strip()
                else:
                    self._osascript_path = False
            except Exception:
                self._osascript_path = False
        
        if not self._osascript_path:
            return False
        
        # Check notification permission (only once)
        if not self._permission_checked:
            self._check_notification_permission()
            self._permission_checked = True
        
        return self._has_permission
    
    def _check_notification_permission(self):
        """Check if we have permission to send notifications."""
        try:
            # Test with a silent notification (no visible test notification)
            # Use a simple AppleScript that just checks if notifications are possible
            test_script = '''
            try
                display notification "" with title ""
                return true
            on error
                return false
            end try
            '''
            result = subprocess.run(
                [self._osascript_path, '-e', test_script],
                capture_output=True,
                stderr=subprocess.DEVNULL,  # Suppress permission check errors
                timeout=2
            )
            # Always assume permission for now - let real notifications fail gracefully
            self._has_permission = True
        except Exception:
            # Assume permission and let real notifications handle errors
            self._has_permission = True
    
    def send_notification(self, event: NotificationEvent) -> bool:
        """Send visual notification using macOS notification center."""
        if not event.visual:
            return False
            
        try:
            # Professional approach: Use AppleScript with proper argument passing
            # This completely avoids escaping issues
            script = '''
            on run argv
                display notification (item 2 of argv) with title "Claude++" subtitle (item 1 of argv)
            end run
            '''
            
            # Pass title and message as separate arguments - no escaping needed!
            result = subprocess.run(
                [self._osascript_path, '-e', script, event.title, event.message],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                if result.stderr:
                    self.logger.debug(f"osascript error: {result.stderr}")
                
                # Fallback: Try with System Events using argument passing (safe)
                fallback_script = '''
                on run argv
                    tell application "System Events"
                        display notification (item 2 of argv) with title "Claude++" subtitle (item 1 of argv)
                    end tell
                end run
                '''
                
                subprocess.run(
                    [self._osascript_path, '-e', fallback_script, event.title, event.message],
                    capture_output=True,
                    timeout=2
                )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.logger.debug("Visual notification timed out")
            return False
        except Exception as e:
            self.logger.debug(f"Visual notification error: {e}")
            return False
    
    def get_strategy_name(self) -> str:
        return "macOS Visual"


class ConsoleStrategy(NotificationStrategy):
    """Console notification strategy (always available fallback)."""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.notifications.console')
    
    def can_execute(self) -> bool:
        """Console is always available."""
        return True
    
    def send_notification(self, event: NotificationEvent) -> bool:
        """Send notification to console with color coding."""
        try:
            # Color mapping
            colors = {
                NotificationType.INFO: '\033[94m',      # Blue
                NotificationType.SUCCESS: '\033[92m',   # Green  
                NotificationType.WARNING: '\033[93m',   # Yellow
                NotificationType.ERROR: '\033[91m',     # Red
                NotificationType.AUTO_RESPONSE: '\033[96m',  # Cyan
                NotificationType.TASK_COMPLETE: '\033[95m',  # Magenta
                NotificationType.MANUAL_REQUIRED: '\033[93m', # Yellow
                NotificationType.CLAUDE_CODE_COMPLETE: '\033[92m',  # Green
                NotificationType.CLAUDE_CODE_WAITING: '\033[93m',   # Yellow
                NotificationType.CLAUDE_CODE_ERROR: '\033[91m'      # Red
            }
            
            reset_color = '\033[0m'
            color = colors.get(event.type, '')
            
            timestamp = time.strftime('%H:%M:%S', time.localtime(event.timestamp))
            
            # プロのターミナルUI: 横一列表示（確実版）
            # タイトルとメッセージを同じ行に表示して改行問題を解決
            if event.message and event.message != event.title:
                display_text = f"🔔 [{timestamp}] {event.title} - {event.message}"
            else:
                display_text = f"🔔 [{timestamp}] {event.title}"
            
            # Phase 1改善（修正版): 通知のみ直接出力、他ログは抑制
            # 通知は重要なため、ログレベル制限を回避して直接表示
            # ファイルログは従来通り logger を使用
            print(f"{color}{display_text}{reset_color}", file=sys.stderr, flush=True)
            self.logger.info(f"Console notification displayed: {display_text}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Console output error: {e}")
            return False
    
    def get_strategy_name(self) -> str:
        return "Console"


class NotificationSystem:
    """Professional notification system with clean implementation."""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.notifications')
        self.enabled = True
        self.sound_enabled = True
        self.visual_enabled = True
        self.console_enabled = True
        
        # Sound file mappings (macOS system sounds)
        self.sound_files = {
            NotificationType.INFO: "/System/Library/Sounds/Tink.aiff",
            NotificationType.SUCCESS: "/System/Library/Sounds/Glass.aiff", 
            NotificationType.WARNING: "/System/Library/Sounds/Ping.aiff",
            NotificationType.ERROR: "/System/Library/Sounds/Sosumi.aiff",
            NotificationType.AUTO_RESPONSE: "/System/Library/Sounds/Pop.aiff",
            NotificationType.TASK_COMPLETE: "/System/Library/Sounds/Purr.aiff",
            NotificationType.MANUAL_REQUIRED: "/System/Library/Sounds/Basso.aiff",
            NotificationType.CLAUDE_CODE_COMPLETE: "/System/Library/Sounds/Hero.aiff",
            NotificationType.CLAUDE_CODE_WAITING: "/System/Library/Sounds/Blow.aiff",
            NotificationType.CLAUDE_CODE_ERROR: "/System/Library/Sounds/Funk.aiff"
        }
        
        # Strategies
        self.strategies: List[NotificationStrategy] = []
        
        # Simple deduplication (extended to prevent silence detection duplicates)
        self._recent_notifications = {}
        self._dedup_window = 5  # seconds (extended from 2 to 5 to prevent duplicate notifications)
        
        # Initialize strategies
        self._init_strategies()
    
    def _init_strategies(self):
        """Initialize notification strategies."""
        # Order matters - try visual first, then audio, then console
        strategies = [
            MacOSVisualStrategy(),
            MacOSAudioStrategy(),
            ConsoleStrategy(),
        ]
        
        for strategy in strategies:
            if strategy.can_execute():
                self.strategies.append(strategy)
                self.logger.debug(f"Enabled strategy: {strategy.get_strategy_name()}")
        
        if not self.strategies:
            # This should never happen since ConsoleStrategy is always available
            self.logger.error("No notification strategies available!")
    
    def initialize(self, config: Dict):
        """Initialize with configuration."""
        notif_config = config.get('notifications', {})
        self.enabled = notif_config.get('enabled', True)
        self.sound_enabled = notif_config.get('sound', True)
        self.visual_enabled = notif_config.get('visual', True)
        self.console_enabled = notif_config.get('console', True)
        
        # Custom sound files if provided
        custom_sounds = notif_config.get('sound_files', {})
        if isinstance(custom_sounds, dict):
            for key, sound_file in custom_sounds.items():
                try:
                    notif_type = NotificationType(key)
                    if os.path.exists(sound_file):
                        self.sound_files[notif_type] = sound_file
                except ValueError:
                    pass
    
    def notify(self, 
               notif_type: NotificationType,
               title: str, 
               message: str = None,
               sound_file: str = None,
               visual: bool = None,
               sound: bool = None) -> bool:
        """Send a notification."""
        
        if not self.enabled:
            return False
        
        # Use message as title if no message provided
        if message is None:
            message = title
        
        # Check for duplicate
        dedup_key = f"{notif_type.value}:{title}"
        current_time = time.time()
        
        if dedup_key in self._recent_notifications:
            if current_time - self._recent_notifications[dedup_key] < self._dedup_window:
                return True  # Silently ignore duplicate
        
        self._recent_notifications[dedup_key] = current_time
        
        # Clean old entries
        self._recent_notifications = {
            k: v for k, v in self._recent_notifications.items()
            if current_time - v < self._dedup_window * 2
        }
        
        # Create event
        event = NotificationEvent(
            type=notif_type,
            title=title,
            message=message,
            sound_file=sound_file or self.sound_files.get(notif_type),
            visual=visual if visual is not None else self.visual_enabled,
            sound=sound if sound is not None else self.sound_enabled
        )
        
        # Send through strategies
        success = False
        for strategy in self.strategies:
            # Skip console if disabled
            if isinstance(strategy, ConsoleStrategy) and not self.console_enabled:
                continue
                
            try:
                if strategy.send_notification(event):
                    success = True
                    # Don't break - let multiple strategies handle it
            except Exception as e:
                self.logger.debug(f"Strategy {strategy.get_strategy_name()} error: {e}")
        
        return success
    
    # Convenience methods
    def info(self, title: str, message: str = None) -> bool:
        """Send info notification."""
        return self.notify(NotificationType.INFO, title, message)
    
    def success(self, title: str, message: str = None) -> bool:
        """Send success notification."""
        return self.notify(NotificationType.SUCCESS, title, message)
    
    def warning(self, title: str, message: str = None) -> bool:
        """Send warning notification."""
        return self.notify(NotificationType.WARNING, title, message)
    
    def error(self, title: str, message: str = None) -> bool:
        """Send error notification."""
        return self.notify(NotificationType.ERROR, title, message)
    
    def claude_code_complete(self, title: str = "Claude Code 作業完了", 
                           message: str = "タスクが正常に完了しました") -> bool:
        """Send Claude Code completion notification."""
        return self.notify(NotificationType.CLAUDE_CODE_COMPLETE, title, message)
    
    def claude_code_waiting(self, title: str = "Claude Code 確認待ち", 
                          message: str = "ユーザーの確認が必要です") -> bool:
        """Send Claude Code waiting notification."""
        return self.notify(NotificationType.CLAUDE_CODE_WAITING, title, message)
    
    def claude_code_error(self, title: str = "Claude Code エラー", 
                        message: str = "エラーが発生しました") -> bool:
        """Send Claude Code error notification."""
        return self.notify(NotificationType.CLAUDE_CODE_ERROR, title, message)


# Global instance
_notification_system = None


def get_notification_system() -> NotificationSystem:
    """Get global notification system instance."""
    global _notification_system
    if _notification_system is None:
        _notification_system = NotificationSystem()
    return _notification_system


# Convenience functions
def notify(notif_type: NotificationType, title: str, message: str = None) -> bool:
    """Send a notification."""
    return get_notification_system().notify(notif_type, title, message)


def info(title: str, message: str = None) -> bool:
    """Send info notification."""
    return get_notification_system().info(title, message)


def success(title: str, message: str = None) -> bool:
    """Send success notification."""
    return get_notification_system().success(title, message)


def warning(title: str, message: str = None) -> bool:
    """Send warning notification."""
    return get_notification_system().warning(title, message)


def error(title: str, message: str = None) -> bool:
    """Send error notification."""
    return get_notification_system().error(title, message)


def claude_code_complete(title: str = "Claude Code 作業完了", 
                       message: str = "タスクが正常に完了しました") -> bool:
    """Send Claude Code completion notification."""
    return get_notification_system().claude_code_complete(title, message)


def claude_code_waiting(title: str = "Claude Code 確認待ち", 
                      message: str = "ユーザーの確認が必要です") -> bool:
    """Send Claude Code waiting notification."""
    return get_notification_system().claude_code_waiting(title, message)


def claude_code_error(title: str = "Claude Code エラー", 
                    message: str = "エラーが発生しました") -> bool:
    """Send Claude Code error notification."""
    return get_notification_system().claude_code_error(title, message)


if __name__ == '__main__':
    # Simple test
    import sys
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Testing Professional Notification System...")
    
    system = get_notification_system()
    system.initialize({})
    
    # Test all notification types
    tests = [
        (NotificationType.INFO, "テスト情報", "これは情報メッセージです"),
        (NotificationType.SUCCESS, "テスト成功", "操作が正常に完了しました"),
        (NotificationType.WARNING, "テスト警告", "これは警告です"),
        (NotificationType.ERROR, "テストエラー", "エラーが発生しました"),
        (NotificationType.CLAUDE_CODE_COMPLETE, "Claude Code 完了", "タスクが完了しました"),
        (NotificationType.CLAUDE_CODE_WAITING, "入力待ち", "入力をお待ちしています"),
        (NotificationType.CLAUDE_CODE_ERROR, "Claude Code エラー", "問題が発生しました"),
    ]
    
    for notif_type, title, message in tests:
        print(f"\nTesting {notif_type.value}...")
        success = system.notify(notif_type, title, message)
        print(f"Result: {'✓' if success else '✗'}")
        time.sleep(1)
    
    print("\n✅ Test completed")