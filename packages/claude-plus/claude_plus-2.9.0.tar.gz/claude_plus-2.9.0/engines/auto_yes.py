#!/usr/bin/env python3
"""
Claude++ Auto-Yes Engine
Automatically responds to confirmation prompts with intelligent pattern matching.
"""

import re
import time
import logging
from typing import Optional, Dict, List, Pattern
import asyncio


class AutoYesEngine:
    """Engine for automatically responding to confirmation prompts."""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.auto_yes')
        self.config = {}
        self.enabled = True
        self.dangerous_operations = False
        self.patterns = []
        self.response = ""  # Enter key (empty string + newline)
        self.delay_ms = 500
        
        # Dangerous operation patterns (require manual confirmation)
        self.dangerous_patterns = [
            r"delete.*file",
            r"remove.*directory", 
            r"rm\s+-rf",
            r"drop.*database",
            r"format.*disk",
            r"delete.*branch",
            r"force.*push",
            r"rebase.*-i",
            r"reset.*--hard"
        ]
        
        # Compiled regex patterns for performance
        self.compiled_patterns = []
        self.compiled_dangerous = []
        
        # Statistics
        self.stats = {
            'total_prompts': 0,
            'auto_responses': 0,
            'manual_required': 0,
            'dangerous_blocked': 0
        }
        
    async def initialize(self, config: Dict):
        """Initialize the engine with configuration."""
        self.config = config.get('auto_yes', {})
        self.enabled = self.config.get('enabled', True)
        self.dangerous_operations = self.config.get('dangerous_operations', False)
        self.response = self.config.get('response', '')  # Default to Enter
        self.delay_ms = self.config.get('delay_ms', 500)
        
        # Load patterns from config
        config_patterns = self.config.get('patterns', [])
        self.patterns = self._get_default_patterns() + config_patterns
        
        # Compile regex patterns
        self._compile_patterns()
        
        self.logger.info(f"Auto-Yes engine initialized: {len(self.patterns)} patterns")
        self.logger.info(f"Dangerous operations: {'enabled' if self.dangerous_operations else 'disabled'}")
        
    def _get_default_patterns(self) -> List[str]:
        """Get default continuation patterns for actual Claude behavior."""
        return [
            # Menu selection patterns (respond with Enter)
            r"❯\s*1\.\s*Yes",
            r"❯\s*Yes",
            r"❯.*Yes.*",
            
            # Confirmation patterns (respond with Enter for Yes)
            r"Do\s+you\s+want\s+to\s+",
            r"Would\s+you\s+like\s+to\s+",
            r"Continue\?\s*\(Y/n\)",
            r"Continue\?\s*",
            r"Proceed\?\s*",
            r"Overwrite\?\s*",
            r"\(Y/n\)",
            r"\[Y/n\]",
            r"確認してください",
            
            # Press Enter patterns
            r"Press\s+Enter\s+to\s+continue",
            r"Press\s+any\s+key\s+to\s+continue", 
            r"Press\s+Enter.*",
            r"\[Press\s+Enter\]",
            r"Hit\s+Enter\s+to\s+continue",
            
            # Japanese patterns
            r"続行するにはEnterを押してください",
            r"Enterを押して続行",
            r"Enterキーを押してください",
            
            # General continuation patterns  
            r"Enter.*続行",
            r"Enter.*continue",
            r"続行.*Enter",
            r"continue.*Enter",
            
            # Common waiting patterns
            r"Press.*続行",
            r"キーを押して.*続行",
            r"任意のキーを押して",
            
            # Generic continuation indicators
            r"\.\.\.\s*$",  # Dots at end of line (waiting)
            r"待機中\.\.\.",
            r"Processing\.\.\.",
        ]
        
    def _compile_patterns(self):
        """Compile regex patterns for performance."""
        self.compiled_patterns = []
        for pattern in self.patterns:
            try:
                compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                self.compiled_patterns.append(compiled)
            except re.error as e:
                self.logger.warning(f"Invalid regex pattern '{pattern}': {e}")
                
        self.compiled_dangerous = []
        for pattern in self.dangerous_patterns:
            try:
                compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
                self.compiled_dangerous.append(compiled)
            except re.error as e:
                self.logger.warning(f"Invalid dangerous pattern '{pattern}': {e}")
                
    def register_with_daemon(self, daemon):
        """Register this engine with the daemon."""
        daemon.register_engine('auto_yes', self)
        daemon.register_pattern_matcher(self.process_text)
        
    def process_text(self, text: str) -> Optional[str]:
        """Process text and return response if pattern matches."""
        if not self.enabled:
            return None
            
        # Update statistics
        self.stats['total_prompts'] += 1
        
        # Check for dangerous operations first
        if self._is_dangerous_operation(text):
            self.stats['dangerous_blocked'] += 1
            self.logger.warning(f"Dangerous operation detected, requiring manual confirmation: {text.strip()}")
            return None
            
        # Check for confirmation patterns
        if self._matches_confirmation_pattern(text):
            self.stats['auto_responses'] += 1
            self.logger.info(f"Auto-responding to prompt: {text.strip()}")
            
            # Add delay if configured
            if self.delay_ms > 0:
                time.sleep(self.delay_ms / 1000.0)
                
            return self.response
            
        return None
        
    def _is_dangerous_operation(self, text: str) -> bool:
        """Check if text contains dangerous operation patterns."""
        if self.dangerous_operations:
            return False  # User explicitly enabled dangerous operations
            
        text_lower = text.lower()
        
        for pattern in self.compiled_dangerous:
            if pattern.search(text_lower):
                return True
                
        return False
        
    def _matches_confirmation_pattern(self, text: str) -> bool:
        """Check if text matches any confirmation patterns."""
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True
                
        return False
        
    def get_stats(self) -> Dict:
        """Get engine statistics."""
        return self.stats.copy()
        
    def reset_stats(self):
        """Reset statistics counters."""
        self.stats = {
            'total_prompts': 0,
            'auto_responses': 0, 
            'manual_required': 0,
            'dangerous_blocked': 0
        }
        
    def add_pattern(self, pattern: str):
        """Add a new confirmation pattern."""
        try:
            compiled = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            self.patterns.append(pattern)
            self.compiled_patterns.append(compiled)
            self.logger.info(f"Added new pattern: {pattern}")
        except re.error as e:
            self.logger.error(f"Invalid regex pattern '{pattern}': {e}")
            
    def remove_pattern(self, pattern: str):
        """Remove a confirmation pattern."""
        if pattern in self.patterns:
            index = self.patterns.index(pattern)
            self.patterns.pop(index)
            self.compiled_patterns.pop(index)
            self.logger.info(f"Removed pattern: {pattern}")
        else:
            self.logger.warning(f"Pattern not found: {pattern}")
            
    def enable(self):
        """Enable auto-yes functionality."""
        self.enabled = True
        self.logger.info("Auto-Yes engine enabled")
        
    def disable(self):
        """Disable auto-yes functionality."""
        self.enabled = False
        self.logger.info("Auto-Yes engine disabled")
        
    def enable_dangerous_operations(self):
        """Enable automatic responses to dangerous operations."""
        self.dangerous_operations = True
        self.logger.warning("Dangerous operations auto-response ENABLED - Use with caution!")
        
    def disable_dangerous_operations(self):
        """Disable automatic responses to dangerous operations."""
        self.dangerous_operations = False
        self.logger.info("Dangerous operations auto-response disabled")
        
    async def cleanup(self):
        """Clean up resources."""
        self.logger.info(f"Auto-Yes engine cleanup - Final stats: {self.stats}")


