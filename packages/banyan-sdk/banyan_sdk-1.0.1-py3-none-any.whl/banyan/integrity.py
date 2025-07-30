"""
Banyan Data Integrity Module

Provides production-ready data integrity features including:
- Atomic file operations
- Hash verification
- File locking
- Error recovery
- Content-addressable storage
"""

import os
import json
import hashlib
import tempfile
import shutil
import time
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union, ContextManager
from contextlib import contextmanager
from dataclasses import dataclass
import threading

# Import fcntl only on Unix systems
try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

logger = logging.getLogger(__name__)

@dataclass
class IntegrityError(Exception):
    """Exception raised when data integrity checks fail"""
    message: str
    file_path: Optional[str] = None
    expected_hash: Optional[str] = None
    actual_hash: Optional[str] = None

class ContentHasher:
    """Content-addressable hashing utilities with full SHA-256"""
    
    @staticmethod
    def hash_content(content: str) -> str:
        """Generate full SHA-256 hash for content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    @staticmethod
    def hash_bytes(data: bytes) -> str:
        """Generate full SHA-256 hash for bytes"""
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def short_hash(content: str, length: int = 12) -> str:
        """Generate shortened hash for display purposes only"""
        return ContentHasher.hash_content(content)[:length]
    
    @staticmethod
    def verify_content(content: str, expected_hash: str) -> bool:
        """Verify content matches expected hash"""
        actual_hash = ContentHasher.hash_content(content)
        return actual_hash == expected_hash

class FileLock:
    """Cross-platform file locking implementation"""
    
    def __init__(self, lock_file: Path, timeout: float = 30.0):
        self.lock_file = Path(lock_file)
        self.timeout = timeout
        self.lock_fd = None
        self._lock = threading.Lock()
    
    def acquire(self) -> bool:
        """Acquire lock with timeout"""
        with self._lock:
            if self.lock_fd is not None:
                return True  # Already acquired
            
            start_time = time.time()
            self.lock_file.parent.mkdir(parents=True, exist_ok=True)
            
            while time.time() - start_time < self.timeout:
                try:
                    # Create lock file
                    self.lock_fd = os.open(str(self.lock_file), 
                                         os.O_CREAT | os.O_EXCL | os.O_RDWR)
                    
                    # Write process info
                    lock_info = {
                        'pid': os.getpid(),
                        'timestamp': time.time(),
                        'thread_id': threading.get_ident()
                    }
                    os.write(self.lock_fd, json.dumps(lock_info).encode())
                    
                    # Try to get exclusive lock (non-blocking)
                    try:
                        if HAS_FCNTL:
                            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        # On Windows, file creation with O_EXCL is sufficient
                        logger.debug(f"Acquired lock: {self.lock_file}")
                        return True
                    except (OSError, IOError):
                        os.close(self.lock_fd)
                        self.lock_fd = None
                        self.lock_file.unlink(missing_ok=True)
                
                except FileExistsError:
                    # Lock file exists, check if it's stale
                    if self._is_stale_lock():
                        self._remove_stale_lock()
                        continue
                
                except Exception as e:
                    logger.debug(f"Lock attempt failed: {e}")
                    if self.lock_fd:
                        try:
                            os.close(self.lock_fd)
                        except:
                            pass
                        self.lock_fd = None
                
                time.sleep(0.1)  # Brief wait before retry
            
            return False
    
    def release(self):
        """Release the lock"""
        with self._lock:
            if self.lock_fd is not None:
                try:
                    if HAS_FCNTL:
                        fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
                    os.close(self.lock_fd)
                except:
                    pass
                finally:
                    self.lock_fd = None
                
                # Remove lock file
                try:
                    self.lock_file.unlink(missing_ok=True)
                    logger.debug(f"Released lock: {self.lock_file}")
                except:
                    pass
    
    def _is_stale_lock(self) -> bool:
        """Check if lock file is stale (process died)"""
        try:
            with open(self.lock_file, 'r') as f:
                lock_info = json.load(f)
            
            pid = lock_info.get('pid')
            timestamp = lock_info.get('timestamp', 0)
            
            # Check if process is still running
            if pid:
                try:
                    os.kill(pid, 0)  # Signal 0 just checks if process exists
                    # Process exists, check if lock is too old (stale after 5 minutes)
                    return time.time() - timestamp > 300
                except ProcessLookupError:
                    # Process doesn't exist
                    return True
                except PermissionError:
                    # Process exists but we can't signal it, assume it's valid
                    return False
            
            return True
        except Exception:
            return True
    
    def _remove_stale_lock(self):
        """Remove stale lock file"""
        try:
            self.lock_file.unlink(missing_ok=True)
            logger.debug(f"Removed stale lock: {self.lock_file}")
        except Exception as e:
            logger.warning(f"Failed to remove stale lock {self.lock_file}: {e}")
    
    def __enter__(self):
        if not self.acquire():
            raise TimeoutError(f"Failed to acquire lock {self.lock_file} within {self.timeout}s")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

@contextmanager
def file_lock(lock_file: Path, timeout: float = 30.0) -> ContextManager[FileLock]:
    """Context manager for file locking"""
    lock = FileLock(lock_file, timeout)
    try:
        if not lock.acquire():
            raise TimeoutError(f"Failed to acquire lock {lock_file} within {timeout}s")
        yield lock
    finally:
        lock.release()

class AtomicFileOperations:
    """Atomic file operations with integrity verification"""
    
    @staticmethod
    def write_text_atomic(file_path: Path, content: str, expected_hash: Optional[str] = None) -> str:
        """
        Atomically write text content with hash verification
        Returns the content hash
        """
        file_path = Path(file_path)
        content_hash = ContentHasher.hash_content(content)
        
        # Verify hash if provided
        if expected_hash and content_hash != expected_hash:
            raise IntegrityError(
                f"Content hash mismatch for {file_path}",
                str(file_path),
                expected_hash,
                content_hash
            )
        
        # Create parent directory
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to temporary file first
        temp_file = None
        try:
            temp_fd, temp_path = tempfile.mkstemp(
                prefix=f".{file_path.name}.",
                suffix=".tmp",
                dir=file_path.parent
            )
            temp_file = Path(temp_path)
            
            # Write content
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
            
            # Verify written content
            written_content = temp_file.read_text(encoding='utf-8')
            written_hash = ContentHasher.hash_content(written_content)
            
            if written_hash != content_hash:
                raise IntegrityError(
                    f"Written content verification failed for {file_path}",
                    str(file_path),
                    content_hash,
                    written_hash
                )
            
            # Atomic move (rename is atomic on most filesystems)
            if os.name == 'nt':  # Windows
                if file_path.exists():
                    file_path.unlink()
            shutil.move(str(temp_file), str(file_path))
            
            logger.debug(f"Atomically wrote {len(content)} bytes to {file_path}")
            return content_hash
            
        except Exception as e:
            # Clean up temp file on error
            if temp_file and temp_file.exists():
                try:
                    temp_file.unlink()
                except:
                    pass
            raise IntegrityError(f"Failed to write {file_path}: {e}", str(file_path))
    
    @staticmethod
    def write_json_atomic(file_path: Path, data: Dict[str, Any], expected_hash: Optional[str] = None) -> str:
        """
        Atomically write JSON data with hash verification
        Returns the content hash
        """
        content = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
        return AtomicFileOperations.write_text_atomic(file_path, content, expected_hash)
    
    @staticmethod
    def read_text_verified(file_path: Path, expected_hash: Optional[str] = None) -> tuple[str, str]:
        """
        Read text content with hash verification
        Returns (content, actual_hash)
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
            actual_hash = ContentHasher.hash_content(content)
            
            if expected_hash and actual_hash != expected_hash:
                raise IntegrityError(
                    f"Content hash verification failed for {file_path}",
                    str(file_path),
                    expected_hash,
                    actual_hash
                )
            
            return content, actual_hash
            
        except Exception as e:
            if isinstance(e, IntegrityError):
                raise
            raise IntegrityError(f"Failed to read {file_path}: {e}", str(file_path))
    
    @staticmethod
    def read_json_verified(file_path: Path, expected_hash: Optional[str] = None) -> tuple[Dict[str, Any], str]:
        """
        Read JSON data with hash verification
        Returns (data, actual_hash)
        """
        content, content_hash = AtomicFileOperations.read_text_verified(file_path, expected_hash)
        try:
            data = json.loads(content)
            return data, content_hash
        except json.JSONDecodeError as e:
            raise IntegrityError(f"Invalid JSON in {file_path}: {e}", str(file_path))

