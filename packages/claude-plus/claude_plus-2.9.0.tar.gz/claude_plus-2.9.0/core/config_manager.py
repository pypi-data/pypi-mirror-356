#!/usr/bin/env python3
"""
Claude++ System Configuration Manager
Interactive configuration management for end users.
"""

import os
import sys
import yaml
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text

console = Console()

CLAUDE_PLUS_DIR = Path.home() / ".claude-plus"
CONFIG_FILE = CLAUDE_PLUS_DIR / "config.yaml"

@click.command()
@click.option('--language', '-l', default='auto',
              type=click.Choice(['auto', 'japanese', 'english']),
              help='Interface language / インターフェース言語')
@click.option('--reset', is_flag=True, help='Reset to default configuration / デフォルト設定にリセット')
def main(language, reset):
    """Claude++ System Configuration Manager / Claude++システム設定管理"""
    
    # Auto-detect language from existing config
    if language == 'auto':
        language = detect_language()
    
    if reset:
        if language == 'japanese':
            if Confirm.ask("設定をデフォルトにリセットしますか？"):
                reset_config()
                console.print("[green]設定をリセットしました[/green]")
                return
        else:
            if Confirm.ask("Reset configuration to defaults?"):
                reset_config()
                console.print("[green]Configuration reset[/green]")
                return
    
    if language == 'japanese':
        config_manager_japanese()
    else:
        config_manager_english()

