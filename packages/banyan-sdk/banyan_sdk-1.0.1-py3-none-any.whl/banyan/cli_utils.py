"""
Banyan CLI Utilities

Helper functions for CLI operations including file handling, prompt diffing,
configuration management, and project scaffolding.

Production-ready features:
- Atomic file operations with integrity checking
- File locking to prevent race conditions  
- Delta compression for efficient storage
- Comprehensive error handling and recovery
"""

import os
import json
import yaml
import hashlib
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
import logging
from datetime import datetime
import re
import requests

from .integrity import (
    ContentHasher, 
    AtomicFileOperations, 
    IntegrityError, 
    get_integrity_manager
)
from .storage import StorageManager

logger = logging.getLogger(__name__)

@dataclass
class PromptFile:
    """Represents a simple prompt file with production-ready integrity features"""
    name: str
    content: str
    file_path: Optional[str] = None
    description: str = ""  # Description for the prompt
    _content_hash: Optional[str] = None  # Cached hash
    
    @classmethod
    def from_file(cls, file_path: Path) -> 'PromptFile':
        """Create PromptFile from a simple text/yaml file with integrity verification"""
        name = file_path.stem  # filename without extension
        try:
            content, content_hash = AtomicFileOperations.read_text_verified(file_path)
            content = content.strip()
            instance = cls(name=name, content=content, file_path=str(file_path))
            instance._content_hash = content_hash
            return instance
        except IntegrityError as e:
            logger.error(f"Integrity error reading {file_path}: {e}")
            # Fall back to regular read for backwards compatibility
            content = file_path.read_text().strip()
            return cls(name=name, content=content, file_path=str(file_path))
    
    def save_to_file(self, prompts_dir: Path) -> bool:
        """Save prompt to a simple text file with atomic operations and locking"""
        try:
            file_path = prompts_dir / f"{self.name}.txt"
            integrity_manager = get_integrity_manager(prompts_dir.parent)
            
            # Use resource locking to prevent concurrent modifications
            with integrity_manager.lock_resource(f"prompt_{self.name}"):
                self._content_hash = AtomicFileOperations.write_text_atomic(file_path, self.content)
                logger.debug(f"Atomically saved prompt {self.name} with hash {self._content_hash[:8]}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to save prompt file {self.name}: {e}")
            return False

    def content_hash(self) -> str:
        """Generate full SHA-256 hash for prompt content"""
        if self._content_hash is None:
            self._content_hash = ContentHasher.hash_content(self.content)
        return self._content_hash
    
    def short_hash(self, length: int = 12) -> str:
        """Generate shortened hash for display purposes"""
        return self.content_hash()[:length]
    
    def verify_integrity(self, expected_hash: Optional[str] = None) -> bool:
        """Verify content integrity against expected hash"""
        current_hash = self.content_hash()
        if expected_hash:
            return current_hash == expected_hash
        return True  # No expected hash provided, assume valid

@dataclass 
class StagedFile:
    """Represents a staged file ready for commit with full integrity"""
    name: str
    content: str
    branch: str = "main"
    operation: str = "modified"  # added, modified, deleted
    hash: str = ""  # Full SHA-256 hash
    short_hash: str = ""  # Short hash for display
    staged_at: str = ""
    
    def __post_init__(self):
        if not self.hash:
            self.hash = ContentHasher.hash_content(self.content)
        if not self.short_hash:
            self.short_hash = self.hash[:8]
        if not self.staged_at:
            self.staged_at = datetime.now().isoformat()
    
    def verify_integrity(self) -> bool:
        """Verify content integrity"""
        return ContentHasher.verify_content(self.content, self.hash)

@dataclass
class IndexEntry:
    """Represents an entry in the Git-like index with full hash integrity"""
    name: str
    content_hash: str  # Full SHA-256 hash
    file_mode: str = "100644"  # Regular file
    last_modified: str = ""
    content_size: int = 0  # Size in bytes for verification
    
    def __post_init__(self):
        if not self.last_modified:
            self.last_modified = datetime.now().isoformat()
    
    def short_hash(self, length: int = 12) -> str:
        """Get shortened hash for display"""
        return self.content_hash[:length]

@dataclass
class ConflictInfo:
    """Information about a merge conflict with full integrity"""
    name: str
    local_content: str
    remote_content: str
    base_content: Optional[str] = None  # Common ancestor if available
    local_hash: str = ""  # Full SHA-256 hash
    remote_hash: str = ""  # Full SHA-256 hash
    base_hash: str = ""   # Full SHA-256 hash for base
    
    def __post_init__(self):
        if not self.local_hash:
            self.local_hash = ContentHasher.hash_content(self.local_content)
        if not self.remote_hash:
            self.remote_hash = ContentHasher.hash_content(self.remote_content)
        if self.base_content and not self.base_hash:
            self.base_hash = ContentHasher.hash_content(self.base_content)
    
    def generate_conflict_markers(self) -> str:
        """Generate content with Git-style conflict markers"""
        lines = []
        lines.append("<<<<<<< LOCAL")
        lines.append(self.local_content)
        lines.append("=======")
        lines.append(self.remote_content)
        lines.append(">>>>>>> REMOTE")
        return "\n".join(lines)
    
    def verify_integrity(self) -> bool:
        """Verify that content matches stored hashes"""
        local_ok = ContentHasher.verify_content(self.local_content, self.local_hash)
        remote_ok = ContentHasher.verify_content(self.remote_content, self.remote_hash)
        
        if self.base_content and self.base_hash:
            base_ok = ContentHasher.verify_content(self.base_content, self.base_hash)
            return local_ok and remote_ok and base_ok
        
        return local_ok and remote_ok

@dataclass
class LocalVersion:
    """Represents a local version of a prompt with full integrity and delta support"""
    name: str
    content: str
    branch: str = "main"
    version: str = "1.0"
    message: str = ""
    metadata: Optional[Dict[str, Any]] = None
    hash: str = ""  # Full SHA-256 hash for commit identity
    content_hash: str = ""  # Full SHA-256 hash for content integrity
    pushed: bool = False
    parent_hash: Optional[str] = None  # For delta compression
    merge_parents: Optional[List[str]] = None  # For merge commits (multiple parents)
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.merge_parents is None:
            self.merge_parents = []
        
        # Generate content hash first
        if not self.content_hash:
            self.content_hash = ContentHasher.hash_content(self.content)
        
        # Generate commit hash from content + metadata for uniqueness
        if not self.hash:
            # Include content hash, branch, version, and timestamp for unique commit identity
            timestamp = self.metadata.get('timestamp', datetime.now().isoformat())
            hash_input = f"{self.content_hash}:{self.branch}:{self.version}:{timestamp}:{self.message}"
            if self.parent_hash:
                hash_input += f":{self.parent_hash}"
            # Include merge parents for merge commits
            if self.merge_parents:
                hash_input += f":merge_parents:{'|'.join(self.merge_parents)}"
            self.hash = ContentHasher.hash_content(hash_input)[:8]  # Use short hash for commits
    
    def verify_integrity(self) -> bool:
        """Verify content integrity"""
        return ContentHasher.verify_content(self.content, self.content_hash)
    
    def short_hash(self, length: int = 8) -> str:
        """Get short commit hash for display"""
        return self.hash[:length]
    
    def is_merge_commit(self) -> bool:
        """Check if this is a merge commit (has multiple parents)"""
        return len(self.merge_parents) > 0

@dataclass
class BanyanConfig:
    """Configuration for Banyan CLI"""
    api_key: Optional[str] = None
    base_url: str = "https://app.usebanyan.com"
    project_id: Optional[str] = None
    default_branch: str = "main"
    prompt_dir: str = "prompts"
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    active_prompt: Optional[str] = None  # NEW: Currently active prompt
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BanyanConfig':
        return cls(**data)

@dataclass
class MergeState:
    """Track ongoing merge state like Git's .git/MERGE_HEAD"""
    source_branch: str
    target_branch: str
    source_commit_hash: str
    target_commit_hash: str
    base_commit_hash: Optional[str] = None  # Common ancestor
    merge_strategy: str = "auto"
    merge_message: str = ""
    conflicts_resolved: List[str] = None  # Files that have had conflicts resolved
    started_at: str = ""
    
    def __post_init__(self):
        if self.conflicts_resolved is None:
            self.conflicts_resolved = []
        if not self.started_at:
            self.started_at = datetime.now().isoformat()

@dataclass
class PromptState:
    """Represents the current prompt and branch state"""
    prompt_name: str
    branch_name: str = "main"
    last_updated: str = ""
    
    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = datetime.now().isoformat()
    
    @property
    def context(self) -> str:
        """Get the prompt@branch context string"""
        return f"{self.prompt_name}@{self.branch_name}"