class IntegrityManager:
    """Manages data integrity for the entire Banyan project"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.banyan_dir = self.project_root / '.banyan'
        self.locks_dir = self.banyan_dir / 'locks'
        self.integrity_dir = self.banyan_dir / 'integrity'
        
        # Create directories
        self.locks_dir.mkdir(parents=True, exist_ok=True)
        self.integrity_dir.mkdir(parents=True, exist_ok=True)
    
    def get_lock_path(self, resource_name: str) -> Path:
        """Get lock file path for a resource"""
        safe_name = resource_name.replace('/', '_').replace('\\', '_')
        return self.locks_dir / f"{safe_name}.lock"
    
    @contextmanager
    def lock_resource(self, resource_name: str, timeout: float = 30.0):
        """Lock a named resource"""
        lock_path = self.get_lock_path(resource_name)
        with file_lock(lock_path, timeout) as lock:
            yield lock
    
    def verify_project_integrity(self) -> Dict[str, Any]:
        """Verify integrity of entire project"""
        results = {
            'checked_files': 0,
            'corrupted_files': [],
            'missing_hashes': [],
            'errors': []
        }
        
        try:
            # Check all critical files
            for root, dirs, files in os.walk(self.banyan_dir):
                for file in files:
                    if file.endswith(('.json', '.txt')) and not file.startswith('.'):
                        file_path = Path(root) / file
                        results['checked_files'] += 1
                        
                        try:
                            # Read and verify file
                            if file.endswith('.json'):
                                AtomicFileOperations.read_json_verified(file_path)
                            else:
                                AtomicFileOperations.read_text_verified(file_path)
                        except IntegrityError as e:
                            results['corrupted_files'].append({
                                'file': str(file_path),
                                'error': str(e)
                            })
                        except Exception as e:
                            results['errors'].append({
                                'file': str(file_path),
                                'error': str(e)
                            })
        
        except Exception as e:
            results['errors'].append({'error': f"Project integrity check failed: {e}"})
        
        return results
    
    def repair_corrupted_file(self, file_path: Path, backup_content: str = None) -> bool:
        """Attempt to repair a corrupted file"""
        try:
            if backup_content:
                # Use provided backup content
                AtomicFileOperations.write_text_atomic(file_path, backup_content)
                logger.info(f"Repaired corrupted file: {file_path}")
                return True
            else:
                # Try to find backup or previous version
                # This would need to be implemented based on the specific backup strategy
                logger.warning(f"No backup available for corrupted file: {file_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to repair file {file_path}: {e}")
            return False

# Global integrity manager instance
_integrity_manager: Optional[IntegrityManager] = None

def get_integrity_manager(project_root: Path = None) -> IntegrityManager:
    """Get or create global integrity manager"""
    global _integrity_manager
    if _integrity_manager is None or (project_root and _integrity_manager.project_root != project_root):
        _integrity_manager = IntegrityManager(project_root or Path.cwd())
    return _integrity_manager 