#!/usr/bin/env python3
"""
Claude++ Pattern Matcher
Advanced pattern recognition system for text processing.
"""

import re
import time
import logging
from typing import Dict, List, Optional, Callable, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


class PatternType(Enum):
    """Types of patterns supported."""
    REGEX = "regex"
    STRING = "string"
    FUNCTION = "function"
    MULTILINE = "multiline"
    CONTEXT = "context"


class MatchResult:
    """Result of a pattern match."""
    
    def __init__(self, 
                 matched: bool = False,
                 response: str = None,
                 confidence: float = 0.0,
                 pattern_id: str = None,
                 match_groups: Tuple = None,
                 context: Dict = None):
        self.matched = matched
        self.response = response
        self.confidence = confidence
        self.pattern_id = pattern_id
        self.match_groups = match_groups or ()
        self.context = context or {}
        self.timestamp = time.time()
        
    def __bool__(self):
        return self.matched


@dataclass
class PatternDefinition:
    """Definition of a pattern to match."""
    pattern_id: str
    pattern_type: PatternType
    pattern: Union[str, Callable]
    response: Union[str, Callable] = None
    priority: int = 50
    enabled: bool = True
    description: str = ""
    tags: List[str] = field(default_factory=list)
    context_requirements: Dict[str, Any] = field(default_factory=dict)
    cooldown_seconds: float = 0.0
    max_matches: int = -1  # -1 = unlimited
    
    # Runtime state
    match_count: int = field(default=0, init=False)
    last_match_time: float = field(default=0.0, init=False)
    

class BasePatternMatcher(ABC):
    """Base class for pattern matchers."""
    
    @abstractmethod
    def match(self, text: str, context: Dict = None) -> MatchResult:
        """Match pattern against text."""
        pass


class RegexPatternMatcher(BasePatternMatcher):
    """Regex-based pattern matcher."""
    
    def __init__(self, definition: PatternDefinition):
        self.definition = definition
        self.regex = re.compile(definition.pattern, re.IGNORECASE | re.MULTILINE)
        
    def match(self, text: str, context: Dict = None) -> MatchResult:
        """Match regex pattern against text."""
        match = self.regex.search(text)
        
        if match:
            response = self._generate_response(match, context)
            confidence = 1.0  # Regex matches are binary
            
            return MatchResult(
                matched=True,
                response=response,
                confidence=confidence,
                pattern_id=self.definition.pattern_id,
                match_groups=match.groups(),
                context=context
            )
            
        return MatchResult(matched=False)
        
    def _generate_response(self, match, context: Dict = None) -> str:
        """Generate response from match."""
        if callable(self.definition.response):
            return self.definition.response(match, context)
        elif isinstance(self.definition.response, str):
            # Support group substitution
            try:
                return self.definition.response.format(*match.groups())
            except (IndexError, AttributeError):
                return self.definition.response
        else:
            return ""  # Default response (Enter key)


class StringPatternMatcher(BasePatternMatcher):
    """Simple string-based pattern matcher."""
    
    def __init__(self, definition: PatternDefinition):
        self.definition = definition
        self.pattern = definition.pattern.lower()
        
    def match(self, text: str, context: Dict = None) -> MatchResult:
        """Match string pattern against text."""
        if self.pattern in text.lower():
            response = self._generate_response(text, context)
            confidence = 0.8  # String matches have high confidence
            
            return MatchResult(
                matched=True,
                response=response,
                confidence=confidence,
                pattern_id=self.definition.pattern_id,
                context=context
            )
            
        return MatchResult(matched=False)
        
    def _generate_response(self, text: str, context: Dict = None) -> str:
        """Generate response from string match."""
        if callable(self.definition.response):
            return self.definition.response(text, context)
        else:
            return self.definition.response or ""


class FunctionPatternMatcher(BasePatternMatcher):
    """Function-based pattern matcher for complex logic."""
    
    def __init__(self, definition: PatternDefinition):
        self.definition = definition
        
    def match(self, text: str, context: Dict = None) -> MatchResult:
        """Match using custom function."""
        if callable(self.definition.pattern):
            try:
                result = self.definition.pattern(text, context)
                
                if isinstance(result, MatchResult):
                    result.pattern_id = self.definition.pattern_id
                    return result
                elif isinstance(result, bool):
                    if result:
                        response = self._generate_response(text, context)
                        return MatchResult(
                            matched=True,
                            response=response,
                            confidence=0.7,
                            pattern_id=self.definition.pattern_id,
                            context=context
                        )
                    else:
                        return MatchResult(matched=False)
                elif isinstance(result, str):
                    return MatchResult(
                        matched=True,
                        response=result,
                        confidence=0.7,
                        pattern_id=self.definition.pattern_id,
                        context=context
                    )
                else:
                    return MatchResult(matched=False)
                    
            except Exception as e:
                logging.getLogger('pattern_matcher').error(
                    f"Function pattern error: {e}"
                )
                return MatchResult(matched=False)
        
        return MatchResult(matched=False)
        
    def _generate_response(self, text: str, context: Dict = None) -> str:
        """Generate response from function match."""
        if callable(self.definition.response):
            return self.definition.response(text, context)
        else:
            return self.definition.response or ""


