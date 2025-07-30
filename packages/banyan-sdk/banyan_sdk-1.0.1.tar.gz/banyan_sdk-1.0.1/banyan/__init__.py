"""
Banyan SDK

A client SDK for logging real-world prompt usage to Banyan
and fetching prompts directly from the platform.

This module provides backward compatibility with the original API while using
the new refactored architecture:
- core.py: Low-level REST/API methods
- sdk.py: Runtime methods for applications
- cli.py: Git-like CLI interface
- cli_utils.py: CLI helper functions
"""

# Version
__version__ = "1.0.1"

# Import from refactored modules for backward compatibility
from .sdk import (
    PromptStackLogger,
    PromptData,
    ExperimentData,
    LogEntry,
    configure,
    get_prompt,
    experiment,
    log_prompt,
    flush,
    get_stats,
    shutdown,
    log,  # Alias for log_prompt
)

# Also expose core components for advanced usage
from .core import BanyanAPIClient, APIResponse
from .cli_utils import BanyanProjectManager, BanyanConfig, PromptFile


from .integrity import (
    ContentHasher,
    AtomicFileOperations,
    IntegrityError,
    IntegrityManager,
    get_integrity_manager
)
from .storage import (
    StorageManager,
    DeltaCompressor,
    ContentStore
)

# Keep all existing imports for full backward compatibility
import asyncio
import json
import time
import threading
import hashlib
from queue import Queue, Empty
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass
import requests
import logging

# Configure logging for backward compatibility
logger = logging.getLogger(__name__)

# All classes and functions are now imported from refactored modules above
# This file maintains backward compatibility while using the new architecture

__all__ = [
    # Main classes
    'PromptStackLogger',
    'PromptData', 
    'ExperimentData',
    'LogEntry',
    
    # Global functions
    'configure',
    'get_prompt',
    'experiment', 
    'log_prompt',
    'log',  # Alias
    'flush',
    'get_stats',
    'shutdown',
    
    # Core components
    'BanyanAPIClient',
    'APIResponse',
    
    # CLI components  
    'BanyanProjectManager',
    'BanyanConfig',
    'PromptFile',
    
    # Production-ready features
    'ContentHasher',
    'AtomicFileOperations', 
    'IntegrityError',
    'IntegrityManager',
    'get_integrity_manager',
    'StorageManager',
    'DeltaCompressor',
    'ContentStore',
    
    # Version
    '__version__'
] 