class BanyanProjectManager:
    """
    Manages Banyan project structure and configuration with production-ready features:
    - Atomic operations with integrity checking
    - File locking to prevent race conditions
    - Delta compression for efficient storage
    - Comprehensive error handling and recovery
    """
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root or os.getcwd())
        self.banyan_dir = self.project_root / '.banyan'
        self.config_file = self.banyan_dir / 'config.json'
        
        # Prompt-specific directory structure
        self.refs_dir = self.banyan_dir / 'refs'  # refs/{prompt_name}/heads/{branch_name}
        self.staging_dir = self.banyan_dir / 'staging'  # staging/{prompt_name}/{branch_name}.json
        self.commits_dir = self.banyan_dir / 'commits'  # commits/{prompt_name}/{branch_name}.json
        self.index_dir = self.banyan_dir / 'index'  # index/{prompt_name}/{branch_name}.json
        self.conflicts_dir = self.banyan_dir / 'conflicts'  # conflicts/{prompt_name}/{branch_name}.json
        
        self.global_config_dir = Path.home() / '.banyan'
        self.global_config_file = self.global_config_dir / 'config.json'
        
        # Production-ready features
        self.integrity_manager = get_integrity_manager(self.project_root)
        self.storage_manager = StorageManager(self.banyan_dir / 'storage')
        
        # Cache for frequently accessed data
        self._cache = {}
        self._cache_lock = threading.RLock()
    
    @property
    def prompts_dir(self) -> Path:
        """Get the prompts directory from configuration"""
        try:
            if self.config_file.exists():
                config = self.load_config()
                return self.project_root / config.prompt_dir
            else:
                # Use default during initialization
                return self.project_root / BanyanConfig().prompt_dir
        except Exception:
            # Fallback to default if config loading fails
            return self.project_root / BanyanConfig().prompt_dir
    
    def clear_cache(self):
        """Clear all cached data"""
        with self._cache_lock:
            self._cache.clear()
            logger.debug("Cleared project manager cache")
    
    def invalidate_cache(self, resource_pattern: str):
        """Invalidate cache entries matching pattern"""
        with self._cache_lock:
            keys_to_remove = [k for k in self._cache.keys() if resource_pattern in k]
            for key in keys_to_remove:
                del self._cache[key]
            if keys_to_remove:
                logger.debug(f"Invalidated {len(keys_to_remove)} cache entries for pattern: {resource_pattern}")
    
    def is_banyan_project(self) -> bool:
        """Check if current directory is a Banyan project"""
        return self.banyan_dir.exists() and self.config_file.exists()
    
    # === Prompt and Branch State Management ===
    
    def get_current_prompt_state(self) -> Optional[PromptState]:
        """Get the current active prompt and branch state"""
        try:
            config = self.load_config()
            if not config.active_prompt:
                return None
            
            # Get current branch for the active prompt
            current_branch = self.get_prompt_current_branch(config.active_prompt)
            
            return PromptState(
                prompt_name=config.active_prompt,
                branch_name=current_branch
            )
        except Exception as e:
            logger.error(f"Failed to get current prompt state: {e}")
            return None
    
    def set_active_prompt(self, prompt_name: str, branch_name: str = "main") -> bool:
        """Set the active prompt and branch"""
        try:

            if not self.prompt_exists(prompt_name):
                logger.error(f"Prompt '{prompt_name}' does not exist")
                return False
            
            current_state = self.get_current_prompt_state()
            if current_state and current_state.prompt_name != prompt_name:
                self._save_branch_content(current_state.prompt_name, current_state.branch_name)
            
            # Update config with active prompt
            config = self.load_config()
            config.active_prompt = prompt_name
            self.save_config(config)
            
            # Set current branch for this prompt
            if not self.set_prompt_current_branch(prompt_name, branch_name):
                return False
            
            # Load content for the prompt@branch
            self._load_branch_content(prompt_name, branch_name)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to set active prompt: {e}")
            return False
    
    def get_prompt_current_branch(self, prompt_name: str) -> str:
        """Get current branch for a specific prompt"""
        try:
            prompt_head_file = self.refs_dir / prompt_name / 'HEAD'
            if prompt_head_file.exists():
                head_content = prompt_head_file.read_text().strip()
                if head_content.startswith('ref: refs/heads/'):
                    return head_content.replace('ref: refs/heads/', '')
                else:
                    return head_content  # Direct commit hash
            else:
                # Default to main branch
                return "main"
        except Exception as e:
            logger.error(f"Failed to get current branch for prompt '{prompt_name}': {e}")
            return "main"
    
    def set_prompt_current_branch(self, prompt_name: str, branch_name: str) -> bool:
        """Set current branch for a specific prompt"""
        try:
            prompt_refs_dir = self.refs_dir / prompt_name
            prompt_refs_dir.mkdir(parents=True, exist_ok=True)
            
            prompt_head_file = prompt_refs_dir / 'HEAD'
            prompt_head_file.write_text(f'ref: refs/heads/{branch_name}')
            return True
        except Exception as e:
            logger.error(f"Failed to set current branch for prompt '{prompt_name}': {e}")
            return False
    
    def prompt_exists(self, prompt_name: str) -> bool:
        """Check if a prompt exists"""
        prompt_file = self.prompts_dir / f"{prompt_name}.txt"
        return prompt_file.exists()
    
    def list_prompts(self) -> List[str]:
        """List all available prompts"""
        if not self.prompts_dir.exists():
            return []
        
        prompts = []
        for prompt_file in self.prompts_dir.glob("*.txt"):
            prompts.append(prompt_file.stem)
        
        return sorted(prompts)
    
    def create_prompt_branch(self, prompt_name: str, branch_name: str, from_branch: str = "main") -> bool:
        """Create a new branch for a specific prompt"""
        try:
            # Ensure prompt exists
            if not self.prompt_exists(prompt_name):
                logger.error(f"Prompt '{prompt_name}' does not exist")
                return False
            
            # Create refs directory structure
            prompt_refs_dir = self.refs_dir / prompt_name / 'heads'
            prompt_refs_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if branch already exists
            branch_ref_file = prompt_refs_dir / branch_name
            if branch_ref_file.exists():
                logger.error(f"Branch '{branch_name}' already exists for prompt '{prompt_name}'")
                return False
            
            # Get starting commit from source branch
            from_branch_file = prompt_refs_dir / from_branch
            if from_branch_file.exists():
                start_commit = from_branch_file.read_text().strip()
            else:
                # No existing branches, start with empty commit
                start_commit = ""
            
            # Create branch reference
            branch_ref_file.write_text(start_commit)
            
            # Create branch-specific directories
            (self.staging_dir / prompt_name).mkdir(parents=True, exist_ok=True)
            (self.commits_dir / prompt_name).mkdir(parents=True, exist_ok=True)
            (self.index_dir / prompt_name).mkdir(parents=True, exist_ok=True)
            
            from_index = self.load_prompt_index(prompt_name, from_branch)
            if from_index:
                self.save_prompt_index(prompt_name, branch_name, from_index)
                logger.debug(f"Inherited index from '{from_branch}' to '{branch_name}'")
            
            from_versions = self.load_prompt_local_versions(prompt_name, from_branch)
            if from_versions:
                self.save_prompt_local_versions(prompt_name, branch_name, from_versions.copy())
                logger.debug(f"Inherited {len(from_versions)} versions from '{from_branch}' to '{branch_name}'")
            
            from_branch_content_dir = self.banyan_dir / 'branch_content' / prompt_name
            from_branch_file = from_branch_content_dir / f"{from_branch}.txt"
            
            if from_branch_file.exists():
                # Copy content from source branch
                content = from_branch_file.read_text()
                new_branch_file = from_branch_content_dir / f"{branch_name}.txt"
                new_branch_file.parent.mkdir(parents=True, exist_ok=True)
                new_branch_file.write_text(content)
                logger.debug(f"Copied branch content from '{from_branch}' to '{branch_name}'")
            else:
                # If no branch-specific content exists, use current prompt file content
                prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
                if prompt_file_path.exists():
                    content = prompt_file_path.read_text()
                    new_branch_file = from_branch_content_dir / f"{branch_name}.txt"
                    new_branch_file.parent.mkdir(parents=True, exist_ok=True)
                    new_branch_file.write_text(content)
                    logger.debug(f"Initialized '{branch_name}' with current prompt content")
            
            logger.info(f"Created branch '{branch_name}' for prompt '{prompt_name}' from '{from_branch}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create branch '{branch_name}' for prompt '{prompt_name}': {e}")
            return False
    
    def prompt_branch_exists(self, prompt_name: str, branch_name: str) -> bool:
        """Check if a branch exists for a specific prompt"""
        branch_ref_file = self.refs_dir / prompt_name / 'heads' / branch_name
        return branch_ref_file.exists()
    
    def remote_prompt_branch_exists(self, prompt_name: str, branch_name: str, remote: str = 'origin') -> bool:
        """Check if a remote branch exists for a specific prompt"""
        remote_ref_file = self.refs_dir / prompt_name / 'remotes' / remote / branch_name
        return remote_ref_file.exists()
    
    def list_prompt_branches(self, prompt_name: str, remote_only: bool = False, local_only: bool = False) -> List[str]:
        """List branches for a specific prompt with Git-like remote/local segregation"""
        branches = []
        
        if not local_only:
            # Add remote branches with project/branch naming
            prompt_remotes_dir = self.refs_dir / prompt_name / 'remotes'
            if prompt_remotes_dir.exists():
                for remote_dir in prompt_remotes_dir.iterdir():
                    if remote_dir.is_dir():
                        remote_name = remote_dir.name
                        for branch_file in remote_dir.iterdir():
                            if branch_file.is_file():
                                branch_name = f"{remote_name}/{branch_file.name}"
                                branches.append(branch_name)
        
        if not remote_only:
            # Add local branches
            prompt_heads_dir = self.refs_dir / prompt_name / 'heads'
            if prompt_heads_dir.exists():
                for branch_file in prompt_heads_dir.iterdir():
                    if branch_file.is_file():
                        branches.append(branch_file.name)
            elif not remote_only:
                # Default branch if no local branches exist
                branches.append("main")
        
        return sorted(set(branches))
    
    def list_local_prompt_branches(self, prompt_name: str) -> List[str]:
        """List only local branches for a specific prompt"""
        return self.list_prompt_branches(prompt_name, local_only=True)
    
    def list_remote_prompt_branches(self, prompt_name: str, remote: str = 'origin') -> List[str]:
        """List remote branches for a specific prompt with remote/ prefix"""
        prompt_remotes_dir = self.refs_dir / prompt_name / 'remotes' / remote
        if not prompt_remotes_dir.exists():
            return []
        
        branches = []
        for branch_file in prompt_remotes_dir.iterdir():
            if branch_file.is_file():
                branches.append(f"{remote}/{branch_file.name}")
        
        return sorted(branches)
    
    def get_tracking_branch(self, prompt_name: str, local_branch: str) -> Optional[str]:
        """Get the remote tracking branch for a local branch"""
        try:
            tracking_file = self.refs_dir / prompt_name / 'tracking' / local_branch
            if tracking_file.exists():
                return tracking_file.read_text().strip()
            else:
                # Default tracking: if origin/branch exists, track it
                if self.remote_prompt_branch_exists(prompt_name, local_branch, 'origin'):
                    return f"origin/{local_branch}"
                return None
        except Exception as e:
            logger.error(f"Failed to get tracking branch for {prompt_name}@{local_branch}: {e}")
            return None
    
    def set_tracking_branch(self, prompt_name: str, local_branch: str, remote_branch: str) -> bool:
        """Set a local branch to track a remote branch"""
        try:
            tracking_dir = self.refs_dir / prompt_name / 'tracking'
            tracking_dir.mkdir(parents=True, exist_ok=True)
            
            tracking_file = tracking_dir / local_branch
            tracking_file.write_text(remote_branch)
            return True
        except Exception as e:
            logger.error(f"Failed to set tracking branch for {prompt_name}@{local_branch}: {e}")
            return False
    
    def is_branch_name_remote(self, branch_name: str) -> bool:
        """Check if a branch name refers to a remote branch (contains '/')"""
        return '/' in branch_name
    
    def parse_remote_branch(self, remote_branch: str) -> tuple[str, str]:
        """Parse remote branch name into (remote, branch)"""
        if '/' not in remote_branch:
            raise ValueError(f"Invalid remote branch name: {remote_branch}")
        parts = remote_branch.split('/', 1)
        return parts[0], parts[1]
    
    def create_remote_tracking_branch(self, prompt_name: str, branch_name: str, remote_commit_hash: str, remote: str = 'origin') -> bool:
        """Create a remote tracking reference for a branch"""
        try:
            remote_refs_dir = self.refs_dir / prompt_name / 'remotes' / remote
            remote_refs_dir.mkdir(parents=True, exist_ok=True)
            
            remote_ref_file = remote_refs_dir / branch_name
            remote_ref_file.write_text(remote_commit_hash)
            
            return True
        except Exception as e:
            logger.error(f"Failed to create remote tracking branch for '{prompt_name}@{branch_name}': {e}")
            return False
    
    def create_local_branch_from_remote(self, prompt_name: str, local_branch: str, remote_branch: str) -> bool:
        """Create a local branch that tracks a remote branch"""
        try:
            if self.is_branch_name_remote(remote_branch):
                remote, remote_branch_name = self.parse_remote_branch(remote_branch)
                
                # Check if remote branch exists
                if not self.remote_prompt_branch_exists(prompt_name, remote_branch_name, remote):
                    logger.error(f"Remote branch {remote_branch} does not exist")
                    return False
                
                # Get remote commit hash
                remote_ref_file = self.refs_dir / prompt_name / 'remotes' / remote / remote_branch_name
                remote_commit_hash = remote_ref_file.read_text().strip()
                
                # Create local branch pointing to same commit
                if self.update_prompt_branch_ref(prompt_name, local_branch, remote_commit_hash):
                    # Set up tracking
                    self.set_tracking_branch(prompt_name, local_branch, remote_branch)
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Failed to create local branch from remote: {e}")
            return False
    
    def checkout_prompt_branch(self, prompt_name: str, branch_name: str, create_new: bool = False) -> bool:
        """Checkout to a branch for a specific prompt with Git-like remote branch support"""
        try:
            # Ensure prompt exists
            if not self.prompt_exists(prompt_name):
                logger.error(f"Prompt '{prompt_name}' does not exist")
                return False
            
            # Save current branch content before switching
            current_branch = self.get_prompt_current_branch(prompt_name)
            target_branch = branch_name
            
            # Handle remote branch checkout
            if self.is_branch_name_remote(branch_name):
                if create_new:
                    logger.error("Cannot use -b flag with remote branch names")
                    return False
                
                # Extract local branch name from remote branch
                remote, remote_branch_name = self.parse_remote_branch(branch_name)
                
                # Check if local branch with same name exists
                if self.prompt_branch_exists(prompt_name, remote_branch_name):
                    # Switch to existing local branch
                    target_branch = remote_branch_name
                    logger.info(f"Switching to existing local branch '{remote_branch_name}' that tracks '{branch_name}'")
                else:
                    # Create local branch from remote
                    if self.create_local_branch_from_remote(prompt_name, remote_branch_name, branch_name):
                        target_branch = remote_branch_name
                        logger.info(f"Created local branch '{remote_branch_name}' from '{branch_name}'")
                    else:
                        logger.error(f"Failed to create local branch from remote '{branch_name}'")
                        return False
            else:
                # Regular local branch handling
                if current_branch != target_branch:
                    self._save_branch_content(prompt_name, current_branch)
                
                if create_new:
                    # Create new local branch
                    if self.prompt_branch_exists(prompt_name, target_branch):
                        logger.error(f"Branch '{target_branch}' already exists for prompt '{prompt_name}'")
                        return False
                    
                    if not self.create_prompt_branch(prompt_name, target_branch, current_branch):
                        return False
                else:
                    # Switch to existing local branch
                    if not self.prompt_branch_exists(prompt_name, target_branch):
                        logger.error(f"Branch '{target_branch}' does not exist for prompt '{prompt_name}'")
                        return False
            
            # Set current branch for this prompt
            if not self.set_prompt_current_branch(prompt_name, target_branch):
                return False
            
            # Load content for the new branch
            self._load_branch_content(prompt_name, target_branch)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to checkout branch '{branch_name}' for prompt '{prompt_name}': {e}")
            return False
    
    def get_prompt_branch_staging_file(self, prompt_name: str, branch_name: str) -> Path:
        """Get staging file path for specific prompt@branch"""
        return self.staging_dir / prompt_name / f"{branch_name}.json"
    
    def get_prompt_branch_commits_file(self, prompt_name: str, branch_name: str) -> Path:
        """Get commits file path for specific prompt@branch"""
        return self.commits_dir / prompt_name / f"{branch_name}.json"
    
    def get_prompt_branch_index_file(self, prompt_name: str, branch_name: str) -> Path:
        """Get index file path for specific prompt@branch"""
        return self.index_dir / prompt_name / f"{branch_name}.json"
    
    def _save_branch_content(self, prompt_name: str, branch_name: str) -> bool:
        """Save current prompt content to branch-specific storage"""
        try:
            prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
            if not prompt_file_path.exists():
                return True  # Nothing to save
            
            # Read current content
            content = prompt_file_path.read_text()
            
            # Create branch content directory
            branch_content_dir = self.banyan_dir / 'branch_content' / prompt_name
            branch_content_dir.mkdir(parents=True, exist_ok=True)
            
            # Save content to branch-specific file
            branch_file = branch_content_dir / f"{branch_name}.txt"
            branch_file.write_text(content)
            
            logger.debug(f"Saved content for {prompt_name}@{branch_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save branch content for {prompt_name}@{branch_name}: {e}")
            return False
    
    def _load_branch_content(self, prompt_name: str, branch_name: str) -> bool:
        """Load branch-specific content to prompt file"""
        try:
            # Check for branch-specific content
            branch_content_dir = self.banyan_dir / 'branch_content' / prompt_name
            branch_file = branch_content_dir / f"{branch_name}.txt"
            
            prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
            
            if branch_file.exists():
                # Load branch-specific content
                content = branch_file.read_text()
                prompt_file_path.write_text(content)
                logger.debug(f"Loaded content for {prompt_name}@{branch_name}")
            else:
                # Check if this is a new branch - copy from main branch if available
                main_branch_file = branch_content_dir / "main.txt"
                if main_branch_file.exists() and branch_name != "main":
                    content = main_branch_file.read_text()
                    prompt_file_path.write_text(content)
                    # Save this content as the starting point for the new branch
                    branch_file.write_text(content)
                    logger.debug(f"Initialized {prompt_name}@{branch_name} from main branch")
                # If no branch-specific content exists, keep current content
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load branch content for {prompt_name}@{branch_name}: {e}")
            return False
    
    def update_prompt_branch_ref(self, prompt_name: str, branch_name: str, commit_hash: str) -> bool:
        """Update branch reference to point to a specific commit (enhanced for prompt-centric)"""
        try:
            prompt_refs_dir = self.refs_dir / prompt_name / 'heads'
            prompt_refs_dir.mkdir(parents=True, exist_ok=True)
            
            branch_file = prompt_refs_dir / branch_name
            branch_file.write_text(commit_hash)
            return True
        except Exception as e:
            logger.error(f"Failed to update branch ref for '{prompt_name}@{branch_name}': {e}")
            return False
    
    # === Staging Area Management (Enhanced for Prompt-Centric) ===
    
    def load_staging_area(self, prompt_name: str = None, branch_name: str = None) -> List[StagedFile]:
        """Load staged files for specific prompt@branch or current context with integrity verification"""
        try:
            # Use current context if not specified
            if not prompt_name or not branch_name:
                state = self.get_current_prompt_state()
                if not state:
                    return []  # No active context, return empty
                prompt_name = state.prompt_name
                branch_name = state.branch_name
            
            # Check cache first
            cache_key = f"staging_{prompt_name}_{branch_name}"
            with self._cache_lock:
                if cache_key in self._cache:
                    return self._cache[cache_key]
            
            # Get prompt-branch specific staging file
            staging_file = self.get_prompt_branch_staging_file(prompt_name, branch_name)
            if not staging_file.exists():
                return []
            
            # Load with integrity verification
            data, content_hash = AtomicFileOperations.read_json_verified(staging_file)
            staged_files = [StagedFile(**item) for item in data]
            
            # Verify integrity of each staged file
            valid_files = []
            for staged_file in staged_files:
                if staged_file.verify_integrity():
                    valid_files.append(staged_file)
                else:
                    logger.warning(f"Staged file {staged_file.name} failed integrity check, excluding")
            
            # Cache the result
            with self._cache_lock:
                self._cache[cache_key] = valid_files
            
            return valid_files
            
        except IntegrityError as e:
            logger.error(f"Integrity error loading staging area for {prompt_name}@{branch_name}: {e}")
            return []
        except Exception as e:
            logger.error(f"Failed to load staging area for {prompt_name}@{branch_name}: {e}")
            return []
    
    def save_staging_area(self, staged_files: List[StagedFile], prompt_name: str = None, branch_name: str = None) -> bool:
        """Save staged files for specific prompt@branch or current context with atomic operations"""
        try:
            # Use current context if not specified
            if not prompt_name or not branch_name:
                state = self.get_current_prompt_state()
                if not state:
                    logger.error("No active prompt context for saving staging area")
                    return False
                prompt_name = state.prompt_name
                branch_name = state.branch_name
            
            # Verify integrity of staged files
            for staged_file in staged_files:
                if not staged_file.verify_integrity():
                    logger.error(f"Integrity check failed for staged file {staged_file.name}")
                    return False
            
            # Use resource locking to prevent concurrent modifications
            with self.integrity_manager.lock_resource(f"staging_{prompt_name}_{branch_name}"):
                # Ensure staging directory exists
                staging_dir = self.staging_dir / prompt_name
                staging_dir.mkdir(parents=True, exist_ok=True)
                
                # Save to prompt-branch specific staging file atomically
                staging_file = self.get_prompt_branch_staging_file(prompt_name, branch_name)
                data = [asdict(sf) for sf in staged_files]
                AtomicFileOperations.write_json_atomic(staging_file, data)
                
                logger.debug(f"Atomically saved staging area for {prompt_name}@{branch_name}")
                return True
            
        except Exception as e:
            logger.error(f"Failed to save staging area for {prompt_name}@{branch_name}: {e}")
            return False
    
    def stage_prompt_content(self, prompt_name: str, content: str, operation: str = "modified") -> bool:
        """Stage content for a specific prompt using current context with storage optimization"""
        try:
            state = self.get_current_prompt_state()
            if not state:
                logger.error("No active prompt context. Use 'banyan prompt <name>' to set active prompt.")
                return False
            
            if prompt_name != state.prompt_name:
                logger.error(f"Cannot stage '{prompt_name}' - current active prompt is '{state.prompt_name}'")
                return False
            
            # Save current content to branch-specific storage with delta compression
            self._save_branch_content(prompt_name, state.branch_name)
            
            # Store content in storage manager for efficient access
            base_hash = None
            index = self.load_prompt_index(prompt_name, state.branch_name)
            if prompt_name in index:
                # Use existing content as base for delta compression
                existing_entry = index[prompt_name]
                base_hash = existing_entry.content_hash
            
            content_hash = self.storage_manager.store(content, "prompt", base_hash)
            
            # Create staging entry with verified hash
            staged_file = StagedFile(
                name=prompt_name,
                content=content,
                branch=state.branch_name,
                operation=operation,
                hash=content_hash
            )
            
            # Verify the staged file integrity
            if not staged_file.verify_integrity():
                logger.error(f"Staged file integrity verification failed for {prompt_name}")
                return False
            
            # Load existing staging area for current prompt@branch
            staged_files = self.load_staging_area(state.prompt_name, state.branch_name)
            
            # Remove existing entry for this prompt
            staged_files = [sf for sf in staged_files if sf.name != prompt_name]
            
            # Add new staged file (unless deleting)
            if operation != "deleted":
                staged_files.append(staged_file)
            
            # Invalidate cache for this staging area
            self.invalidate_cache(f"staging_{state.prompt_name}_{state.branch_name}")
            
            # Save staging area for current prompt@branch
            return self.save_staging_area(staged_files, state.prompt_name, state.branch_name)
            
        except Exception as e:
            logger.error(f"Failed to stage prompt content: {e}")
            return False
    
    def unstage_file(self, file_name: str) -> bool:
        """Remove file from staging area for current prompt@branch"""
        try:
            state = self.get_current_prompt_state()
            if not state:
                logger.error("No active prompt context for unstaging file")
                return False
            
            staged_files = self.load_staging_area(state.prompt_name, state.branch_name)
            staged_files = [sf for sf in staged_files if sf.name != file_name]
            return self.save_staging_area(staged_files, state.prompt_name, state.branch_name)
        except Exception as e:
            logger.error(f"Failed to unstage file: {e}")
            return False
    
    def clear_staging_area(self, prompt_name: str = None, branch_name: str = None) -> bool:
        """Clear all staged files for specific prompt@branch or current context"""
        try:
            # Use current context if not specified
            if not prompt_name or not branch_name:
                state = self.get_current_prompt_state()
                if not state:
                    # No active context, nothing to clear
                    return True
                prompt_name = state.prompt_name
                branch_name = state.branch_name
            
            # Clear prompt-branch specific staging file
            staging_file = self.get_prompt_branch_staging_file(prompt_name, branch_name)
            if staging_file.exists():
                staging_file.unlink()
            
            return True
        except Exception as e:
            logger.error(f"Failed to clear staging area for {prompt_name}@{branch_name}: {e}")
            return False
    
    # === Prompt-specific Index Management ===
    
    def load_prompt_index(self, prompt_name: str, branch_name: str) -> Dict[str, IndexEntry]:
        """Load the index for a specific prompt@branch"""
        index_file = self.get_prompt_branch_index_file(prompt_name, branch_name)
        if not index_file.exists():
            return {}
        
        try:
            with open(index_file, 'r') as f:
                data = json.load(f)
            return {name: IndexEntry(**entry) for name, entry in data.items()}
        except Exception as e:
            logger.error(f"Failed to load index for {prompt_name}@{branch_name}: {e}")
            return {}
    
    def save_prompt_index(self, prompt_name: str, branch_name: str, index: Dict[str, IndexEntry]) -> bool:
        """Save the index for a specific prompt@branch"""
        try:
            # Ensure index directory exists
            index_dir = self.index_dir / prompt_name
            index_dir.mkdir(parents=True, exist_ok=True)
            
            index_file = self.get_prompt_branch_index_file(prompt_name, branch_name)
            data = {name: asdict(entry) for name, entry in index.items()}
            with open(index_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save index for {prompt_name}@{branch_name}: {e}")
            return False
    
    def initialize_prompt_index_if_needed(self, prompt_name: str, branch_name: str) -> bool:
        """Initialize the index for a prompt if it doesn't exist yet"""
        try:
            index = self.load_prompt_index(prompt_name, branch_name)
            if prompt_name not in index:
                prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
                if prompt_file_path.exists():
                    content = prompt_file_path.read_text()
                    content_hash = ContentHasher.hash_content(content)
                    index[prompt_name] = IndexEntry(
                        name=prompt_name,
                        content_hash=content_hash
                    )
                    self.save_prompt_index(prompt_name, branch_name, index)
                    logger.debug(f"Initialized index for {prompt_name}@{branch_name}")
                    return True
            return True
        except Exception as e:
            logger.error(f"Failed to initialize index for {prompt_name}@{branch_name}: {e}")
            return False
    
    def update_prompt_index_entry(self, prompt: PromptFile, prompt_name: str = None, branch_name: str = None) -> bool:
        """Update index entry for a prompt in specific branch"""
        try:
            # Use current context if not specified
            if not prompt_name or not branch_name:
                state = self.get_current_prompt_state()
                if not state:
                    logger.error("No active prompt context for updating index")
                    return False
                prompt_name = state.prompt_name
                branch_name = state.branch_name
            
            # Ensure index exists and is initialized
            self.initialize_prompt_index_if_needed(prompt_name, branch_name)
            
            index = self.load_prompt_index(prompt_name, branch_name)
            index[prompt.name] = IndexEntry(
                name=prompt.name,
                content_hash=prompt.content_hash()
            )
            return self.save_prompt_index(prompt_name, branch_name, index)
        except Exception as e:
            logger.error(f"Failed to update index entry for {prompt_name}@{branch_name}: {e}")
            return False
    
    def update_prompt_index_from_remote(self, prompt_name: str, branch_name: str, content: str, version: str) -> bool:
        """Update index entry from remote pull for specific prompt@branch"""
        try:
            index = self.load_prompt_index(prompt_name, branch_name)
            content_hash = ContentHasher.hash_content(content)
            index[prompt_name] = IndexEntry(
                name=prompt_name,
                content_hash=content_hash
            )
            
            # Also track the remote version for future commits
            versions = self.load_prompt_local_versions(prompt_name, branch_name)
            # Create a proper version entry to track remote state
            remote_version = LocalVersion(
                name=prompt_name,
                content=content,
                branch=branch_name,
                version=version,
                message=f"Pulled from remote (v{version})",
                metadata={
                    "created_by": "banyan-cli-pull",
                    "source": "remote",
                    "original_version": version,
                    "file_path": f"{prompt_name}.txt",
                    "operation": "pulled",
                    "timestamp": datetime.now().isoformat(),
                    "author_name": "Remote",
                    "author_email": ""
                },
                pushed=True  # Mark as pushed since it came from remote
            )
            
            # Remove any existing version for this prompt with same content hash
            existing_hash = remote_version.hash
            versions = [v for v in versions if v.hash != existing_hash]
            versions.append(remote_version)
            
            self.save_prompt_local_versions(prompt_name, branch_name, versions)
            return self.save_prompt_index(prompt_name, branch_name, index)
        except Exception as e:
            logger.error(f"Failed to update index from remote for {prompt_name}@{branch_name}: {e}")
            return False
    
    def remove_prompt_index_entry(self, prompt_name: str, target_prompt: str = None, branch_name: str = None) -> bool:
        """Remove entry from prompt-specific index"""
        try:
            # Use current context if not specified
            if not target_prompt or not branch_name:
                state = self.get_current_prompt_state()
                if not state:
                    logger.error("No active prompt context for removing index entry")
                    return False
                target_prompt = state.prompt_name
                branch_name = state.branch_name
            
            index = self.load_prompt_index(target_prompt, branch_name)
            if prompt_name in index:
                del index[prompt_name]
                return self.save_prompt_index(target_prompt, branch_name, index)
            return True
        except Exception as e:
            logger.error(f"Failed to remove index entry for {target_prompt}@{branch_name}: {e}")
            return False
    
    # === Prompt-specific Conflict Management ===
    
    def load_prompt_conflicts(self, prompt_name: str, branch_name: str) -> List[ConflictInfo]:
        """Load conflict information for specific prompt@branch"""
        conflict_file = self.conflicts_dir / prompt_name / f"{branch_name}.json"
        if not conflict_file.exists():
            return []
        
        try:
            with open(conflict_file, 'r') as f:
                data = json.load(f)
            return [ConflictInfo(**conflict) for conflict in data]
        except Exception as e:
            logger.error(f"Failed to load conflicts for {prompt_name}@{branch_name}: {e}")
            return []
    
    def save_prompt_conflicts(self, prompt_name: str, branch_name: str, conflicts: List[ConflictInfo]) -> bool:
        """Save conflict information for specific prompt@branch"""
        try:
            # Ensure conflicts directory exists
            conflict_dir = self.conflicts_dir / prompt_name
            conflict_dir.mkdir(parents=True, exist_ok=True)
            
            conflict_file = self.conflicts_dir / prompt_name / f"{branch_name}.json"
            data = [asdict(conflict) for conflict in conflicts]
            with open(conflict_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save conflicts for {prompt_name}@{branch_name}: {e}")
            return False
    
    def add_prompt_conflict(self, prompt_name: str, branch_name: str, conflict: ConflictInfo) -> bool:
        """Add a conflict to track for specific prompt@branch"""
        try:
            conflicts = self.load_prompt_conflicts(prompt_name, branch_name)
            # Remove existing conflict for same file
            conflicts = [c for c in conflicts if c.name != conflict.name]
            conflicts.append(conflict)
            return self.save_prompt_conflicts(prompt_name, branch_name, conflicts)
        except Exception as e:
            logger.error(f"Failed to add conflict for {prompt_name}@{branch_name}: {e}")
            return False
    
    def resolve_prompt_conflict(self, prompt_name: str, branch_name: str, conflict_name: str) -> bool:
        """Mark a conflict as resolved for specific prompt@branch"""
        try:
            conflicts = self.load_prompt_conflicts(prompt_name, branch_name)
            conflicts = [c for c in conflicts if c.name != conflict_name]
            return self.save_prompt_conflicts(prompt_name, branch_name, conflicts)
        except Exception as e:
            logger.error(f"Failed to resolve conflict for {prompt_name}@{branch_name}: {e}")
            return False
    
    def has_prompt_conflicts(self, prompt_name: str, branch_name: str) -> bool:
        """Check if there are any unresolved conflicts for specific prompt@branch"""
        return len(self.load_prompt_conflicts(prompt_name, branch_name)) > 0
    
    def create_conflict_file(self, conflict: ConflictInfo) -> bool:
        """Create a file with conflict markers"""
        try:
            conflict_content = conflict.generate_conflict_markers()
            file_path = self.prompts_dir / f"{conflict.name}.txt"
            file_path.write_text(conflict_content)
            return True
        except Exception as e:
            logger.error(f"Failed to create conflict file: {e}")
            return False
    
    # === Prompt-specific Local Version Management ===
    
    def load_prompt_local_versions(self, prompt_name: str, branch_name: str) -> List[LocalVersion]:
        """Load local versions for specific prompt@branch"""
        commits_file = self.get_prompt_branch_commits_file(prompt_name, branch_name)
        if not commits_file.exists():
            return []
        
        try:
            with open(commits_file, 'r') as f:
                data = json.load(f)
            return [LocalVersion(**item) for item in data]
        except Exception as e:
            logger.error(f"Failed to load versions for {prompt_name}@{branch_name}: {e}")
            return []
    
    def save_prompt_local_versions(self, prompt_name: str, branch_name: str, versions: List[LocalVersion]) -> bool:
        """Save local versions for specific prompt@branch"""
        try:
            # Ensure commits directory exists
            commits_dir = self.commits_dir / prompt_name
            commits_dir.mkdir(parents=True, exist_ok=True)
            
            commits_file = self.get_prompt_branch_commits_file(prompt_name, branch_name)
            data = [asdict(version) for version in versions]
            with open(commits_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save versions for {prompt_name}@{branch_name}: {e}")
            return False
    
    def get_next_prompt_version(self, prompt_name: str, branch_name: str) -> str:
        """Get next version number for specific prompt@branch in web UI format (1.0, 1.1, 1.2)"""
        versions = self.load_prompt_local_versions(prompt_name, branch_name)
        
        if not versions:
            return "1.0"
        
        # Get latest version
        latest_version = "1.0"
        for version in versions:
            if self._compare_versions(version.version, latest_version) > 0:
                latest_version = version.version
        
        # Increment minor version by default
        if '.' in latest_version:
            major, minor = latest_version.split('.')
            return f"{major}.{int(minor) + 1}"
        else:
            # Handle edge case where version might not have decimal
            return f"{latest_version}.1"
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compare two versions in web UI format (1.0, 1.1). Returns -1, 0, or 1"""
        def parse_version(v):
            parts = v.split('.')
            if len(parts) == 1:
                return (int(parts[0]), 0)
            elif len(parts) == 2:
                return (int(parts[0]), int(parts[1]))
            else:
                # Handle semantic versioning by taking only major.minor
                return (int(parts[0]), int(parts[1]))
        
        v1_parts = parse_version(v1)
        v2_parts = parse_version(v2)
        
        if v1_parts < v2_parts:
            return -1
        elif v1_parts > v2_parts:
            return 1
        else:
            return 0
    
    def create_prompt_commit(self, staging_area: List[StagedFile], message: str, client=None) -> Optional[List[LocalVersion]]:
        """Create local versions from staged files for current prompt@branch (automatically handles metadata)"""
        try:
            # Get current prompt state for prompt-centric commits
            current_state = self.get_current_prompt_state()
            if not current_state:
                logger.error("No active prompt state for commit")
                return None
            
            versions = []
            
            # Get remote versions to ensure we continue from the right version
            remote_prompts = {}
            if client:
                remote_prompts = self.get_remote_prompts(client)
            
            # Load config to get author information
            config = self.load_config()
            
            # Ensure we have author info
            if client and (not config.author_name or not config.author_email):
                self.update_config_with_author_info(client)
                config = self.load_config()  # Reload config
            
            for staged_file in staging_area:
                # Ensure staged file belongs to current prompt context
                if staged_file.name != current_state.prompt_name:
                    logger.error(f"Cannot commit staged file '{staged_file.name}' - active prompt is '{current_state.prompt_name}'")
                    continue
                
                # Auto-generate metadata with author information
                metadata = {
                    "created_by": "banyan-cli",
                    "file_path": f"{staged_file.name}.txt",
                    "operation": staged_file.operation,
                    "timestamp": datetime.now().isoformat(),
                    "author_name": config.author_name or "Unknown",
                    "author_email": config.author_email or ""
                }
                
                # Find highest version for this prompt and branch across local and remote
                try:
                    local_versions = self.load_prompt_local_versions(current_state.prompt_name, current_state.branch_name)
                    
                    # Start with version 1.0
                    highest_version = 1.0
                    
                    # Check local versions for this specific prompt and branch
                    for existing_version in local_versions:
                        try:
                            version_num = float(existing_version.version)
                            if version_num >= highest_version:
                                highest_version = version_num
                        except (ValueError, TypeError):
                            continue
                    
                    # Check remote versions  
                    if staged_file.name in remote_prompts:
                        try:
                            remote_version = remote_prompts[staged_file.name].get('version', '1.0')
                            remote_version_num = float(remote_version)
                            if remote_version_num >= highest_version:
                                highest_version = remote_version_num
                        except (ValueError, TypeError):
                            pass
                    
                    # Increment version for new commit
                    if highest_version >= 1.0:
                        highest_version += 0.1
                    else:
                        highest_version = 1.0
                
                except Exception:
                    highest_version = 1.0
                
                version = LocalVersion(
                    name=staged_file.name,
                    content=staged_file.content,
                    branch=current_state.branch_name,  # Use current branch from state
                    version=f"{highest_version:.1f}",
                    metadata=metadata,
                    message=message
                )
                
                versions.append(version)
            
            # Save versions to prompt-specific storage
            if versions:
                existing_versions = self.load_prompt_local_versions(current_state.prompt_name, current_state.branch_name)
                existing_versions.extend(versions)
                self.save_prompt_local_versions(current_state.prompt_name, current_state.branch_name, existing_versions)
                
                # Update prompt-specific branch references to point to the latest commit
                for version in versions:
                    self.update_prompt_branch_ref(version.name, version.branch, version.hash)
                    
                    # Also save the committed content to branch-specific storage
                    self._save_branch_content(version.name, version.branch)
            
            return versions
            
        except Exception as e:
            logger.error(f"Failed to create versions: {e}")
            return None
    
    def get_unpushed_prompt_versions(self, prompt_name: str, branch_name: str) -> List[LocalVersion]:
        """Get versions that haven't been pushed for specific prompt@branch"""
        versions = self.load_prompt_local_versions(prompt_name, branch_name)
        return [v for v in versions if not v.pushed]
    
    def mark_prompt_versions_as_pushed(self, prompt_name: str, branch_name: str, version_hashes: List[str]) -> bool:
        """Mark versions as pushed for specific prompt@branch"""
        try:
            versions = self.load_prompt_local_versions(prompt_name, branch_name)
            for version in versions:
                if version.hash in version_hashes:
                    version.pushed = True
            return self.save_prompt_local_versions(prompt_name, branch_name, versions)
        except Exception as e:
            logger.error(f"Failed to mark versions as pushed for {prompt_name}@{branch_name}: {e}")
            return False
    
    # === Existing methods (keeping them) ===
    
    def init_project(
        self,
        project_id: str,
        base_url: Optional[str] = None,
        branch: str = "main"
    ) -> bool:
        """Initialize a new Banyan project"""
        try:
            # Create directory structure
            self.banyan_dir.mkdir(exist_ok=True)
            
            # Load global config for defaults
            global_config = self.load_global_config()
            
            # Create project config
            config = BanyanConfig(
                project_id=project_id,
                base_url=base_url or global_config.base_url,
                default_branch=branch,
                api_key=global_config.api_key  # Use global API key as default
            )
            
            self.save_config(config)
            
            # Create prompts directory in project root (after config is saved)
            prompts_dir = self.project_root / config.prompt_dir
            prompts_dir.mkdir(exist_ok=True)
            
            # Create .gitignore entry
            gitignore_path = self.project_root / '.gitignore'
            gitignore_content = "\n# Banyan CLI - Internal files (keep prompts directory visible)\n.banyan/config.json\n.banyan/staging/\n.banyan/commits/\n.banyan/index/\n.banyan/refs/\n.banyan/branch_content/\n.banyan/conflicts/\n.banyan/merge_state/\n.banyan/storage/\n.banyan/metadata/\n"
            
            if gitignore_path.exists():
                existing_content = gitignore_path.read_text()
                banyan_entries = ['.banyan/config.json', '.banyan/staging/', '.banyan/commits/', '.banyan/index/', '.banyan/refs/', '.banyan/branch_content/', '.banyan/conflicts/', '.banyan/merge_state/', '.banyan/storage/', '.banyan/metadata/']
                missing_entries = [entry for entry in banyan_entries if entry not in existing_content]
                if missing_entries:
                    with open(gitignore_path, 'a') as f:
                        f.write(gitignore_content)
            else:
                gitignore_path.write_text(gitignore_content)
            
            # Create README for prompts directory
            readme_path = prompts_dir / 'README.md'
            readme_content = """# Banyan Prompts Directory

This directory contains your prompt templates as simple text files.

## How to Use

1. **Create/Edit Prompts**: Simply create or edit `.txt` files in this directory
   - Each file represents one prompt
   - File name becomes the prompt name (e.g., `my-prompt.txt` → "my-prompt")
   - Content is plain text - just write your prompt directly

2. **Branch Management**: Each prompt has its own independent branches
   - Switch prompts: `banyan prompt <name>`
   - Switch branches: `banyan branch <branch>` or `banyan branch -b <new-branch>`
   - When you switch branches, the content in the file will automatically update

3. **Version Control Workflow**:
   ```bash
   # Edit your prompt file directly in this directory
   vim my-prompt.txt
   
   # Stage your changes
   banyan add my-prompt
   
   # Commit your changes
   banyan commit -m "Improved prompt clarity"
   
   # Pull latest changes
   banyan pull
   
   # Push to web UI
   banyan push
   
   # Handle merge conflicts
   banyan status  # Shows conflicts
   # Edit files to resolve conflicts
   banyan add my-prompt  # Mark as resolved
   banyan commit -m "Resolve merge conflict"
   ```

## Example Prompt File

**File: customer-service.txt**
```
You are a helpful customer service representative for {{company_name}}.

Customer inquiry: {{user_message}}

Please provide a professional, empathetic response that:
- Addresses their concern directly
- Offers a solution or next steps
- Maintains a friendly tone

Response:
```

## Commands Reference
- `banyan prompt --list` - List all prompts
- `banyan prompt <name>` - Switch to a prompt
- `banyan branch --list` - List branches for current prompt
- `banyan branch <branch>` - Switch branches
- `banyan branch -b <branch>` - Create and switch to new branch
- `banyan status` - Check current state
- `banyan add <prompt-name>` - Stage changes
- `banyan commit -m "message"` - Create version
- `banyan push` - Upload to web UI
- `banyan pull` - Download from web UI
- `banyan merge <branch>` - Merge branches
- `banyan merge --abort` - Abort current merge

## Important Notes
- **Branch-specific content**: Each branch of a prompt can have different content
- **Auto-switching**: When you switch branches, the file content automatically updates
- **Direct editing**: You work directly with these files - no complex formats needed
- **Git-like workflow**: Familiar staging, committing, and pushing workflow
"""
            readme_path.write_text(readme_content)
            
            logger.info(f"Initialized Banyan project in {self.project_root}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize project: {e}")
            return False
    
    def load_config(self) -> BanyanConfig:
        """Load project configuration with integrity verification"""
        if not self.config_file.exists():
            return BanyanConfig()
        
        try:
            # Try atomic read with integrity verification
            data, content_hash = AtomicFileOperations.read_json_verified(self.config_file)
            return BanyanConfig.from_dict(data)
        except IntegrityError as e:
            logger.warning(f"Config integrity error, falling back to regular read: {e}")
            # Fall back to regular read for backwards compatibility
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                return BanyanConfig.from_dict(data)
            except Exception as fallback_e:
                logger.error(f"Failed to load config: {fallback_e}")
                return BanyanConfig()
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return BanyanConfig()
    
    def save_config(self, config: BanyanConfig) -> bool:
        """Save project configuration with atomic operations and locking"""
        try:
            self.banyan_dir.mkdir(exist_ok=True)
            
            # Use resource locking to prevent concurrent modifications
            with self.integrity_manager.lock_resource("project_config"):
                content_hash = AtomicFileOperations.write_json_atomic(self.config_file, config.to_dict())
                logger.debug(f"Atomically saved config with hash {content_hash[:8]}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False
    
    def load_global_config(self) -> BanyanConfig:
        """Load global configuration"""
        if not self.global_config_file.exists():
            return BanyanConfig()
        
        try:
            with open(self.global_config_file, 'r') as f:
                data = json.load(f)
            return BanyanConfig.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to load global config: {e}")
            return BanyanConfig()
    
    def save_global_config(self, config: BanyanConfig) -> bool:
        """Save global configuration"""
        try:
            self.global_config_dir.mkdir(exist_ok=True)
            with open(self.global_config_file, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save global config: {e}")
            return False
    
    def get_author_info_from_database(self, client) -> Dict[str, Optional[str]]:
        """Get author name and email from the database using the API"""
        try:
            # Make an API call to get user information using API key auth
            response = client._make_request('GET', 'api/auth/cli-user')
            if response.success and response.data:
                user_data = response.data
                return {
                    'author_name': user_data.get('full_name'),
                    'author_email': user_data.get('email')
                }
        except Exception as e:
            logger.debug(f"Could not fetch author info from database: {e}")
        
        return {
            'author_name': None,
            'author_email': None
        }
    
    def update_config_with_author_info(self, client) -> bool:
        """Update local config with author information from database"""
        try:
            config = self.load_config()
            
            # Skip if we already have author info
            if config.author_name and config.author_email:
                return True
            
            # Get author info from database
            author_info = self.get_author_info_from_database(client)
            
            if author_info['author_name'] or author_info['author_email']:
                # Update config with database info
                if author_info['author_name'] and not config.author_name:
                    config.author_name = author_info['author_name']
                if author_info['author_email'] and not config.author_email:
                    config.author_email = author_info['author_email']
                
                # Save updated config
                return self.save_config(config)
            
            return True
        except Exception as e:
            logger.error(f"Failed to update config with author info: {e}")
            return False
    
    def load_local_prompts(self) -> List[PromptFile]:
        """Load all prompt files from prompts directory"""
        prompts = []
        
        if not self.prompts_dir.exists():
            return prompts
        
        try:
            # Support both .txt and .yaml files
            for pattern in ['*.txt', '*.yaml', '*.yml']:
                for file_path in self.prompts_dir.glob(pattern):
                    if file_path.is_file():
                        try:
                            prompt = PromptFile.from_file(file_path)
                            prompts.append(prompt)
                        except Exception as e:
                            logger.error(f"Failed to load prompt file {file_path}: {e}")
                            continue
            
            return prompts
            
        except Exception as e:
            logger.error(f"Failed to load local prompts: {e}")
            return []
    
    def save_prompt_file(self, prompt: PromptFile) -> bool:
        """Save a prompt to a simple text file"""
        try:
            self.prompts_dir.mkdir(exist_ok=True)
            return prompt.save_to_file(self.prompts_dir)
        except Exception as e:
            logger.error(f"Failed to save prompt file: {e}")
            return False
    
    def delete_prompt_file(self, prompt_name: str) -> bool:
        """Delete a local prompt file"""
        try:
            file_path = self.prompts_dir / f"{prompt_name}.json"
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete prompt {prompt_name}: {e}")
            return False
    
    def save_prompt_metadata(self, prompt_name: str, metadata: Dict[str, Any]) -> bool:
        """Save metadata for a prompt (including description)"""
        try:
            metadata_dir = self.banyan_dir / "metadata"
            metadata_dir.mkdir(exist_ok=True)
            
            metadata_file = metadata_dir / f"{prompt_name}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Failed to save metadata for prompt {prompt_name}: {e}")
            return False
    
    def load_prompt_metadata(self, prompt_name: str) -> Dict[str, Any]:
        """Load metadata for a prompt"""
        try:
            metadata_file = self.banyan_dir / "metadata" / f"{prompt_name}.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to load metadata for prompt {prompt_name}: {e}")
            return {}

    def get_remote_prompts(self, client) -> Dict[str, Dict[str, Any]]:
        """Get remote prompts for comparison"""
        try:
            config = self.load_config()
            if not config.project_id:
                return {}
            
            response = client.list_prompts(project_id=config.project_id)
            if not response.success:
                logger.error(f"Failed to fetch remote prompts: {response.error}")
                return {}
            
            # Handle different response data structures
            if isinstance(response.data, dict):
                prompts_data = response.data.get('prompts', [])
            elif isinstance(response.data, list):
                prompts_data = response.data
            else:
                logger.error(f"Unexpected response data type: {type(response.data)}")
                return {}
            
            # Create a mapping of prompt name to latest version info
            remote_prompts = {}
            for prompt in prompts_data:
                # Handle case where prompt might be a string or dict
                if isinstance(prompt, str):
                    continue
                    
                if not isinstance(prompt, dict):
                    continue
                
                prompt_name = prompt.get('name')
                if not prompt_name:
                    continue
                
                versions = prompt.get('versions', [])
                if versions and len(versions) > 0:
                    # Get the active version or the latest version
                    active_version = None
                    for version in versions:
                        if isinstance(version, dict) and version.get('is_active'):
                            active_version = version
                            break
                    
                    if not active_version and versions:
                        active_version = versions[0] if isinstance(versions[0], dict) else None
                    
                    if active_version and isinstance(active_version, dict):
                        content = active_version.get('content', '')
                        remote_prompts[prompt_name] = {
                            'id': prompt.get('id'),
                            'content': content,
                            'version': active_version.get('version_number', '1.0'),
                            'hash': ContentHasher.hash_content(content)
                        }
            
            return remote_prompts
        except Exception as e:
            logger.error(f"Failed to get remote prompts: {e}")
            return {}
    
    def get_prompt_working_directory_status(self, client, prompt_name: str, branch_name: str) -> Dict[str, str]:
        """Get Git-like status for specific prompt@branch"""
        try:
            # Only check the specific prompt
            prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
            if not prompt_file_path.exists():
                return {prompt_name: 'deleted'}
            
            prompt = PromptFile.from_file(prompt_file_path)
            remote_prompts = self.get_remote_prompts(client)
            staged_files = {sf.name: sf for sf in self.load_staging_area(prompt_name, branch_name)}
            index = self.load_prompt_index(prompt_name, branch_name)
            conflicts = {c.name for c in self.load_prompt_conflicts(prompt_name, branch_name)}
            
            status = {}
            
            # Check for conflicts first
            if prompt_name in conflicts:
                status[prompt_name] = 'conflict'
                return status
            
            # Check if staged
            if prompt_name in staged_files:
                staged_file = staged_files[prompt_name]
                # Check if working directory differs from staged
                if prompt.content_hash() != staged_file.hash:
                    status[prompt_name] = 'staged+modified'  # Both staged and modified
                else:
                    status[prompt_name] = 'staged'
                return status
            
            # Check against index (last committed state)
            if prompt_name in index:
                index_entry = index[prompt_name]
                if prompt.content_hash() != index_entry.content_hash:
                    status[prompt_name] = 'modified'
                else:
                    status[prompt_name] = 'unchanged'
            elif prompt_name in remote_prompts:
                # No index entry but exists remotely - compare with remote
                remote_hash = remote_prompts[prompt_name]['hash']
                local_hash = prompt.content_hash()
                
                if local_hash != remote_hash:
                    status[prompt_name] = 'modified'
                else:
                    status[prompt_name] = 'unchanged'
            else:
                # New file, not in index or remote
                status[prompt_name] = 'untracked'
            
            return status
        except Exception as e:
            logger.error(f"Failed to get working directory status for {prompt_name}@{branch_name}: {e}")
            return {}

    def sync_remote_branches_for_prompt(self, client, prompt_name: str, force: bool = False) -> Dict[str, Any]:
        """
        Sync all branches for a prompt from remote, creating local branch structure.
        
        Returns:
            Dict with sync results: {
                'branches_synced': int,
                'branches_created': List[str],
                'branches_updated': List[str],
                'errors': List[str]
            }
        """
        result = {
            'branches_synced': 0,
            'branches_created': [],
            'branches_updated': [],
            'errors': []
        }
        
        try:
            # Ensure prompt exists locally
            if not self.prompt_exists(prompt_name):
                # Create the prompt file first (we'll update content from remote)
                prompt_file = PromptFile(name=prompt_name, content="# Placeholder content")
                self.save_prompt_file(prompt_file)
            
            # Fetch all remote branches for this prompt
            remote_branches = self.fetch_remote_prompt_branches(client, prompt_name)
            
            if not remote_branches:
                result['errors'].append(f"No remote branches found for prompt '{prompt_name}'")
                return result
            
            logger.info(f"Found {len(remote_branches)} remote branches for '{prompt_name}'")
            
            # Process each remote branch
            for remote_branch in remote_branches:
                branch_name = remote_branch.get('name', 'unknown')
                
                try:
                    # Fetch the latest content for this branch
                    branch_content = self.fetch_remote_prompt_version_for_branch(client, prompt_name, branch_name)
                    
                    if not branch_content:
                        result['errors'].append(f"Failed to fetch content for branch '{branch_name}'")
                        continue
                    
                    # Check if local branch exists
                    branch_exists = self.prompt_branch_exists(prompt_name, branch_name)
                    
                    if not branch_exists:
                        # Create new local branch
                        if self.create_prompt_branch(prompt_name, branch_name, "main"):
                            result['branches_created'].append(branch_name)
                            logger.info(f"Created local branch '{branch_name}' for prompt '{prompt_name}'")
                        else:
                            result['errors'].append(f"Failed to create local branch '{branch_name}'")
                            continue
                    
                    # Create/update remote tracking reference
                    remote_version = branch_content.get('version', '1.0')
                    remote_hash = ContentHasher.hash_content(branch_content.get('content', ''))
                    
                    # Create remote tracking reference with origin/ prefix
                    self.create_remote_tracking_branch(prompt_name, branch_name, remote_hash, 'origin')
                    
                    # Update local branch reference if it exists
                    if branch_exists:
                        self.update_prompt_branch_ref(prompt_name, branch_name, remote_hash)
                        result['branches_updated'].append(branch_name)
                    else:
                        # Create local branch from remote
                        self.update_prompt_branch_ref(prompt_name, branch_name, remote_hash)
                        # Set up tracking relationship
                        self.set_tracking_branch(prompt_name, branch_name, f"origin/{branch_name}")
                        result['branches_created'].append(branch_name)
                    
                    # Update prompt content file if this is the currently active branch
                    current_state = self.get_current_prompt_state()
                    if (current_state and 
                        current_state.prompt_name == prompt_name and 
                        current_state.branch_name == branch_name):
                        
                        # Update the actual prompt file with remote content
                        remote_content = branch_content.get('content', '')
                        if remote_content:
                            prompt_file = PromptFile(name=prompt_name, content=remote_content)
                            if self.save_prompt_file(prompt_file):
                                logger.info(f"Updated content for active branch '{branch_name}'")
                    
                    # Update index with remote version info
                    self.update_prompt_index_from_remote(prompt_name, branch_name, branch_content.get('content', ''), remote_version)
                    
                    result['branches_synced'] += 1
                    logger.info(f"✓ Synced branch '{branch_name}' for prompt '{prompt_name}' (origin/{branch_name})")
                    
                except Exception as e:
                    error_msg = f"Error syncing branch '{branch_name}': {e}"
                    result['errors'].append(error_msg)
                    logger.error(error_msg)
                    continue
            
            return result
            
        except Exception as e:
            error_msg = f"Error syncing branches for prompt '{prompt_name}': {e}"
            result['errors'].append(error_msg)
            logger.error(error_msg)
            return result

    def list_prompt_branches_with_state(self, prompt_name: str, include_remote: bool = False) -> List[Dict[str, Any]]:
        """List branches for a prompt with their local/remote state information"""
        try:
            branches = []
            current_state = self.get_current_prompt_state()
            current_branch = current_state.branch_name if (current_state and current_state.prompt_name == prompt_name) else None
            
            # Get local branches
            local_branches = self.list_local_prompt_branches(prompt_name)
            for branch_name in local_branches:
                commit_hash = ""
                branch_ref_file = self.refs_dir / prompt_name / 'heads' / branch_name
                if branch_ref_file.exists():
                    commit_hash = branch_ref_file.read_text().strip()[:8]
                
                # Determine branch state
                branch_state = self._get_branch_state(prompt_name, branch_name)
                tracking_branch = self.get_tracking_branch(prompt_name, branch_name)
                
                branch_info = {
                    'name': branch_name,
                    'type': 'local',
                    'commit_hash': commit_hash,
                    'is_current': branch_name == current_branch,
                    'state': branch_state,
                    'tracking_branch': tracking_branch,
                    'behind_remote': branch_state in ['remote', 'behind'],
                    'ahead_of_remote': branch_state in ['ahead'],
                    'has_local_changes': self._branch_has_local_changes(prompt_name, branch_name)
                }
                
                branches.append(branch_info)
            
            # Get remote branches if requested
            if include_remote:
                remote_branches = self.list_remote_prompt_branches(prompt_name)
                for remote_branch in remote_branches:
                    remote, branch_name = self.parse_remote_branch(remote_branch)
                    
                    # Check if there's a local branch tracking this remote branch
                    has_local_tracking = any(b['tracking_branch'] == remote_branch for b in branches)
                    
                    remote_ref_file = self.refs_dir / prompt_name / 'remotes' / remote / branch_name
                    commit_hash = ""
                    if remote_ref_file.exists():
                        commit_hash = remote_ref_file.read_text().strip()[:8]
                    
                    remote_info = {
                        'name': remote_branch,
                        'type': 'remote',
                        'commit_hash': commit_hash,
                        'is_current': False,
                        'state': 'remote',
                        'tracking_branch': None,
                        'has_local_tracking': has_local_tracking,
                        'behind_remote': False,
                        'ahead_of_remote': False,
                        'has_local_changes': False
                    }
                    
                    branches.append(remote_info)
            
            # Sort branches: current first, then local, then remote, then alphabetically
            def sort_key(b):
                return (
                    not b['is_current'],  # Current branch first
                    b['type'] == 'remote',  # Local branches before remote
                    b['name']  # Alphabetical
                )
            
            branches.sort(key=sort_key)
            return branches
            
        except Exception as e:
            logger.error(f"Error listing branches with state for '{prompt_name}': {e}")
            return []

    def fetch_remote_prompt_branches(self, client, prompt_name: str) -> List[Dict[str, Any]]:
        """Fetch all branches for a prompt from remote API"""
        try:
            # First get the prompt ID from the prompt name
            response = client.list_prompts(project_id=self.load_config().project_id)
            if not response.success:
                logger.error(f"Failed to fetch prompts: {response.error}")
                return []
            
            remote_prompts = response.data.get('prompts', [])
            target_prompt = None
            
            for prompt in remote_prompts:
                if prompt.get('name') == prompt_name:
                    target_prompt = prompt
                    break
            
            if not target_prompt:
                logger.error(f"Prompt '{prompt_name}' not found in remote")
                return []
            
            # Make direct API request to get branches for this prompt
            # This requires a new method in the core client
            prompt_id = target_prompt.get('id') or target_prompt.get('prompt_id')
            if not prompt_id:
                logger.error(f"No prompt ID found for '{prompt_name}'")
                return []
            
            # Use the direct API client to fetch branches
            headers = {'Authorization': f'Bearer {self.load_config().api_key}'}
            
            # Try to get user ID for the branches API (required by backend)
            user_response = requests.get(f"{self.load_config().base_url}/api/auth/cli-user", headers=headers)
            if user_response.status_code != 200:
                logger.error("Failed to authenticate for branch fetching")
                return []
            
            user_data = user_response.json()
            user_id = user_data.get('id')
            
            # Fetch branches for this prompt
            branches_url = f"{self.load_config().base_url}/api/branches/prompt/{prompt_id}"
            branches_response = requests.get(branches_url, headers=headers, params={'userId': user_id})
            
            if branches_response.status_code == 200:
                branches_data = branches_response.json()
                return branches_data if isinstance(branches_data, list) else []
            else:
                logger.error(f"Failed to fetch branches: {branches_response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching remote branches for '{prompt_name}': {e}")
            return []
        
    def fetch_remote_prompt_version_for_branch(self, client, prompt_name: str, branch_name: str) -> Optional[Dict[str, Any]]:
        """Fetch the latest version of a prompt from a specific branch"""
        try:
            # Use the existing get_prompt method but specify the branch
            from banyan.core import BanyanAPIClient
            if isinstance(client, BanyanAPIClient):
                response = client.get_prompt(prompt_name, branch=branch_name, project_id=self.load_config().project_id)
                if response.success:
                    return response.data
            else:
                # Legacy client support
                response = client.list_prompts(project_id=self.load_config().project_id, branch=branch_name)
                if response.success:
                    remote_prompts = response.data.get('prompts', [])
                    for prompt in remote_prompts:
                        if prompt.get('name') == prompt_name:
                            return prompt
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching prompt version for '{prompt_name}' from branch '{branch_name}': {e}")
            return None
        
    def _get_branch_state(self, prompt_name: str, branch_name: str) -> str:
        """Determine if a branch is local-only, remote-only, or synchronized"""
        try:
            # Check if we have remote tracking info
            remote_ref_file = self.refs_dir / prompt_name / 'remotes' / 'origin' / branch_name
            local_ref_file = self.refs_dir / prompt_name / 'heads' / branch_name
            
            local_exists = local_ref_file.exists()
            remote_exists = remote_ref_file.exists()
            
            if not local_exists and not remote_exists:
                return 'unknown'
            elif local_exists and not remote_exists:
                return 'local'  # Local-only branch, not pushed
            elif not local_exists and remote_exists:
                return 'remote'  # Remote branch not checked out locally
            else:
                # Both exist, compare commit hashes
                local_hash = local_ref_file.read_text().strip()
                remote_hash = remote_ref_file.read_text().strip()
                
                if local_hash == remote_hash:
                    return 'up-to-date'
                else:
                    # For now, assume local is ahead if different
                    # In a full implementation, you'd check commit ancestry
                    return 'ahead'
                    
        except Exception as e:
            logger.error(f"Error determining branch state for '{prompt_name}@{branch_name}': {e}")
            return 'unknown'
    
    def _branch_has_local_changes(self, prompt_name: str, branch_name: str) -> bool:
        """Check if a branch has uncommitted local changes"""
        try:
            # Check if current prompt file has changes vs last commit
            if not self.prompt_exists(prompt_name):
                return False
            
            # Get current content
            prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
            if not prompt_file_path.exists():
                return False
            
            current_content = prompt_file_path.read_text()
            current_hash = ContentHasher.hash_content(current_content)
            
            # Get last committed hash for this branch
            branch_ref_file = self.refs_dir / prompt_name / 'heads' / branch_name
            if not branch_ref_file.exists():
                return True  # No commits, so any content is a change
            
            last_commit_hash = branch_ref_file.read_text().strip()
            
            return current_hash != last_commit_hash
            
        except Exception as e:
            logger.error(f"Error checking local changes for '{prompt_name}@{branch_name}': {e}")
            return False

    # === Git-like Conflict Resolution and Version Control ===

    def detect_merge_conflicts(self, prompt_name: str, branch_name: str, local_content: str, remote_content: str) -> Optional[ConflictInfo]:
        """Detect if there are conflicts between local and remote content"""
        try:
            local_hash = ContentHasher.hash_content(local_content)
            remote_hash = ContentHasher.hash_content(remote_content)
            
            if local_hash != remote_hash:
                # Check if we have uncommitted local changes
                index = self.load_prompt_index(prompt_name, branch_name)
                staging_area = self.load_staging_area(prompt_name, branch_name)
                
                # If there are staged changes or the working directory differs from index, there's a conflict
                has_uncommitted_changes = (
                    len(staging_area) > 0 or 
                    (prompt_name in index and index[prompt_name].content_hash != ContentHasher.hash_content(local_content))
                )
                
                if has_uncommitted_changes:
                    return ConflictInfo(
                        name=prompt_name,
                        local_content=local_content,
                        remote_content=remote_content
                    )
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to detect merge conflicts: {e}")
            return None

    def check_remote_ahead(self, client, prompt_name: str, branch_name: str) -> Dict[str, Any]:
        """Check if remote branch is ahead of local branch"""
        try:
            # Get remote version info
            remote_content = self.fetch_remote_prompt_version_for_branch(client, prompt_name, branch_name)
            if not remote_content:
                return {'is_ahead': False, 'message': 'Remote branch not found'}
            
            # Get local latest version
            local_versions = self.load_prompt_local_versions(prompt_name, branch_name)
            if not local_versions:
                return {'is_ahead': True, 'message': 'No local versions, remote is ahead'}
            
            # Find the latest local version
            latest_local = max(local_versions, key=lambda v: float(v.version))
            remote_version = remote_content.get('version', '1.0')
            
            try:
                local_version_num = float(latest_local.version)
                remote_version_num = float(remote_version)
                
                if remote_version_num > local_version_num:
                    return {
                        'is_ahead': True,
                        'message': f'Remote is ahead (remote: {remote_version}, local: {latest_local.version})',
                        'local_version': latest_local.version,
                        'remote_version': remote_version
                    }
                elif remote_version_num < local_version_num:
                    return {
                        'is_ahead': False,
                        'message': f'Local is ahead (local: {latest_local.version}, remote: {remote_version})',
                        'local_version': latest_local.version,
                        'remote_version': remote_version
                    }
                else:
                    # Same version number, check content hash
                    local_hash = ContentHasher.hash_content(latest_local.content)
                    remote_hash = ContentHasher.hash_content(remote_content.get('content', ''))
                    
                    if local_hash != remote_hash:
                        return {
                            'is_ahead': True,
                            'message': 'Remote has different content at same version',
                            'local_version': latest_local.version,
                            'remote_version': remote_version
                        }
                    else:
                        return {
                            'is_ahead': False,
                            'message': 'Local and remote are synchronized',
                            'local_version': latest_local.version,
                            'remote_version': remote_version
                        }
            except (ValueError, TypeError):
                # Can't compare versions, assume remote is ahead
                return {
                    'is_ahead': True,
                    'message': 'Cannot compare version numbers',
                    'local_version': latest_local.version,
                    'remote_version': remote_version
                }
                
        except Exception as e:
            logger.error(f"Failed to check if remote is ahead: {e}")
            return {'is_ahead': False, 'message': f'Error checking remote: {e}'}

    def can_fast_forward(self, prompt_name: str, branch_name: str, remote_content: str) -> bool:
        """Check if we can fast-forward merge (no local uncommitted changes)"""
        try:
            # Check for staged changes
            staging_area = self.load_staging_area(prompt_name, branch_name)
            if staging_area:
                return False
            
            # Check for working directory changes
            prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
            if not prompt_file_path.exists():
                return True  # No local file, can fast-forward
            
            local_content = prompt_file_path.read_text()
            index = self.load_prompt_index(prompt_name, branch_name)
            
            if prompt_name in index:
                local_hash = ContentHasher.hash_content(local_content)
                if local_hash != index[prompt_name].content_hash:
                    return False  # Working directory has changes
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to check fast-forward possibility: {e}")
            return False

    def perform_merge(self, prompt_name: str, branch_name: str, local_content: str, remote_content: str, strategy: str = "auto") -> bool:
        """Perform merge between local and remote content"""
        try:
            if strategy == "auto":
                # Try to auto-merge if possible
                if local_content == remote_content:
                    return True  # Already merged
                
                # Check if we can fast-forward
                if self.can_fast_forward(prompt_name, branch_name, remote_content):
                    # Fast-forward: just update to remote content
                    prompt_file = PromptFile(name=prompt_name, content=remote_content)
                    return self.save_prompt_file(prompt_file)
                else:
                    # Create conflict for manual resolution
                    conflict = ConflictInfo(
                        name=prompt_name,
                        local_content=local_content,
                        remote_content=remote_content
                    )
                    self.add_prompt_conflict(prompt_name, branch_name, conflict)
                    self.create_conflict_file(conflict)
                    return False
            
            elif strategy == "ours":
                # Keep local version
                return True
            
            elif strategy == "theirs":
                # Take remote version
                prompt_file = PromptFile(name=prompt_name, content=remote_content)
                return self.save_prompt_file(prompt_file)
            
            else:
                logger.error(f"Unknown merge strategy: {strategy}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to perform merge: {e}")
            return False

    def validate_push_preconditions(self, client, prompt_name: str, branch_name: str) -> Dict[str, Any]:
        """Validate that we can push - similar to git push validation"""
        try:
            # Check if there are uncommitted changes
            staging_area = self.load_staging_area(prompt_name, branch_name)
            if staging_area:
                return {
                    'can_push': False,
                    'reason': 'uncommitted_changes',
                    'message': 'You have uncommitted changes. Please commit them before pushing.'
                }
            
            # Check if remote is ahead
            remote_check = self.check_remote_ahead(client, prompt_name, branch_name)
            if remote_check['is_ahead']:
                return {
                    'can_push': False,
                    'reason': 'remote_ahead',
                    'message': f"Remote branch is ahead. Please pull first. {remote_check['message']}"
                }
            
            # Check if there are unpushed commits
            unpushed_versions = self.get_unpushed_prompt_versions(prompt_name, branch_name)
            if not unpushed_versions:
                return {
                    'can_push': False,
                    'reason': 'nothing_to_push',
                    'message': 'Everything up-to-date'
                }
            
            return {
                'can_push': True,
                'unpushed_count': len(unpushed_versions),
                'message': f'Ready to push {len(unpushed_versions)} version(s)'
            }
            
        except Exception as e:
            logger.error(f"Failed to validate push preconditions: {e}")
            return {
                'can_push': False,
                'reason': 'error',
                'message': f'Error validating push: {e}'
            }

    def handle_pull_with_conflicts(self, client, prompt_name: str, branch_name: str, force: bool = False) -> Dict[str, Any]:
        """Handle pull operation with proper conflict detection and resolution"""
        try:
            # Fetch remote content
            remote_content_data = self.fetch_remote_prompt_version_for_branch(client, prompt_name, branch_name)
            if not remote_content_data:
                return {
                    'success': False,
                    'message': f'Remote branch {branch_name} not found'
                }
            
            remote_content = remote_content_data.get('content', '')
            remote_version = remote_content_data.get('version', '1.0')
            
            # Get local content
            local_file_path = self.prompts_dir / f"{prompt_name}.txt"
            local_content = local_file_path.read_text() if local_file_path.exists() else ''
            
            # If forced, just overwrite
            if force:
                prompt_file = PromptFile(name=prompt_name, content=remote_content)
                if self.save_prompt_file(prompt_file):
                    self.update_prompt_index_from_remote(prompt_name, branch_name, remote_content, remote_version)
                    return {
                        'success': True,
                        'message': f'Force pulled {prompt_name}',
                        'action': 'overwritten'
                    }
                else:
                    return {
                        'success': False,
                        'message': f'Failed to save {prompt_name}'
                    }
            
            # Check for conflicts
            conflict = self.detect_merge_conflicts(prompt_name, branch_name, local_content, remote_content)
            if conflict:
                # Add conflict and create conflict file
                self.add_prompt_conflict(prompt_name, branch_name, conflict)
                self.create_conflict_file(conflict)
                return {
                    'success': False,
                    'message': f'Merge conflict in {prompt_name}. Please resolve conflicts and try again.',
                    'action': 'conflict_created',
                    'conflict_file': f"{prompt_name}.txt"
                }
            
            # No conflicts, can merge safely
            if self.perform_merge(prompt_name, branch_name, local_content, remote_content, "auto"):
                self.update_prompt_index_from_remote(prompt_name, branch_name, remote_content, remote_version)
                return {
                    'success': True,
                    'message': f'Successfully pulled {prompt_name}',
                    'action': 'merged'
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to merge {prompt_name}'
                }
                
        except Exception as e:
            logger.error(f"Failed to handle pull with conflicts: {e}")
            return {
                'success': False,
                'message': f'Error during pull: {e}'
            }

    def is_conflict_resolved(self, prompt_name: str) -> bool:
        """Check if conflict markers have been resolved in the file"""
        try:
            prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
            if not prompt_file_path.exists():
                return True
            
            content = prompt_file_path.read_text()
            
            # Check for various Git-style conflict markers
            conflict_markers = [
                '<<<<<<< HEAD', '<<<<<<< LOCAL', '<<<<<<< current',
                '||||||| base', '||||||| merged common ancestors',
                '=======',
                '>>>>>>> REMOTE', '>>>>>>> source', '>>>>>>> incoming'
            ]
            
            for marker in conflict_markers:
                if marker in content:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to check if conflict is resolved: {e}")
            return False

    def has_unstaged_changes(self, prompt_name: str, branch_name: str) -> bool:
        """Check if there are unstaged changes in the working directory"""
        try:
            # Ensure index is initialized for this prompt@branch
            self.initialize_prompt_index_if_needed(prompt_name, branch_name)
            
            # Get current prompt file content
            prompt_file_path = self.prompts_dir / f"{prompt_name}.txt"
            if not prompt_file_path.exists():
                # If prompt file doesn't exist but there's an index entry, it's a deletion
                index = self.load_prompt_index(prompt_name, branch_name)
                return prompt_name in index
            
            current_content = prompt_file_path.read_text()
            current_hash = ContentHasher.hash_content(current_content)
            
            # Compare with index (last committed/staged state)
            index = self.load_prompt_index(prompt_name, branch_name)
            if prompt_name in index:
                index_entry = index[prompt_name]
                return current_hash != index_entry.content_hash
            else:
                # No index entry means this is a new untracked file
                return True
                
        except Exception as e:
            logger.error(f"Failed to check unstaged changes for {prompt_name}@{branch_name}: {e}")
            return False
    
    def has_staged_changes(self, prompt_name: str, branch_name: str) -> bool:
        """Check if there are staged changes ready for commit"""
        try:
            staging_area = self.load_staging_area(prompt_name, branch_name)
            return len(staging_area) > 0
        except Exception as e:
            logger.error(f"Failed to check staged changes for {prompt_name}@{branch_name}: {e}")
            return False

    # === Enhanced Git-like Merge System ===
    
    def load_merge_state(self, prompt_name: str, branch_name: str) -> Optional[MergeState]:
        """Load ongoing merge state for specific prompt@branch"""
        merge_state_file = self.banyan_dir / 'merge_state' / prompt_name / f"{branch_name}.json"
        if not merge_state_file.exists():
            return None
        
        try:
            with open(merge_state_file, 'r') as f:
                data = json.load(f)
            return MergeState(**data)
        except Exception as e:
            logger.error(f"Failed to load merge state for {prompt_name}@{branch_name}: {e}")
            return None
    
    def save_merge_state(self, prompt_name: str, branch_name: str, merge_state: MergeState) -> bool:
        """Save ongoing merge state for specific prompt@branch"""
        try:
            merge_state_dir = self.banyan_dir / 'merge_state' / prompt_name
            merge_state_dir.mkdir(parents=True, exist_ok=True)
            
            merge_state_file = merge_state_dir / f"{branch_name}.json"
            with open(merge_state_file, 'w') as f:
                json.dump(asdict(merge_state), f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save merge state for {prompt_name}@{branch_name}: {e}")
            return False
    
    def clear_merge_state(self, prompt_name: str, branch_name: str) -> bool:
        """Clear merge state after successful merge or abort"""
        try:
            merge_state_file = self.banyan_dir / 'merge_state' / prompt_name / f"{branch_name}.json"
            if merge_state_file.exists():
                merge_state_file.unlink()
            return True
        except Exception as e:
            logger.error(f"Failed to clear merge state for {prompt_name}@{branch_name}: {e}")
            return False
    
    def find_common_ancestor(self, prompt_name: str, branch1: str, branch2: str) -> Optional[str]:
        """Find the common ancestor commit between two branches (simplified version)"""
        try:
            # Load versions from both branches
            branch1_versions = self.load_prompt_local_versions(prompt_name, branch1)
            branch2_versions = self.load_prompt_local_versions(prompt_name, branch2)
            
            if not branch1_versions or not branch2_versions:
                return None
            
            # Create sets of commit hashes for fast lookup
            branch1_commits = {v.hash for v in branch1_versions}
            branch2_commits = {v.hash for v in branch2_versions}
            
            # Find common commits
            common_commits = branch1_commits.intersection(branch2_commits)
            if not common_commits:
                return None
            
            # For simplicity, return the most recent common commit
            # In a full implementation, we'd do proper ancestry traversal
            for version in sorted(branch1_versions, key=lambda v: v.metadata.get('timestamp', ''), reverse=True):
                if version.hash in common_commits:
                    return version.hash
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to find common ancestor for {prompt_name} between {branch1} and {branch2}: {e}")
            return None
    
    def get_branch_head_commit(self, prompt_name: str, branch_name: str) -> Optional[str]:
        """Get the latest commit hash for a branch"""
        try:
            versions = self.load_prompt_local_versions(prompt_name, branch_name)
            if not versions:
                return None
            
            # Return the most recent commit
            latest_version = max(versions, key=lambda v: v.metadata.get('timestamp', ''))
            return latest_version.hash
            
        except Exception as e:
            logger.error(f"Failed to get head commit for {prompt_name}@{branch_name}: {e}")
            return None
    
    def get_commit_content(self, prompt_name: str, branch_name: str, commit_hash: str) -> Optional[str]:
        """Get content for a specific commit"""
        try:
            versions = self.load_prompt_local_versions(prompt_name, branch_name)
            for version in versions:
                if version.hash == commit_hash:
                    return version.content
            
            # Also check other branches (commit might be reachable from multiple branches)
            for branch in self.list_prompt_branches(prompt_name, local_only=True):
                if branch != branch_name:
                    other_versions = self.load_prompt_local_versions(prompt_name, branch)
                    for version in other_versions:
                        if version.hash == commit_hash:
                            return version.content
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get commit content for {commit_hash}: {e}")
            return None
    
    def can_fast_forward_merge(self, prompt_name: str, source_branch: str, target_branch: str) -> bool:
        """Check if we can do a fast-forward merge (target is ancestor of source)"""
        try:
            source_head = self.get_branch_head_commit(prompt_name, source_branch)
            target_head = self.get_branch_head_commit(prompt_name, target_branch)
            
            if not source_head or not target_head:
                return False
            
            # Check if target branch head is an ancestor of source branch head
            # For simplicity, check if target head exists in source branch history
            source_versions = self.load_prompt_local_versions(prompt_name, source_branch)
            source_commit_hashes = {v.hash for v in source_versions}
            
            return target_head in source_commit_hashes
            
        except Exception as e:
            logger.error(f"Failed to check fast-forward possibility: {e}")
            return False
    
    def perform_three_way_merge(self, prompt_name: str, source_content: str, target_content: str, base_content: str) -> Dict[str, Any]:
        """Perform three-way merge between source, target, and base content"""
        try:
            # If all three are the same, no conflict
            if source_content == target_content == base_content:
                return {
                    'success': True,
                    'content': source_content,
                    'has_conflicts': False,
                    'merge_type': 'no_change'
                }
            
            # If source and target are the same, no conflict
            if source_content == target_content:
                return {
                    'success': True,
                    'content': source_content,
                    'has_conflicts': False,
                    'merge_type': 'identical'
                }
            
            # If source is same as base, take target (target changed, source didn't)
            if source_content == base_content:
                return {
                    'success': True,
                    'content': target_content,
                    'has_conflicts': False,
                    'merge_type': 'target_only_changed'
                }
            
            # If target is same as base, take source (source changed, target didn't)
            if target_content == base_content:
                return {
                    'success': True,
                    'content': source_content,
                    'has_conflicts': False,
                    'merge_type': 'source_only_changed'
                }
            
            # Both branches changed differently - this is a conflict
            # For text content, we'll create conflict markers
            conflict_content = self._generate_three_way_conflict_markers(
                source_content, target_content, base_content
            )
            
            return {
                'success': False,
                'content': conflict_content,
                'has_conflicts': True,
                'merge_type': 'conflict',
                'conflict_info': {
                    'source_content': source_content,
                    'target_content': target_content,
                    'base_content': base_content
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to perform three-way merge: {e}")
            return {
                'success': False,
                'content': '',
                'has_conflicts': True,
                'merge_type': 'error',
                'error': str(e)
            }
    
    def _generate_three_way_conflict_markers(self, source_content: str, target_content: str, base_content: str) -> str:
        """Generate Git-style conflict markers with base content"""
        lines = []
        lines.append("<<<<<<< HEAD (current branch)")
        lines.append(target_content)
        lines.append("||||||| base")
        lines.append(base_content)
        lines.append("=======")
        lines.append(source_content)
        lines.append(">>>>>>> source branch")
        return "\n".join(lines)
    
    def start_merge(
        self, 
        prompt_name: str, 
        target_branch: str, 
        source_branch: str, 
        strategy: str = "auto",
        no_commit: bool = False
    ) -> Dict[str, Any]:
        """Start a Git-like merge operation"""
        try:
            # Check if already in a merge
            existing_merge_state = self.load_merge_state(prompt_name, target_branch)
            if existing_merge_state:
                return {
                    'success': False,
                    'error': 'Already in a merge. Complete or abort current merge first.',
                    'merge_in_progress': True
                }
            
            # Check if branches exist
            if not self.prompt_branch_exists(prompt_name, source_branch):
                return {
                    'success': False,
                    'error': f"Source branch '{source_branch}' does not exist"
                }
            
            if not self.prompt_branch_exists(prompt_name, target_branch):
                return {
                    'success': False,
                    'error': f"Target branch '{target_branch}' does not exist"
                }
            
            # Get commit heads
            source_head = self.get_branch_head_commit(prompt_name, source_branch)
            target_head = self.get_branch_head_commit(prompt_name, target_branch)
            
            if not source_head or not target_head:
                return {
                    'success': False,
                    'error': 'One or both branches have no commits'
                }
            
            # Check if already up to date
            if source_head == target_head:
                return {
                    'success': True,
                    'merge_type': 'up_to_date',
                    'message': 'Already up to date.'
                }
            
            # Check for fast-forward merge
            if self.can_fast_forward_merge(prompt_name, source_branch, target_branch):
                return self._perform_fast_forward_merge(
                    prompt_name, target_branch, source_branch, source_head, no_commit
                )
            
            # Find common ancestor
            base_commit = self.find_common_ancestor(prompt_name, source_branch, target_branch)
            
            # Get content from all three points
            source_content = self.get_commit_content(prompt_name, source_branch, source_head) or ""
            target_content = self.get_commit_content(prompt_name, target_branch, target_head) or ""
            base_content = ""
            
            if base_commit:
                base_content = self.get_commit_content(prompt_name, target_branch, base_commit) or ""
            
            # Perform three-way merge
            merge_result = self.perform_three_way_merge(prompt_name, source_content, target_content, base_content)
            
            # Create merge state
            merge_state = MergeState(
                source_branch=source_branch,
                target_branch=target_branch,
                source_commit_hash=source_head,
                target_commit_hash=target_head,
                base_commit_hash=base_commit,
                merge_strategy=strategy,
                merge_message=f"Merge branch '{source_branch}' into {target_branch}"
            )
            
            if merge_result['has_conflicts']:
                # Save conflict information
                conflict = ConflictInfo(
                    name=prompt_name,
                    local_content=target_content,
                    remote_content=source_content,
                    base_content=base_content
                )
                
                self.add_prompt_conflict(prompt_name, target_branch, conflict)
                self.save_merge_state(prompt_name, target_branch, merge_state)
                
                # Create conflict file with markers
                prompt_file = PromptFile(name=prompt_name, content=merge_result['content'])
                self.save_prompt_file(prompt_file)
                
                return {
                    'success': True,  # Changed to True because merge started successfully
                    'merge_type': 'conflict',
                    'has_conflicts': True,
                    'conflict_files': [prompt_name],
                    'message': f"Automatic merge failed; fix conflicts and then commit the result."
                }
            else:
                # Successful automatic merge
                if not no_commit:
                    # Stage and commit the merge
                    self.stage_prompt_content(prompt_name, merge_result['content'], "modified")
                    
                    # Create merge commit with multiple parents
                    staging_area = self.load_staging_area(prompt_name, target_branch)
                    merge_commit = self._create_merge_commit(
                        staging_area, merge_state, target_head, source_head
                    )
                    
                    if merge_commit:
                        self.clear_staging_area(prompt_name, target_branch)
                        return {
                            'success': True,
                            'merge_type': 'merge_commit',
                            'commit_hash': merge_commit.hash,
                            'message': f"Merge made by the '{strategy}' strategy."
                        }
                    else:
                        return {
                            'success': False,
                            'error': 'Failed to create merge commit'
                        }
                else:
                    # Stage for manual commit
                    self.stage_prompt_content(prompt_name, merge_result['content'], "modified")
                    self.save_merge_state(prompt_name, target_branch, merge_state)
                    
                    return {
                        'success': True,
                        'merge_type': 'staged',
                        'message': 'Automatic merge successful; staged for commit.'
                    }
                    
        except Exception as e:
            logger.error(f"Failed to start merge: {e}")
            return {
                'success': False,
                'error': f'Error starting merge: {e}'
            }
    
    def _perform_fast_forward_merge(
        self, 
        prompt_name: str, 
        target_branch: str, 
        source_branch: str, 
        source_head: str,
        no_commit: bool = False
    ) -> Dict[str, Any]:
        """Perform a fast-forward merge"""
        try:
            # Get source content
            source_content = self.get_commit_content(prompt_name, source_branch, source_head) or ""
            
            # Update prompt file
            prompt_file = PromptFile(name=prompt_name, content=source_content)
            self.save_prompt_file(prompt_file)
            
            # Update target branch reference to point to source head
            self.update_prompt_branch_ref(prompt_name, target_branch, source_head)
            
            # Update index
            self.update_prompt_index_entry(prompt_file, prompt_name, target_branch)
            
            return {
                'success': True,
                'merge_type': 'fast_forward',
                'commit_hash': source_head,
                'message': 'Fast-forward'
            }
            
        except Exception as e:
            logger.error(f"Failed to perform fast-forward merge: {e}")
            return {
                'success': False,
                'error': f'Fast-forward merge failed: {e}'
            }
    
    def _create_merge_commit(
        self, 
        staging_area: List[StagedFile], 
        merge_state: MergeState,
        target_parent: str,
        source_parent: str
    ) -> Optional[LocalVersion]:
        """Create a merge commit with multiple parents"""
        try:
            if not staging_area:
                return None
            
            staged_file = staging_area[0]  # Should only be one file
            
            # Auto-generate metadata
            metadata = {
                "created_by": "banyan-cli-merge",
                "file_path": f"{staged_file.name}.txt",
                "operation": "merge",
                "timestamp": datetime.now().isoformat(),
                "merge_type": "three_way"
            }
            
            # Get config for author info
            config = self.load_config()
            if config.author_name:
                metadata["author_name"] = config.author_name
            if config.author_email:
                metadata["author_email"] = config.author_email
            
            # Find highest version for this prompt and branch
            local_versions = self.load_prompt_local_versions(staged_file.name, merge_state.target_branch)
            
            highest_version = 1.0
            for existing_version in local_versions:
                try:
                    version_num = float(existing_version.version)
                    if version_num >= highest_version:
                        highest_version = version_num
                except (ValueError, TypeError):
                    continue
            
            # Increment version for new commit
            if highest_version >= 1.0:
                highest_version += 0.1
            
            # Create merge commit with multiple parents
            merge_commit = LocalVersion(
                name=staged_file.name,
                content=staged_file.content,
                branch=merge_state.target_branch,
                version=f"{highest_version:.1f}",
                metadata=metadata,
                message=merge_state.merge_message,
                parent_hash=target_parent,  # Primary parent (target branch)
                merge_parents=[source_parent]  # Additional parents (source branch)
            )
            
            # Save the new version
            local_versions.append(merge_commit)
            self.save_prompt_local_versions(staged_file.name, merge_state.target_branch, local_versions)
            
            # Update branch reference
            self.update_prompt_branch_ref(staged_file.name, merge_state.target_branch, merge_commit.hash)
            
            return merge_commit
            
        except Exception as e:
            logger.error(f"Failed to create merge commit: {e}")
            return None
    
    def abort_merge(self, prompt_name: str, branch_name: str) -> Dict[str, Any]:
        """Abort an ongoing merge and restore previous state"""
        try:
            # Load merge state
            merge_state = self.load_merge_state(prompt_name, branch_name)
            if not merge_state:
                return {
                    'success': False,
                    'error': 'No merge in progress'
                }
            
            # Clear conflicts
            conflicts = self.load_prompt_conflicts(prompt_name, branch_name)
            if conflicts:
                # Restore original content from target branch
                target_content = self.get_commit_content(
                    prompt_name, branch_name, merge_state.target_commit_hash
                ) or ""
                
                prompt_file = PromptFile(name=prompt_name, content=target_content)
                self.save_prompt_file(prompt_file)
                
                # Clear conflict tracking
                self.save_prompt_conflicts(prompt_name, branch_name, [])
            
            # Clear staging area
            self.clear_staging_area(prompt_name, branch_name)
            
            # Clear merge state
            self.clear_merge_state(prompt_name, branch_name)
            
            return {
                'success': True,
                'message': 'Merge aborted'
            }
            
        except Exception as e:
            logger.error(f"Failed to abort merge: {e}")
            return {
                'success': False,
                'error': f'Failed to abort merge: {e}'
            }
    
    def complete_merge(self, prompt_name: str, branch_name: str, commit_message: Optional[str] = None) -> Dict[str, Any]:
        """Complete a merge after conflicts have been resolved"""
        try:
            # Load merge state
            merge_state = self.load_merge_state(prompt_name, branch_name)
            if not merge_state:
                return {
                    'success': False,
                    'error': 'No merge in progress'
                }
            
            # Check if there are still unresolved conflicts
            conflicts = self.load_prompt_conflicts(prompt_name, branch_name)
            if conflicts:
                return {
                    'success': False,
                    'error': 'You have unresolved merge conflicts. Please resolve them before completing the merge.'
                }
            
            # Check if changes are staged
            staging_area = self.load_staging_area(prompt_name, branch_name)
            if not staging_area:
                return {
                    'success': False,
                    'error': 'No changes staged for commit. Please stage your resolved changes.'
                }
            
            # Use provided commit message or default merge message
            if commit_message:
                merge_state.merge_message = commit_message
            
            # Create merge commit
            merge_commit = self._create_merge_commit(
                staging_area, merge_state, 
                merge_state.target_commit_hash, 
                merge_state.source_commit_hash
            )
            
            if not merge_commit:
                return {
                    'success': False,
                    'error': 'Failed to create merge commit'
                }
            
            # Clear staging area and merge state
            self.clear_staging_area(prompt_name, branch_name)
            self.clear_merge_state(prompt_name, branch_name)
            
            return {
                'success': True,
                'commit_hash': merge_commit.hash,
                'message': f"[{branch_name} {merge_commit.hash}] {merge_state.merge_message}"
            }
            
        except Exception as e:
            logger.error(f"Failed to complete merge: {e}")
            return {
                'success': False,
                'error': f'Failed to complete merge: {e}'
            }

class PromptDiffer:
    """Utility for comparing prompts and showing differences with full integrity"""
    
    @staticmethod
    def content_hash(content: str) -> str:
        """Generate full SHA-256 hash for prompt content"""
        return ContentHasher.hash_content(content)
    
    @staticmethod
    def compare_prompts(local: PromptFile, remote: Dict[str, Any]) -> Dict[str, Any]:
        """Compare local and remote prompt versions with integrity verification"""
        local_hash = local.content_hash()  # Use the PromptFile's hash method
        remote_content = remote.get('content', '')
        remote_hash = PromptDiffer.content_hash(remote_content)
        
        # Verify local content integrity
        local_integrity_ok = local.verify_integrity()
        
        return {
            'name': local.name,
            'local_version': getattr(local, 'version', 'unknown'),
            'remote_version': remote.get('version'),
            'local_hash': local_hash,
            'remote_hash': remote_hash,
            'local_short_hash': local_hash[:12],
            'remote_short_hash': remote_hash[:12],
            'content_differs': local_hash != remote_hash,
            'branch_differs': getattr(local, 'branch', 'main') != remote.get('branch', 'main'),
            'metadata_differs': getattr(local, 'metadata', {}) != remote.get('metadata', {}),
            'local_integrity_ok': local_integrity_ok,
            'content_size_local': len(local.content),
            'content_size_remote': len(remote_content)
        }
    
    @staticmethod
    def format_diff_summary(diffs: List[Dict[str, Any]]) -> str:
        """Format a summary of differences"""
        if not diffs:
            return "No prompts to compare"
        
        lines = ["Prompt Status Summary:", "=" * 50]
        
        for diff in diffs:
            name = diff['name']
            status = []
            
            if diff['content_differs']:
                status.append("content changed")
            if diff['branch_differs']:
                status.append("branch differs")
            if diff['metadata_differs']:
                status.append("metadata differs")
            
            if not status:
                status.append("up to date")
            
            lines.append(f"  {name}: {', '.join(status)}")
        
        return "\n".join(lines)

def validate_prompt_name(name: str) -> Tuple[bool, str]:
    """Validate prompt name format"""
    if not name:
        return False, "Prompt name cannot be empty"
    
    if not name.replace('-', '').replace('_', '').isalnum():
        return False, "Prompt name must contain only letters, numbers, hyphens, and underscores"
    
    if len(name) > 100:
        return False, "Prompt name must be 100 characters or less"
    
    return True, ""

def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    return api_key and api_key.startswith('psk_') and len(api_key) > 10

def validate_project_id(project_id: str) -> bool:
    return len(project_id) == 36 and project_id.count('-') == 4

def get_editor_command() -> str:
    """Get the preferred editor command"""
    return os.environ.get('EDITOR', 'nano')

def open_in_editor(file_path: str) -> bool:
    """Open file in user's preferred editor"""
    try:
        editor = get_editor_command()
        os.system(f"{editor} {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to open editor: {e}")
        return False