class AdvancedPatternMatcher:
    """Advanced pattern matching system with multiple pattern types."""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.pattern_matcher')
        self.patterns: List[PatternDefinition] = []
        self.matchers: Dict[str, BasePatternMatcher] = {}
        self.context = {}
        
        # Statistics
        self.stats = {
            'total_attempts': 0,
            'total_matches': 0,
            'matches_by_pattern': {},
            'performance_metrics': {}
        }
        
    def add_pattern(self, pattern_def: PatternDefinition) -> bool:
        """Add a pattern definition."""
        try:
            # Create appropriate matcher
            matcher = self._create_matcher(pattern_def)
            
            # Add to collections
            self.patterns.append(pattern_def)
            self.matchers[pattern_def.pattern_id] = matcher
            
            # Initialize stats
            self.stats['matches_by_pattern'][pattern_def.pattern_id] = 0
            
            self.logger.info(f"Added pattern: {pattern_def.pattern_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add pattern {pattern_def.pattern_id}: {e}")
            return False
            
    def _create_matcher(self, pattern_def: PatternDefinition) -> BasePatternMatcher:
        """Create appropriate matcher for pattern type."""
        if pattern_def.pattern_type == PatternType.REGEX:
            return RegexPatternMatcher(pattern_def)
        elif pattern_def.pattern_type == PatternType.STRING:
            return StringPatternMatcher(pattern_def)
        elif pattern_def.pattern_type == PatternType.FUNCTION:
            return FunctionPatternMatcher(pattern_def)
        else:
            raise ValueError(f"Unsupported pattern type: {pattern_def.pattern_type}")
            
    def remove_pattern(self, pattern_id: str) -> bool:
        """Remove a pattern by ID."""
        # Find and remove pattern
        for i, pattern in enumerate(self.patterns):
            if pattern.pattern_id == pattern_id:
                del self.patterns[i]
                del self.matchers[pattern_id]
                del self.stats['matches_by_pattern'][pattern_id]
                self.logger.info(f"Removed pattern: {pattern_id}")
                return True
                
        self.logger.warning(f"Pattern not found: {pattern_id}")
        return False
        
    def enable_pattern(self, pattern_id: str) -> bool:
        """Enable a pattern."""
        pattern = self._find_pattern(pattern_id)
        if pattern:
            pattern.enabled = True
            self.logger.info(f"Enabled pattern: {pattern_id}")
            return True
        return False
        
    def disable_pattern(self, pattern_id: str) -> bool:
        """Disable a pattern."""
        pattern = self._find_pattern(pattern_id)
        if pattern:
            pattern.enabled = False
            self.logger.info(f"Disabled pattern: {pattern_id}")
            return True
        return False
        
    def _find_pattern(self, pattern_id: str) -> Optional[PatternDefinition]:
        """Find pattern by ID."""
        for pattern in self.patterns:
            if pattern.pattern_id == pattern_id:
                return pattern
        return None
        
    def match(self, text: str, context: Dict = None) -> Optional[MatchResult]:
        """Match text against all patterns and return best match."""
        start_time = time.time()
        self.stats['total_attempts'] += 1
        
        # Merge context
        full_context = {**self.context, **(context or {})}
        
        best_match = None
        best_priority = -1
        
        # Sort patterns by priority (higher first)
        sorted_patterns = sorted(
            self.patterns, 
            key=lambda p: p.priority, 
            reverse=True
        )
        
        for pattern in sorted_patterns:
            if not pattern.enabled:
                continue
                
            # Check context requirements
            if not self._check_context_requirements(pattern, full_context):
                continue
                
            # Check cooldown
            if self._is_on_cooldown(pattern):
                continue
                
            # Check max matches
            if pattern.max_matches > 0 and pattern.match_count >= pattern.max_matches:
                continue
                
            # Attempt match
            matcher = self.matchers[pattern.pattern_id]
            result = matcher.match(text, full_context)
            
            if result.matched:
                # Update pattern statistics
                pattern.match_count += 1
                pattern.last_match_time = time.time()
                self.stats['total_matches'] += 1
                self.stats['matches_by_pattern'][pattern.pattern_id] += 1
                
                # Check if this is the best match so far
                if pattern.priority > best_priority:
                    best_match = result
                    best_priority = pattern.priority
                    
                self.logger.debug(f"Pattern matched: {pattern.pattern_id}")
                
                # If this is a high-priority match, stop searching
                if pattern.priority >= 90:
                    break
                    
        # Record performance
        elapsed = time.time() - start_time
        self.stats['performance_metrics']['last_match_time'] = elapsed
        
        return best_match
        
    def _check_context_requirements(self, 
                                  pattern: PatternDefinition, 
                                  context: Dict) -> bool:
        """Check if context meets pattern requirements."""
        for key, required_value in pattern.context_requirements.items():
            if key not in context or context[key] != required_value:
                return False
        return True
        
    def _is_on_cooldown(self, pattern: PatternDefinition) -> bool:
        """Check if pattern is on cooldown."""
        if pattern.cooldown_seconds <= 0:
            return False
            
        time_since_match = time.time() - pattern.last_match_time
        return time_since_match < pattern.cooldown_seconds
        
    def update_context(self, context: Dict):
        """Update global context."""
        self.context.update(context)
        
    def set_context(self, context: Dict):
        """Set global context."""
        self.context = context.copy()
        
    def get_stats(self) -> Dict:
        """Get matching statistics."""
        return self.stats.copy()
        
    def reset_stats(self):
        """Reset statistics."""
        self.stats = {
            'total_attempts': 0,
            'total_matches': 0,
            'matches_by_pattern': {pid: 0 for pid in self.stats['matches_by_pattern']},
            'performance_metrics': {}
        }
        
        # Reset pattern-specific stats
        for pattern in self.patterns:
            pattern.match_count = 0
            pattern.last_match_time = 0.0
            
    def list_patterns(self) -> List[Dict]:
        """List all patterns with their information."""
        return [
            {
                'id': p.pattern_id,
                'type': p.pattern_type.value,
                'priority': p.priority,
                'enabled': p.enabled,
                'description': p.description,
                'match_count': p.match_count,
                'tags': p.tags
            }
            for p in self.patterns
        ]