# Example usage and testing
async def test_auto_yes():
    """Test the auto-yes engine with sample prompts."""
    engine = AutoYesEngine()
    
    # Initialize with test config
    config = {
        'auto_yes': {
            'enabled': True,
            'dangerous_operations': False,
            'patterns': [],  # Use default patterns
            'response': '',  # Enter key
            'delay_ms': 100
        }
    }
    await engine.initialize(config)
    
    # Test cases - real Claude scenarios
    test_cases = [
        "❯ 1. Yes",
        "❯ Yes",
        "Press Enter to continue",
        "Press any key to continue",
        "続行するにはEnterを押してください",
        "Enter to continue...",
        "Do you want to delete all files?",  # Should be blocked as dangerous
        "Just some random text",
        "Processing...",
        "Waiting for input..."
    ]
    
    print("Testing Auto-Yes Engine:")
    print("-" * 40)
    
    for i, test_text in enumerate(test_cases, 1):
        response = engine.process_text(test_text)
        status = "AUTO-RESPONSE" if response is not None else "NO RESPONSE"
        print(f"{i}. {test_text}")
        if response is not None:
            display_response = "(Enter)" if response == "" else response
            print(f"   -> {status}: {display_response}")
        else:
            print(f"   -> {status}: None")
        print()
        
    print("Final Statistics:")
    print(engine.get_stats())


if __name__ == "__main__":
    # Run test if executed directly
    asyncio.run(test_auto_yes())