"""
Banyan SDK - Production-ready Runtime Methods

This module provides production-ready runtime methods for applications to interact with
Banyan prompts, experiments, and logging. Features include:
- Advanced experiment management with A/B testing
- Robust error handling and retry logic  
- Configurable logging controls
- Performance monitoring and metrics
- Seamless integration with CLI workflows
"""

import asyncio
import json
import time
import threading
import hashlib
import uuid
from queue import Queue, Empty
from typing import Optional, Dict, Any, Union, List, Callable
from dataclasses import dataclass, field
import logging
from datetime import datetime, timedelta
import os

from .core import BanyanAPIClient, APIResponse

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class LogEntry:
    """Represents a single prompt log entry"""
    prompt_id: Optional[str]
    prompt_name: Optional[str]
    version: Optional[str]
    branch_name: Optional[str]
    input: str
    output: str
    model: Optional[str]
    metadata: Dict[str, Any]
    duration_ms: Optional[int]
    timestamp: float
    experiment_id: Optional[str] = None
    experiment_version_id: Optional[str] = None
    sticky_key: Optional[str] = None
    sticky_value: Optional[str] = None

@dataclass 
class PromptData:
    """Represents a prompt fetched from the platform"""
    prompt_id: str
    name: str
    content: str
    version: str
    branch: str
    project: str
    enable_logging: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExperimentData:
    """Represents an experiment configuration"""
    experiment_id: str
    name: str
    prompt_id: str
    status: str
    sticky_type: str
    versions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceMetrics:
    """Performance and usage metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_latency_ms: float = 0.0
    total_latency_ms: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    last_reset: datetime = field(default_factory=datetime.now)

class BanyanCache:
    """Thread-safe cache for prompts and experiments"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self.ttl_seconds:
                    return value
                else:
                    del self._cache[key]
            return None
    
    def set(self, key: str, value: Any):
        with self._lock:
            self._cache[key] = (value, time.time())
    
    def clear(self):
        with self._lock:
            self._cache.clear()
    
    def size(self) -> int:
        with self._lock:
            return len(self._cache)