# Example usage and factory functions
def create_auto_yes_patterns() -> List[PatternDefinition]:
    """Create Enter-based continuation patterns for actual Claude behavior."""
    patterns = []
    
    # Menu selection patterns (respond with Enter)
    patterns.append(PatternDefinition(
        pattern_id="menu_selection",
        pattern_type=PatternType.REGEX,
        pattern=r"❯.*Yes.*",
        response="",  # Enter key
        priority=85,
        description="Menu-style Yes option selection"
    ))
    
    # Press Enter patterns
    patterns.append(PatternDefinition(
        pattern_id="press_enter",
        pattern_type=PatternType.REGEX,
        pattern=r"Press\s+(?:Enter|any\s+key)\s+to\s+continue",
        response="",  # Enter key
        priority=80,
        description="Press Enter to continue prompts"
    ))
    
    # Japanese continuation patterns
    patterns.append(PatternDefinition(
        pattern_id="japanese_enter",
        pattern_type=PatternType.REGEX,
        pattern=r"続行するにはEnterを押してください|Enterを押して続行",
        response="",  # Enter key
        priority=80,
        description="Japanese Enter continuation prompts"
    ))
    
    # Custom function pattern for Enter-based continuation
    def smart_enter_function(text: str, context: Dict) -> MatchResult:
        # Complex logic for Enter responses with safety
        dangerous_keywords = ['delete', 'remove', 'destroy', 'format', 'drop', 'rm -rf']
        
        if any(keyword in text.lower() for keyword in dangerous_keywords):
            return MatchResult(matched=False)  # Don't auto-respond to dangerous operations
            
        # Look for continuation indicators
        continuation_indicators = [
            'enter.*continue', 'continue.*enter', 'press.*enter',
            '続行', 'continue', '...', 'processing'
        ]
        
        if any(indicator in text.lower() for indicator in continuation_indicators):
            return MatchResult(
                matched=True,
                response="",  # Enter key
                confidence=0.8
            )
            
        return MatchResult(matched=False)
    
    patterns.append(PatternDefinition(
        pattern_id="smart_enter",
        pattern_type=PatternType.FUNCTION,
        pattern=smart_enter_function,
        priority=70,
        description="Smart Enter responses with safety checks"
    ))
    
    return patterns