#!/usr/bin/env python3
"""
Claude++ Git Pro Engine
Professional Git automation with intelligent branch management, smart commits, and PR preparation.
"""

import asyncio
import subprocess
import logging
import re
import os
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class GitAction(Enum):
    """Types of Git actions."""
    CREATE_BRANCH = "create_branch"
    COMMIT_CHANGES = "commit_changes"
    CREATE_PR = "create_pr"
    RESOLVE_CONFLICT = "resolve_conflict"
    SYNC_REMOTE = "sync_remote"


@dataclass
class GitContext:
    """Git repository context information."""
    repo_path: str
    current_branch: str
    is_dirty: bool
    staged_files: List[str]
    modified_files: List[str]
    untracked_files: List[str]
    commit_count: int
    remote_url: str = None
    conflicts: List[str] = None
    ahead_behind: Tuple[int, int] = (0, 0)  # (ahead, behind)


@dataclass 
class CommitSuggestion:
    """AI-generated commit suggestion."""
    type: str  # feat, fix, docs, refactor, etc.
    scope: str  # component or area
    description: str
    body: str = ""
    breaking: bool = False
    confidence: float = 0.0


class GitProEngine:
    """Professional Git automation engine with AI-powered suggestions."""
    
    def __init__(self):
        self.logger = logging.getLogger('claude-plus.git_pro')
        self.config = {}
        self.enabled = True
        self.auto_commit = False
        self.auto_branch = False
        self.commit_prefix = ""
        self.notifications = None  # Will be set during registration
        
        # Git analysis patterns
        self.file_patterns = {
            'feat': [r'\.py$', r'\.js$', r'\.ts$', r'\.go$', r'\.rs$'],
            'docs': [r'\.md$', r'\.txt$', r'README', r'CHANGELOG'],
            'test': [r'test.*\.py$', r'.*_test\.py$', r'.*\.test\.js$'],
            'chore': [r'\.yaml$', r'\.yml$', r'\.json$', r'\.toml$', r'\.ini$'],
            'build': [r'Makefile', r'CMakeLists\.txt', r'setup\.py', r'package\.json']
        }
        
        # Conventional commit types
        self.commit_types = {
            'feat': 'A new feature',
            'fix': 'A bug fix', 
            'docs': 'Documentation only changes',
            'style': 'Changes that do not affect the meaning of the code',
            'refactor': 'A code change that neither fixes a bug nor adds a feature',
            'perf': 'A code change that improves performance',
            'test': 'Adding missing tests or correcting existing tests',
            'build': 'Changes that affect the build system or external dependencies',
            'ci': 'Changes to our CI configuration files and scripts',
            'chore': 'Other changes that don\'t modify src or test files'
        }
        
        # Statistics
        self.stats = {
            'branches_created': 0,
            'commits_made': 0,
            'prs_created': 0,
            'conflicts_resolved': 0
        }
        
    async def initialize(self, config: Dict):
        """Initialize Git Pro engine with configuration."""
        self.config = config.get('git', {})
        self.enabled = self.config.get('enabled', True)
        self.auto_commit = self.config.get('auto_commit', False)
        self.auto_branch = self.config.get('auto_branch', False) 
        self.commit_prefix = self.config.get('commit_prefix', '')
        
        # Validate git availability
        if not await self._check_git_available():
            self.logger.error("Git not available - Git Pro engine disabled")
            self.enabled = False
            return
            
        self.logger.info(f"Git Pro engine initialized (auto_commit: {self.auto_commit}, auto_branch: {self.auto_branch})")
        
    async def _check_git_available(self) -> bool:
        """Check if git is available in the system."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', '--version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            return result.returncode == 0
        except FileNotFoundError:
            return False
            
    async def get_git_context(self, repo_path: str = ".") -> Optional[GitContext]:
        """Get comprehensive Git repository context."""
        try:
            # Check if it's a git repository
            if not await self._is_git_repo(repo_path):
                return None
                
            # Get current branch
            current_branch = await self._get_current_branch(repo_path)
            
            # Check repository status
            is_dirty = await self._is_repo_dirty(repo_path)
            staged_files = await self._get_staged_files(repo_path)
            modified_files = await self._get_modified_files(repo_path)
            untracked_files = await self._get_untracked_files(repo_path)
            
            # Get commit count
            commit_count = await self._get_commit_count(repo_path)
            
            # Get remote URL
            remote_url = await self._get_remote_url(repo_path)
            
            # Check for conflicts
            conflicts = await self._get_conflicts(repo_path)
            
            # Get ahead/behind status
            ahead_behind = await self._get_ahead_behind_status(repo_path)
            
            return GitContext(
                repo_path=repo_path,
                current_branch=current_branch,
                is_dirty=is_dirty,
                staged_files=staged_files,
                modified_files=modified_files,
                untracked_files=untracked_files,
                commit_count=commit_count,
                remote_url=remote_url,
                conflicts=conflicts,
                ahead_behind=ahead_behind
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get git context: {e}")
            return None
            
    async def _is_git_repo(self, repo_path: str) -> bool:
        """Check if directory is a git repository."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'rev-parse', '--git-dir',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            return result.returncode == 0
        except Exception:
            return False
            
    async def _get_current_branch(self, repo_path: str) -> str:
        """Get current Git branch name."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'branch', '--show-current',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            return stdout.decode().strip()
        except Exception:
            return "unknown"
            
    async def _is_repo_dirty(self, repo_path: str) -> bool:
        """Check if repository has uncommitted changes."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'diff-index', '--quiet', 'HEAD', '--',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            return result.returncode != 0
        except Exception:
            return False
            
    async def _get_staged_files(self, repo_path: str) -> List[str]:
        """Get list of staged files."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'diff', '--cached', '--name-only',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            files = stdout.decode().strip().split('\n')
            return [f for f in files if f]
        except Exception:
            return []
            
    async def _get_modified_files(self, repo_path: str) -> List[str]:
        """Get list of modified files."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'diff', '--name-only',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            files = stdout.decode().strip().split('\n')
            return [f for f in files if f]
        except Exception:
            return []
            
    async def _get_untracked_files(self, repo_path: str) -> List[str]:
        """Get list of untracked files."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'ls-files', '--others', '--exclude-standard',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            files = stdout.decode().strip().split('\n')
            return [f for f in files if f]
        except Exception:
            return []
            
    async def _get_commit_count(self, repo_path: str) -> int:
        """Get total commit count."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'rev-list', '--count', 'HEAD',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            if result.returncode == 0:
                return int(stdout.decode().strip())
        except Exception:
            pass
        return 0
        
    async def _get_remote_url(self, repo_path: str) -> Optional[str]:
        """Get remote origin URL."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'config', '--get', 'remote.origin.url',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            if result.returncode == 0:
                return stdout.decode().strip()
        except Exception:
            pass
        return None
        
    async def _get_conflicts(self, repo_path: str) -> List[str]:
        """Get list of files with merge conflicts."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'diff', '--name-only', '--diff-filter=U',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            files = stdout.decode().strip().split('\n')
            return [f for f in files if f]
        except Exception:
            return []
            
    async def _get_ahead_behind_status(self, repo_path: str) -> Tuple[int, int]:
        """Get ahead/behind commit count compared to upstream."""
        try:
            result = await asyncio.create_subprocess_exec(
                'git', 'rev-list', '--left-right', '--count', 'HEAD...@{upstream}',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            if result.returncode == 0:
                ahead, behind = stdout.decode().strip().split('\t')
                return (int(ahead), int(behind))
        except Exception:
            pass
        return (0, 0)
        
    async def generate_branch_name(self, task_description: str, context: GitContext = None) -> str:
        """Generate intelligent branch name from task description."""
        # Clean and normalize task description
        clean_desc = re.sub(r'[^\w\s-]', '', task_description.lower())
        clean_desc = re.sub(r'\s+', '-', clean_desc.strip())
        clean_desc = clean_desc[:50]  # Limit length
        
        # Determine branch type prefix
        prefix = self._determine_branch_prefix(task_description, context)
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime('%m%d')
        
        branch_name = f"{prefix}/{clean_desc}-{timestamp}"
        
        self.logger.info(f"Generated branch name: {branch_name}")
        return branch_name
        
    def _determine_branch_prefix(self, task_description: str, context: GitContext = None) -> str:
        """Determine appropriate branch prefix based on task."""
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ['fix', 'bug', 'error', 'issue']):
            return 'fix'
        elif any(word in task_lower for word in ['feature', 'add', 'implement', 'create']):
            return 'feat'
        elif any(word in task_lower for word in ['test', 'testing']):
            return 'test'
        elif any(word in task_lower for word in ['docs', 'documentation', 'readme']):
            return 'docs'
        elif any(word in task_lower for word in ['refactor', 'cleanup', 'optimize']):
            return 'refactor'
        else:
            return 'task'
            
    async def create_branch(self, branch_name: str, repo_path: str = ".") -> bool:
        """Create a new Git branch."""
        try:
            # Check if branch already exists
            result = await asyncio.create_subprocess_exec(
                'git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}',
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            if result.returncode == 0:
                self.logger.warning(f"Branch {branch_name} already exists")
                return False
                
            # Create new branch
            result = await asyncio.create_subprocess_exec(
                'git', 'checkout', '-b', branch_name,
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            if result.returncode == 0:
                self.stats['branches_created'] += 1
                self.logger.info(f"Created branch: {branch_name}")
                
                # Send notification
                if self.notifications:
                    await self.notifications.success(
                        "Git: Branch Created", 
                        f"Created new branch: {branch_name}"
                    )
                    
                return True
            else:
                self.logger.error(f"Failed to create branch: {branch_name}")
                
                # Send error notification
                if self.notifications:
                    await self.notifications.error(
                        "Git: Branch Creation Failed",
                        f"Failed to create branch: {branch_name}"
                    )
                    
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating branch {branch_name}: {e}")
            return False
            
    async def generate_commit_message(self, context: GitContext) -> CommitSuggestion:
        """Generate intelligent commit message based on changes."""
        # Analyze changed files
        all_files = context.staged_files + context.modified_files
        
        # Determine commit type
        commit_type = self._analyze_commit_type(all_files)
        
        # Determine scope
        scope = self._analyze_scope(all_files)
        
        # Generate description
        description = self._generate_description(all_files, commit_type)
        
        # Generate detailed body if needed
        body = self._generate_commit_body(context)
        
        return CommitSuggestion(
            type=commit_type,
            scope=scope,
            description=description,
            body=body,
            confidence=0.8
        )
        
    def _analyze_commit_type(self, files: List[str]) -> str:
        """Analyze files to determine commit type."""
        type_scores = {commit_type: 0 for commit_type in self.commit_types.keys()}
        
        for file_path in files:
            for commit_type, patterns in self.file_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, file_path, re.IGNORECASE):
                        type_scores[commit_type] += 1
                        
        # Return type with highest score, default to 'feat'
        return max(type_scores, key=type_scores.get) or 'feat'
        
    def _analyze_scope(self, files: List[str]) -> str:
        """Analyze files to determine commit scope."""
        if not files:
            return ""
            
        # Extract common directory prefix
        dirs = [os.path.dirname(f) for f in files if os.path.dirname(f)]
        if dirs:
            common_dir = os.path.commonpath(dirs) if len(dirs) > 1 else dirs[0]
            if common_dir and common_dir != '.':
                return os.path.basename(common_dir)
                
        # Fallback to first file's directory
        if files:
            first_dir = os.path.dirname(files[0])
            if first_dir and first_dir != '.':
                return os.path.basename(first_dir)
                
        return ""
        
    def _generate_description(self, files: List[str], commit_type: str) -> str:
        """Generate commit description."""
        file_count = len(files)
        
        if file_count == 0:
            return "update configuration"
        elif file_count == 1:
            filename = os.path.basename(files[0])
            return f"update {filename}"
        else:
            if commit_type == 'feat':
                return f"add new functionality ({file_count} files)"
            elif commit_type == 'fix':
                return f"fix issues ({file_count} files)"
            elif commit_type == 'docs':
                return f"update documentation ({file_count} files)"
            else:
                return f"{commit_type} changes ({file_count} files)"
                
    def _generate_commit_body(self, context: GitContext) -> str:
        """Generate detailed commit body."""
        body_parts = []
        
        if context.staged_files:
            body_parts.append(f"Staged files: {', '.join(context.staged_files[:5])}")
            if len(context.staged_files) > 5:
                body_parts.append(f"... and {len(context.staged_files) - 5} more")
                
        if context.modified_files:
            body_parts.append(f"Modified files: {', '.join(context.modified_files[:3])}")
            
        return '\n'.join(body_parts)
        
    async def auto_commit_changes(self, repo_path: str = ".") -> bool:
        """Automatically commit staged changes with intelligent message."""
        if not self.auto_commit:
            return False
            
        try:
            context = await self.get_git_context(repo_path)
            if not context or not context.staged_files:
                return False
                
            # Generate commit message
            suggestion = await self.generate_commit_message(context)
            
            # Format commit message
            scope_part = f"({suggestion.scope})" if suggestion.scope else ""
            commit_msg = f"{suggestion.type}{scope_part}: {suggestion.description}"
            
            if self.commit_prefix:
                commit_msg = f"{self.commit_prefix} {commit_msg}"
                
            # Add body if available
            if suggestion.body:
                commit_msg += f"\n\n{suggestion.body}"
                
            # Execute commit
            result = await asyncio.create_subprocess_exec(
                'git', 'commit', '-m', commit_msg,
                cwd=repo_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.wait()
            
            if result.returncode == 0:
                self.stats['commits_made'] += 1
                self.logger.info(f"Auto-committed with message: {commit_msg}")
                
                # Send notification
                if self.notifications:
                    await self.notifications.success(
                        "Git: Auto-Commit",
                        f"Committed: {suggestion.description}"
                    )
                    
                return True
            else:
                self.logger.error("Failed to auto-commit changes")
                
                # Send error notification
                if self.notifications:
                    await self.notifications.error(
                        "Git: Commit Failed",
                        "Failed to auto-commit changes"
                    )
                    
                return False
                
        except Exception as e:
            self.logger.error(f"Error in auto-commit: {e}")
            return False
            
    def register_with_daemon(self, daemon, notifications=None):
        """Register Git Pro engine with daemon."""
        daemon.register_engine('git_pro', self)
        self.notifications = notifications
        # Git engine doesn't need pattern matching, but may hook into workflow
        
    async def handle_task_start(self, task_description: str, repo_path: str = ".") -> bool:
        """Handle task start - potentially create branch."""
        if not self.enabled or not self.auto_branch:
            return False
            
        try:
            # Get current git context
            context = await self.get_git_context(repo_path)
            if not context:
                self.logger.warning("Not a git repository, skipping branch creation")
                return False
                
            # Check if we're on main/master branch
            if context.current_branch not in ['main', 'master', 'develop']:
                self.logger.info(f"Already on feature branch: {context.current_branch}")
                return False
                
            # Generate and create branch
            branch_name = await self.generate_branch_name(task_description, context)
            success = await self.create_branch(branch_name, repo_path)
            
            if success:
                self.logger.info(f"Created task branch: {branch_name}")
                return True
            else:
                self.logger.warning(f"Failed to create branch: {branch_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in task start handling: {e}")
            return False
            
    async def handle_task_complete(self, repo_path: str = ".") -> bool:
        """Handle task completion - potentially auto-commit and suggest PR."""
        if not self.enabled:
            return False
            
        try:
            context = await self.get_git_context(repo_path)
            if not context:
                return False
                
            # Auto-commit if enabled and there are staged changes
            if self.auto_commit and context.staged_files:
                await self.auto_commit_changes(repo_path)
                
            # Suggest PR if on feature branch
            if context.current_branch not in ['main', 'master', 'develop']:
                self.logger.info(f"Task completed on branch: {context.current_branch}")
                self.logger.info("Consider creating a pull request")
                return True
                
        except Exception as e:
            self.logger.error(f"Error in task completion handling: {e}")
            
        return False
        
    async def cleanup(self):
        """Clean up Git Pro engine."""
        self.logger.info(f"Git Pro engine cleanup - Final stats: {self.stats}")
        
    def get_stats(self) -> Dict:
        """Get Git engine statistics."""
        return self.stats.copy()


# Example usage and testing
async def test_git_pro():
    """Test Git Pro engine functionality."""
    engine = GitProEngine()
    
    config = {
        'git': {
            'enabled': True,
            'auto_commit': False,
            'auto_branch': True,
            'commit_prefix': 'auto:'
        }
    }
    
    await engine.initialize(config)
    
    print("Testing Git Pro Engine:")
    print("-" * 40)
    
    # Test git context
    context = await engine.get_git_context(".")
    if context:
        print(f"Repository: {context.repo_path}")
        print(f"Branch: {context.current_branch}")
        print(f"Dirty: {context.is_dirty}")
        print(f"Staged files: {len(context.staged_files)}")
        print(f"Modified files: {len(context.modified_files)}")
        print()
        
        # Test branch name generation
        task = "Fix auto-yes engine pattern matching"
        branch_name = await engine.generate_branch_name(task, context)
        print(f"Generated branch name: {branch_name}")
        
        # Test commit message generation
        if context.staged_files or context.modified_files:
            suggestion = await engine.generate_commit_message(context)
            print(f"Commit suggestion: {suggestion.type}({suggestion.scope}): {suggestion.description}")
        
    print(f"\nStats: {engine.get_stats()}")


if __name__ == "__main__":
    asyncio.run(test_git_pro())