class PromptStackLogger:
    """
    Production-ready client for Banyan prompt management and logging
    
    Features:
    - Advanced experiment management with A/B testing
    - Robust error handling and retry logic
    - Configurable logging controls and batching
    - Performance monitoring and caching
    - Thread-safe operations
    - Graceful degradation
    """
    
    def __init__(
        self, 
        api_key: str, 
        base_url: str = "https://app.usebanyan.com",
        project_id: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        queue_size: int = 1000,
        flush_interval: float = 5.0,
        background_thread: bool = True,
        cache_ttl: int = 300,
        enable_metrics: bool = True,
        auto_flush: bool = True,
        batch_size: int = 10
    ):
        """
        Initialize the Banyan client
        
        Args:
            api_key: Your Banyan API key
            base_url: Base URL of your Banyan instance
            project_id: Optional project ID for project-bound API keys
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries (exponential backoff)
            queue_size: Maximum size of the local log queue
            flush_interval: How often to flush queued logs (seconds)
            background_thread: Whether to process logs in background thread
            cache_ttl: Cache time-to-live in seconds
            enable_metrics: Whether to collect performance metrics
            auto_flush: Whether to automatically flush logs
            batch_size: Number of logs to batch together
        """
        # Initialize core API client
        self.api_client = BanyanAPIClient(
            api_key=api_key,
            base_url=base_url,
            project_id=project_id,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        
        # Configuration
        self.batch_size = batch_size
        self.enable_metrics = enable_metrics
        self.auto_flush = auto_flush
        
        # Thread-safe components
        self.log_queue = Queue(maxsize=queue_size)
        self.background_thread_enabled = background_thread
        self.background_thread = None
        self.shutdown_event = threading.Event()
        self._lock = threading.Lock()
        
        # Caching
        self._cache = BanyanCache(ttl_seconds=cache_ttl)
        
        # Performance metrics
        self.metrics = PerformanceMetrics() if enable_metrics else None
        
        # Error handling
        self._error_callback: Optional[Callable[[Exception], None]] = None
        self._warning_callback: Optional[Callable[[str], None]] = None
        
        # Start background thread if enabled
        if background_thread:
            self._start_background_thread(flush_interval)
        
        # Validate connection on initialization
        self._validate_connection()
    
    def _validate_connection(self):
        """Validate API connection during initialization"""
        try:
            response = self.api_client.validate_api_key()
            if not response.success:
                if self._error_callback:
                    self._error_callback(Exception(f"API key validation failed: {response.error}"))
                else:
                    logger.error(f"API key validation failed: {response.error}")
        except Exception as e:
            if self._error_callback:
                self._error_callback(e)
            else:
                logger.error(f"Connection validation failed: {e}")
    
    def set_error_callback(self, callback: Callable[[Exception], None]):
        """Set callback for error handling"""
        self._error_callback = callback
    
    def set_warning_callback(self, callback: Callable[[str], None]):
        """Set callback for warning handling"""
        self._warning_callback = callback
    
    def _start_background_thread(self, flush_interval: float):
        """Start background thread for processing logs"""
        def background_worker():
            batch = []
            last_flush = time.time()
            
            while not self.shutdown_event.is_set():
                try:
                    # Try to get logs from queue
                    try:
                        log_entry = self.log_queue.get(timeout=1.0)
                        batch.append(log_entry)
                    except Empty:
                        pass
                    
                    # Flush if batch is full or interval exceeded
                    current_time = time.time()
                    should_flush = (
                        len(batch) >= self.batch_size or
                        (batch and current_time - last_flush >= flush_interval)
                    )
                    
                    if should_flush and batch:
                        self._flush_batch(batch)
                        batch.clear()
                        last_flush = current_time
                        
                except Exception as e:
                    if self._error_callback:
                        self._error_callback(e)
                    else:
                        logger.error(f"Background thread error: {e}")
            
            # Flush remaining logs on shutdown
            if batch:
                self._flush_batch(batch)
        
        self.background_thread = threading.Thread(target=background_worker, daemon=True)
        self.background_thread.start()
    
    def _flush_batch(self, batch: List[LogEntry]):
        """Flush a batch of log entries"""
        start_time = time.time()
        
        for log_entry in batch:
            try:
                response = self.api_client.log_prompt_usage(
                    prompt_id=log_entry.prompt_id,
                    prompt_name=log_entry.prompt_name,
                    version=log_entry.version,
                    branch_name=log_entry.branch_name,
                    input_text=log_entry.input,
                    output_text=log_entry.output,
                    model=log_entry.model,
                    metadata=log_entry.metadata,
                    duration_ms=log_entry.duration_ms,
                    experiment_id=log_entry.experiment_id,
                    experiment_version_id=log_entry.experiment_version_id,
                    sticky_key=log_entry.sticky_key,
                    sticky_value=log_entry.sticky_value
                )
                
                if self.metrics:
                    if response.success:
                        self.metrics.successful_requests += 1
                    else:
                        self.metrics.failed_requests += 1
                        if self._warning_callback:
                            self._warning_callback(f"Failed to log prompt usage: {response.error}")
                
            except Exception as e:
                if self.metrics:
                    self.metrics.failed_requests += 1
                if self._error_callback:
                    self._error_callback(e)
                else:
                    logger.error(f"Error flushing log entry: {e}")
        
        # Update metrics
        if self.metrics:
            self.metrics.total_requests += len(batch)
            duration_ms = int((time.time() - start_time) * 1000)
            self.metrics.total_latency_ms += duration_ms
            if self.metrics.total_requests > 0:
                self.metrics.avg_latency_ms = self.metrics.total_latency_ms / self.metrics.total_requests
    
    def get_prompt(
        self,
        name: str,
        version: Optional[str] = None,
        branch: str = "main",
        use_cache: bool = True
    ) -> Optional[PromptData]:
        """
        Fetch a prompt by name with caching support
        
        Args:
            name: Prompt name
            version: Specific version (optional, uses latest if not specified)
            branch: Branch name
            use_cache: Whether to use cache
        
        Returns:
            PromptData if found, None otherwise
        """
        start_time = time.time()
        cache_key = f"prompt:{name}:{version or 'latest'}:{branch}"
        
        # Check cache first
        if use_cache:
            cached_result = self._cache.get(cache_key)
            if cached_result:
                if self.metrics:
                    self.metrics.cache_hits += 1
                return cached_result
        
        if self.metrics:
            self.metrics.cache_misses += 1
        
        try:
            response = self.api_client.get_prompt(
                name=name,
                version=version,
                branch=branch,
                project_id=self.api_client.project_id
            )
            
            if response.success and response.data:
                prompt_data = PromptData(
                    prompt_id=response.data.get('prompt_id', ''),
                    name=response.data.get('name', name),
                    content=response.data.get('content', ''),
                    version=response.data.get('version', version or '1.0'),
                    branch=response.data.get('branch', branch),
                    project=response.data.get('project', ''),
                    enable_logging=response.data.get('enable_logging', True),
                    metadata=response.data.get('metadata', {})
                )
                
                # Cache the result
                if use_cache:
                    self._cache.set(cache_key, prompt_data)
                
                return prompt_data
            else:
                if self._warning_callback:
                    self._warning_callback(f"Prompt not found: {name}")
                return None
                
        except Exception as e:
            if self._error_callback:
                self._error_callback(e)
            else:
                logger.error(f"Error fetching prompt {name}: {e}")
            return None
        finally:
            if self.metrics:
                duration_ms = int((time.time() - start_time) * 1000)
                self.metrics.total_latency_ms += duration_ms
                self.metrics.total_requests += 1
                self.metrics.avg_latency_ms = self.metrics.total_latency_ms / self.metrics.total_requests
    
    def experiment(
        self,
        experiment_id: str,
        sticky_key: str,
        sticky_value: str,
        use_cache: bool = True
    ) -> Optional[PromptData]:
        """
        Route request through experiment and return appropriate prompt version
        
        Args:
            experiment_id: Experiment ID
            sticky_key: Key for sticky routing (e.g., 'user_id')
            sticky_value: Value for sticky routing (e.g., actual user ID)
            use_cache: Whether to use cache
        
        Returns:
            PromptData for the selected experiment version
        """
        start_time = time.time()
        cache_key = f"experiment:{experiment_id}:{sticky_key}:{sticky_value}"
        
        # Check cache first
        if use_cache:
            cached_result = self._cache.get(cache_key)
            if cached_result:
                if self.metrics:
                    self.metrics.cache_hits += 1
                return cached_result
        
        if self.metrics:
            self.metrics.cache_misses += 1
        
        try:
            response = self.api_client.route_experiment(
                experiment_id=experiment_id,
                sticky_key=sticky_key,
                sticky_value=sticky_value
            )
            
            if response.success and response.data:
                routing_data = response.data
                
                # Get the selected prompt version
                if 'prompt' in routing_data:
                    prompt_info = routing_data['prompt']
                    prompt_data = PromptData(
                        prompt_id=prompt_info.get('prompt_id', ''),
                        name=prompt_info.get('name', ''),
                        content=prompt_info.get('content', ''),
                        version=prompt_info.get('version', '1.0'),
                        branch=prompt_info.get('branch', 'main'),
                        project=prompt_info.get('project', ''),
                        enable_logging=prompt_info.get('enable_logging', True),
                        metadata={
                            'experiment_id': experiment_id,
                            'experiment_version_id': routing_data.get('selected_version_id'),
                            'sticky_key': sticky_key,
                            'sticky_value': sticky_value,
                            **prompt_info.get('metadata', {})
                        }
                    )
                    
                    # Cache the result
                    if use_cache:
                        self._cache.set(cache_key, prompt_data)
                    
                    return prompt_data
            
            if self._warning_callback:
                self._warning_callback(f"Experiment routing failed: {experiment_id}")
            return None
            
        except Exception as e:
            if self._error_callback:
                self._error_callback(e)
            else:
                logger.error(f"Error routing experiment {experiment_id}: {e}")
            return None
        finally:
            if self.metrics:
                duration_ms = int((time.time() - start_time) * 1000)
                self.metrics.total_latency_ms += duration_ms
                self.metrics.total_requests += 1
                self.metrics.avg_latency_ms = self.metrics.total_latency_ms / self.metrics.total_requests
    
    def log_prompt(
        self,
        input: str,
        output: str,
        prompt_data: Optional[PromptData] = None,
        prompt_id: Optional[str] = None,
        prompt_name: Optional[str] = None,
        version: Optional[str] = None,
        branch_name: Optional[str] = None,
        model: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[int] = None,
        blocking: bool = False
    ) -> bool:
        """
        Log a prompt execution
        
        Args:
            input: The input text sent to the model
            output: The output text received from the model
            prompt_data: PromptData object from get_prompt() (preferred method)
            prompt_id: ID of the prompt (optional)
            prompt_name: Name of the prompt (optional)
            version: Version of the prompt used (optional)
            branch_name: Branch name of the prompt (optional)
            model: Name of the model used (optional)
            metadata: Additional metadata (user_id, session_id, etc.)
            duration_ms: Execution time in milliseconds (optional)
            blocking: If True, send immediately and block until complete
            
        Returns:
            bool: True if successfully queued/sent, False otherwise
        """
        if not input or not output:
            if self._warning_callback:
                self._warning_callback("Cannot log prompt with empty input or output")
            return False
        
        # Extract information from prompt_data if provided
        if prompt_data:
            prompt_id = prompt_data.prompt_id
            prompt_name = prompt_data.name
            version = prompt_data.version
            branch_name = prompt_data.branch
            
            # Check if logging is enabled for this prompt
            if not prompt_data.enable_logging:
                return True  # Silently skip logging but return success
            
            # Merge metadata
            combined_metadata = {**prompt_data.metadata, **(metadata or {})}
            
            # Extract experiment info from metadata
            experiment_id = combined_metadata.get('experiment_id')
            experiment_version_id = combined_metadata.get('experiment_version_id') 
            sticky_key = combined_metadata.get('sticky_key')
            sticky_value = combined_metadata.get('sticky_value')
        else:
            combined_metadata = metadata or {}
            experiment_id = None
            experiment_version_id = None
            sticky_key = None
            sticky_value = None
        
        # Create log entry
        log_entry = LogEntry(
            prompt_id=prompt_id,
            prompt_name=prompt_name,
            version=version,
            branch_name=branch_name,
            input=input,
            output=output,
            model=model,
            metadata=combined_metadata,
            duration_ms=duration_ms,
            timestamp=time.time(),
            experiment_id=experiment_id,
            experiment_version_id=experiment_version_id,
            sticky_key=sticky_key,
            sticky_value=sticky_value
        )
        
        if blocking:
            # Send immediately
            try:
                self._flush_batch([log_entry])
                return True
            except Exception as e:
                if self._error_callback:
                    self._error_callback(e)
                return False
        else:
            # Queue for background processing
            try:
                self.log_queue.put_nowait(log_entry)
                return True
            except Exception as e:
                if self._error_callback:
                    self._error_callback(e)
                return False
    
    def flush(self, timeout: float = 30.0) -> bool:
        """Flush all queued logs"""
        if not self.auto_flush:
            return True
        
        start_time = time.time()
        batch = []
        
        # Collect all queued logs
        while not self.log_queue.empty() and time.time() - start_time < timeout:
            try:
                log_entry = self.log_queue.get_nowait()
                batch.append(log_entry)
            except Empty:
                break
        
        if batch:
            try:
                self._flush_batch(batch)
                return True
            except Exception as e:
                if self._error_callback:
                    self._error_callback(e)
                return False
        
        return True
    
    def get_metrics(self) -> Optional[PerformanceMetrics]:
        """Get performance metrics"""
        return self.metrics
    
    def reset_metrics(self):
        """Reset performance metrics"""
        if self.metrics:
            self.metrics = PerformanceMetrics()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get logging statistics"""
        stats = {
            'queue_size': self.log_queue.qsize(),
            'cache_size': self._cache.size(),
            'background_thread_running': self.background_thread.is_alive() if self.background_thread else False
        }
        
        if self.metrics:
            stats.update({
                'total_requests': self.metrics.total_requests,
                'successful_requests': self.metrics.successful_requests,
                'failed_requests': self.metrics.failed_requests,
                'avg_latency_ms': self.metrics.avg_latency_ms,
                'cache_hits': self.metrics.cache_hits,
                'cache_misses': self.metrics.cache_misses,
                'cache_hit_rate': self.metrics.cache_hits / (self.metrics.cache_hits + self.metrics.cache_misses) if (self.metrics.cache_hits + self.metrics.cache_misses) > 0 else 0
            })
        
        return stats
    
    def clear_cache(self):
        """Clear the prompt cache"""
        self._cache.clear()
    
    def shutdown(self, timeout: float = 30.0):
        """Shutdown the logger gracefully"""
        try:
            # Flush remaining logs
            self.flush(timeout)
            
            # Stop background thread
            if self.background_thread:
                self.shutdown_event.set()
                self.background_thread.join(timeout)
            
            # Close API client
            self.api_client.close()
            
        except Exception as e:
            if self._error_callback:
                self._error_callback(e)
            else:
                logger.error(f"Error during shutdown: {e}")

# Global logger instance
_global_logger: Optional[PromptStackLogger] = None

def configure(
    api_key: str,
    base_url: str = "https://app.usebanyan.com",
    project_id: Optional[str] = None,
    **kwargs
):
    """Configure the global Banyan logger"""
    global _global_logger
    _global_logger = PromptStackLogger(
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        **kwargs
    )

def get_prompt(
    name: str,
    version: Optional[str] = None,
    branch: str = "main",
    use_cache: bool = True
) -> Optional[PromptData]:
    """Fetch a prompt using the global logger"""
    if _global_logger is None:
        raise RuntimeError("Must call configure() first")
    return _global_logger.get_prompt(name, version, branch, use_cache)

def experiment(
    experiment_id: str,
    sticky_key: str,
    sticky_value: str,
    use_cache: bool = True
) -> Optional[PromptData]:
    """Route experiment using the global logger"""
    if _global_logger is None:
        raise RuntimeError("Must call configure() first")
    return _global_logger.experiment(experiment_id, sticky_key, sticky_value, use_cache)

def log_prompt(
    input: str,
    output: str,
    prompt_data: Optional[PromptData] = None,
    prompt_id: Optional[str] = None,
    prompt_name: Optional[str] = None,
    version: Optional[str] = None,
    branch_name: Optional[str] = None,
    model: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    duration_ms: Optional[int] = None,
    blocking: bool = False
) -> bool:
    """Log a prompt execution using the global logger"""
    if _global_logger is None:
        raise RuntimeError("Must call configure() first")
    return _global_logger.log_prompt(
        input=input,
        output=output,
        prompt_data=prompt_data,
        prompt_id=prompt_id,
        prompt_name=prompt_name,
        version=version,
        branch_name=branch_name,
        model=model,
        metadata=metadata,
        duration_ms=duration_ms,
        blocking=blocking
    )

def flush(timeout: float = 30.0) -> bool:
    """Flush all queued logs using the global logger"""
    if _global_logger is None:
        return True
    return _global_logger.flush(timeout)

def get_stats() -> Dict[str, int]:
    """Get logging statistics from the global logger"""
    if _global_logger is None:
        return {}
    return _global_logger.get_stats()

def get_metrics() -> Optional[PerformanceMetrics]:
    """Get performance metrics from the global logger"""
    if _global_logger is None:
        return None
    return _global_logger.get_metrics()

def clear_cache():
    """Clear the global cache"""
    if _global_logger is not None:
        _global_logger.clear_cache()

def shutdown(timeout: float = 30.0):
    """Shutdown the global logger"""
    if _global_logger is not None:
        _global_logger.shutdown(timeout)

# Alias for the main logging function
log = log_prompt 