def detect_language():
    """Detect language from existing configuration"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('system', {}).get('language', 'japanese')
    except:
        pass
    return 'japanese'

def config_manager_japanese():
    """日本語での設定管理"""
    console.print(Panel.fit(
        "[bold blue]Claude++ System 設定管理[/bold blue]\n"
        "現在の設定を確認・変更できます",
        border_style="blue"
    ))
    
    if not CONFIG_FILE.exists():
        console.print("[red]設定ファイルが見つかりません[/red]")
        console.print("まず [yellow]claude-plus-setup[/yellow] を実行してください")
        return
    
    config = load_config()
    
    while True:
        console.print("\n[bold]メニュー:[/bold]")
        console.print("1. 現在の設定を表示")
        console.print("2. 自動化設定")
        console.print("3. 通知設定")
        console.print("4. Git設定")
        console.print("5. 言語・UI設定")
        console.print("6. 詳細設定")
        console.print("7. 設定を保存して終了")
        console.print("8. 保存せずに終了")
        
        choice = Prompt.ask("選択してください", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
        
        if choice == "1":
            show_current_config_japanese(config)
        elif choice == "2":
            config = configure_automation_japanese(config)
        elif choice == "3":
            config = configure_notifications_japanese(config)
        elif choice == "4":
            config = configure_git_japanese(config)
        elif choice == "5":
            config = configure_ui_japanese(config)
        elif choice == "6":
            config = configure_advanced_japanese(config)
        elif choice == "7":
            save_config(config)
            console.print("[green]設定を保存しました[/green]")
            break
        elif choice == "8":
            console.print("[yellow]設定を保存せずに終了します[/yellow]")
            break

def config_manager_english():
    """設定管理ツール（英語版から日本語に統一）"""
    console.print(Panel.fit(
        "[bold blue]Claude++ システム設定管理[/bold blue]\n"
        "現在の設定を表示・変更",
        border_style="blue"
    ))
    
    if not CONFIG_FILE.exists():
        console.print("[red]設定ファイルが見つかりません[/red]")
        console.print("最初に [yellow]claude-plus-setup[/yellow] を実行してください")
        return
    
    config = load_config()
    
    while True:
        console.print("\n[bold]メニュー:[/bold]")
        console.print("1. 現在の設定を表示")
        console.print("2. 自動化設定")
        console.print("3. 通知設定")
        console.print("4. Git設定")
        console.print("5. 言語・UI設定")
        console.print("6. 詳細設定")
        console.print("7. 保存して終了")
        console.print("8. 保存せずに終了")
        
        choice = Prompt.ask("オプションを選択", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
        
        if choice == "1":
            show_current_config_english(config)
        elif choice == "2":
            config = configure_automation_english(config)
        elif choice == "3":
            config = configure_notifications_english(config)
        elif choice == "4":
            config = configure_git_english(config)
        elif choice == "5":
            config = configure_ui_english(config)
        elif choice == "6":
            config = configure_advanced_english(config)
        elif choice == "7":
            save_config(config)
            console.print("[green]Configuration saved[/green]")
            break
        elif choice == "8":
            console.print("[yellow]Exiting without saving[/yellow]")
            break

def show_current_config_japanese(config):
    """現在の設定を日本語で表示"""
    table = Table(title="現在の設定")
    table.add_column("項目", style="cyan")
    table.add_column("値", style="magenta")
    table.add_column("説明", style="green")
    
    # 主要設定を表示
    table.add_row("システム言語", config.get('system', {}).get('language', 'japanese'), "表示言語")
    table.add_row("デバッグモード", str(config.get('system', {}).get('debug', False)), "詳細ログ出力")
    table.add_row("自動Yes", str(config.get('auto_yes', {}).get('enabled', True)), "確認の自動化")
    table.add_row("通知", str(config.get('notifications', {}).get('enabled', True)), "システム通知")
    table.add_row("透明Git", str(config.get('transparent_git', {}).get('enabled', True)), "自動バックアップ")
    table.add_row("自動保護", str(config.get('auto_protection', {}).get('enabled', True)), "作業保護システム")
    
    console.print(table)

def show_current_config_english(config):
    """現在の設定を表示（日本語に統一）"""
    table = Table(title="現在の設定")
    table.add_column("設定項目", style="cyan")
    table.add_column("値", style="magenta")
    table.add_column("説明", style="green")
    
    # Show main settings
    table.add_row("システム言語", config.get('system', {}).get('language', 'japanese'), "表示言語")
    table.add_row("デバッグモード", str(config.get('system', {}).get('debug', False)), "詳細ログ出力")
    table.add_row("自動確認", str(config.get('auto_yes', {}).get('enabled', True)), "確認プロンプト自動化")
    table.add_row("通知", str(config.get('notifications', {}).get('enabled', True)), "システム通知")
    table.add_row("透明Git", str(config.get('transparent_git', {}).get('enabled', True)), "自動バックアップ")
    table.add_row("自動保護", str(config.get('auto_protection', {}).get('enabled', True)), "作業保護システム")
    
    console.print(table)

def configure_automation_japanese(config):
    """自動化設定の変更"""
    console.print("\n[bold blue]自動化設定[/bold blue]")
    
    auto_yes = config.setdefault('auto_yes', {})
    auto_yes['enabled'] = Confirm.ask("自動Yes機能を有効にしますか？", default=auto_yes.get('enabled', True))
    
    if auto_yes['enabled']:
        auto_yes['dangerous_operations'] = Confirm.ask(
            "危険な操作も自動化しますか？（推奨: No）", 
            default=auto_yes.get('dangerous_operations', False)
        )
        
        delay = Prompt.ask(
            "応答遅延（ミリ秒）", 
            default=str(auto_yes.get('delay_ms', 500))
        )
        auto_yes['delay_ms'] = int(delay)
    
    return config

def configure_automation_english(config):
    """Configure automation settings"""
    console.print("\n[bold blue]Automation Settings[/bold blue]")
    
    auto_yes = config.setdefault('auto_yes', {})
    auto_yes['enabled'] = Confirm.ask("Enable Auto Yes feature?", default=auto_yes.get('enabled', True))
    
    if auto_yes['enabled']:
        auto_yes['dangerous_operations'] = Confirm.ask(
            "Also automate dangerous operations? (Recommended: No)", 
            default=auto_yes.get('dangerous_operations', False)
        )
        
        delay = Prompt.ask(
            "Response delay (milliseconds)", 
            default=str(auto_yes.get('delay_ms', 500))
        )
        auto_yes['delay_ms'] = int(delay)
    
    return config

def configure_notifications_japanese(config):
    """通知設定の変更"""
    console.print("\n[bold blue]通知設定[/bold blue]")
    
    notifications = config.setdefault('notifications', {})
    notifications['enabled'] = Confirm.ask("通知を有効にしますか？", default=notifications.get('enabled', True))
    
    if notifications['enabled']:
        notifications['sound'] = Confirm.ask("音声通知を有効にしますか？", default=notifications.get('sound', True))
        notifications['visual'] = Confirm.ask("視覚通知を有効にしますか？", default=notifications.get('visual', True))
        
        verbosity = Prompt.ask(
            "通知の詳細レベル",
            choices=["minimal", "normal", "verbose"],
            default=notifications.get('verbosity', 'normal')
        )
        notifications['verbosity'] = verbosity
    
    return config

def configure_notifications_english(config):
    """Configure notification settings"""
    console.print("\n[bold blue]Notification Settings[/bold blue]")
    
    notifications = config.setdefault('notifications', {})
    notifications['enabled'] = Confirm.ask("Enable notifications?", default=notifications.get('enabled', True))
    
    if notifications['enabled']:
        notifications['sound'] = Confirm.ask("Enable sound notifications?", default=notifications.get('sound', True))
        notifications['visual'] = Confirm.ask("Enable visual notifications?", default=notifications.get('visual', True))
        
        verbosity = Prompt.ask(
            "Notification verbosity level",
            choices=["minimal", "normal", "verbose"],
            default=notifications.get('verbosity', 'normal')
        )
        notifications['verbosity'] = verbosity
    
    return config

def configure_git_japanese(config):
    """Git設定の変更"""
    console.print("\n[bold blue]Git設定[/bold blue]")
    
    git = config.setdefault('git', {})
    git['enabled'] = Confirm.ask("Git統合を有効にしますか？", default=git.get('enabled', True))
    
    if git['enabled']:
        git['auto_branch'] = Confirm.ask("自動ブランチ作成を有効にしますか？", default=git.get('auto_branch', True))
        git['auto_commit'] = Confirm.ask("自動コミットを有効にしますか？（推奨: No）", default=git.get('auto_commit', False))
        git['intelligent_commits'] = Confirm.ask("AI生成コミットメッセージを使用しますか？", default=git.get('intelligent_commits', True))
    
    transparent_git = config.setdefault('transparent_git', {})
    transparent_git['enabled'] = Confirm.ask("透明Git保護を有効にしますか？", default=transparent_git.get('enabled', True))
    
    if transparent_git['enabled']:
        interval = Prompt.ask(
            "自動保存間隔（分）",
            default=str(transparent_git.get('auto_save_interval', 30))
        )
        transparent_git['auto_save_interval'] = int(interval)
    
    return config

def configure_git_english(config):
    """Configure Git settings"""
    console.print("\n[bold blue]Git Settings[/bold blue]")
    
    git = config.setdefault('git', {})
    git['enabled'] = Confirm.ask("Enable Git integration?", default=git.get('enabled', True))
    
    if git['enabled']:
        git['auto_branch'] = Confirm.ask("Enable automatic branch creation?", default=git.get('auto_branch', True))
        git['auto_commit'] = Confirm.ask("Enable auto-commit? (Recommended: No)", default=git.get('auto_commit', False))
        git['intelligent_commits'] = Confirm.ask("Use AI-generated commit messages?", default=git.get('intelligent_commits', True))
    
    transparent_git = config.setdefault('transparent_git', {})
    transparent_git['enabled'] = Confirm.ask("Enable transparent Git protection?", default=transparent_git.get('enabled', True))
    
    if transparent_git['enabled']:
        interval = Prompt.ask(
            "Auto-save interval (minutes)",
            default=str(transparent_git.get('auto_save_interval', 30))
        )
        transparent_git['auto_save_interval'] = int(interval)
    
    return config

def configure_ui_japanese(config):
    """UI設定の変更"""
    console.print("\n[bold blue]言語・UI設定[/bold blue]")
    
    system = config.setdefault('system', {})
    language = Prompt.ask(
        "表示言語",
        choices=["japanese", "english"],
        default=system.get('language', 'japanese')
    )
    system['language'] = language
    
    ui = config.setdefault('ui', {})
    ui['beginner_friendly'] = Confirm.ask("初心者向けモードを有効にしますか？", default=ui.get('beginner_friendly', True))
    ui['hide_technical_terms'] = Confirm.ask("技術用語を簡単な表現にしますか？", default=ui.get('hide_technical_terms', True))
    
    help_frequency = Prompt.ask(
        "ヘルプ表示頻度",
        choices=["rare", "occasional", "frequent"],
        default=ui.get('help_frequency', 'occasional')
    )
    ui['help_frequency'] = help_frequency
    
    return config

def configure_ui_english(config):
    """Configure UI settings"""
    console.print("\n[bold blue]Language & UI Settings[/bold blue]")
    
    system = config.setdefault('system', {})
    language = Prompt.ask(
        "Display language",
        choices=["japanese", "english"],
        default=system.get('language', 'japanese')
    )
    system['language'] = language
    
    ui = config.setdefault('ui', {})
    ui['beginner_friendly'] = Confirm.ask("Enable beginner-friendly mode?", default=ui.get('beginner_friendly', True))
    ui['hide_technical_terms'] = Confirm.ask("Simplify technical terms?", default=ui.get('hide_technical_terms', True))
    
    help_frequency = Prompt.ask(
        "Help display frequency",
        choices=["rare", "occasional", "frequent"],
        default=ui.get('help_frequency', 'occasional')
    )
    ui['help_frequency'] = help_frequency
    
    return config

def configure_advanced_japanese(config):
    """詳細設定の変更"""
    console.print("\n[bold blue]詳細設定[/bold blue]")
    
    system = config.setdefault('system', {})
    system['debug'] = Confirm.ask("デバッグモードを有効にしますか？", default=system.get('debug', False))
    
    auto_protection = config.setdefault('auto_protection', {})
    protection_level = Prompt.ask(
        "保護レベル",
        choices=["LOW", "MEDIUM", "HIGH", "MAXIMUM"],
        default=auto_protection.get('protection_level', 'HIGH')
    )
    auto_protection['protection_level'] = protection_level
    
    backup_freq = Prompt.ask(
        "バックアップ頻度（分）",
        default=str(auto_protection.get('backup_frequency', 20))
    )
    auto_protection['backup_frequency'] = int(backup_freq)
    
    return config

def configure_advanced_english(config):
    """Configure advanced settings"""
    console.print("\n[bold blue]Advanced Settings[/bold blue]")
    
    system = config.setdefault('system', {})
    system['debug'] = Confirm.ask("Enable debug mode?", default=system.get('debug', False))
    
    auto_protection = config.setdefault('auto_protection', {})
    protection_level = Prompt.ask(
        "Protection level",
        choices=["LOW", "MEDIUM", "HIGH", "MAXIMUM"],
        default=auto_protection.get('protection_level', 'HIGH')
    )
    auto_protection['protection_level'] = protection_level
    
    backup_freq = Prompt.ask(
        "Backup frequency (minutes)",
        default=str(auto_protection.get('backup_frequency', 20))
    )
    auto_protection['backup_frequency'] = int(backup_freq)
    
    return config

def load_config():
    """Load configuration from file"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except:
        return {}

def save_config(config):
    """Save configuration to file"""
    CLAUDE_PLUS_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

def reset_config():
    """Reset configuration to defaults"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()

if __name__ == "__main__":
    main()