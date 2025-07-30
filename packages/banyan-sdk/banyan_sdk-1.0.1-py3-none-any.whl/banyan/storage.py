"""
Banyan Storage Module

Provides production-ready storage features including:
- Delta compression for efficient storage
- Batch operations
- Indexing and caching
- Performance optimization
"""

import os
import json
import zlib
import time
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from .integrity import ContentHasher, AtomicFileOperations, IntegrityError

logger = logging.getLogger(__name__)

@dataclass
class DeltaEntry:
    """Represents a delta between two content versions"""
    base_hash: str
    target_hash: str
    delta_data: bytes
    compression_ratio: float
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'base_hash': self.base_hash,
            'target_hash': self.target_hash,
            'delta_data': self.delta_data.hex(),  # Store as hex string
            'compression_ratio': self.compression_ratio,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DeltaEntry':
        return cls(
            base_hash=data['base_hash'],
            target_hash=data['target_hash'],
            delta_data=bytes.fromhex(data['delta_data']),
            compression_ratio=data['compression_ratio'],
            created_at=data['created_at']
        )

class DeltaCompressor:
    """Handles delta compression between content versions"""
    
    @staticmethod
    def create_delta(base_content: str, target_content: str) -> DeltaEntry:
        """Create a delta from base to target content"""
        import difflib
        from datetime import datetime
        
        base_hash = ContentHasher.hash_content(base_content)
        target_hash = ContentHasher.hash_content(target_content)
        
        # Create unified diff
        diff_lines = list(difflib.unified_diff(
            base_content.splitlines(keepends=True),
            target_content.splitlines(keepends=True),
            lineterm='',
            n=3  # Context lines
        ))
        
        # Serialize and compress delta
        delta_text = ''.join(diff_lines)
        delta_bytes = delta_text.encode('utf-8')
        compressed_delta = zlib.compress(delta_bytes, level=6)
        
        # Calculate compression ratio
        original_size = len(target_content.encode('utf-8'))
        compressed_size = len(compressed_delta)
        compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
        
        return DeltaEntry(
            base_hash=base_hash,
            target_hash=target_hash,
            delta_data=compressed_delta,
            compression_ratio=compression_ratio,
            created_at=datetime.now().isoformat()
        )
    
    @staticmethod
    def apply_delta(base_content: str, delta_entry: DeltaEntry) -> str:
        """Apply a delta to base content to reconstruct target content"""
        import difflib
        
        # Verify base content hash
        base_hash = ContentHasher.hash_content(base_content)
        if base_hash != delta_entry.base_hash:
            raise IntegrityError(
                f"Base content hash mismatch",
                expected_hash=delta_entry.base_hash,
                actual_hash=base_hash
            )
        
        # Decompress and parse delta
        try:
            delta_bytes = zlib.decompress(delta_entry.delta_data)
            delta_text = delta_bytes.decode('utf-8')
            delta_lines = delta_text.splitlines(keepends=True)
        except Exception as e:
            raise IntegrityError(f"Failed to decompress delta: {e}")
        
        # Apply delta using difflib
        try:
            base_lines = base_content.splitlines(keepends=True)
            
            # Parse unified diff and apply changes
            target_lines = []
            i = 0
            
            for line in delta_lines:
                if line.startswith('@@'):
                    # Parse hunk header: @@ -start,count +start,count @@
                    parts = line.split()
                    if len(parts) >= 2:
                        old_range = parts[1][1:]  # Remove '-'
                        new_range = parts[2][1:]  # Remove '+'
                        
                        old_start = int(old_range.split(',')[0]) - 1  # Convert to 0-based
                        # Add unchanged lines before this hunk
                        while i < old_start and i < len(base_lines):
                            target_lines.append(base_lines[i])
                            i += 1
                
                elif line.startswith(' '):
                    # Context line (unchanged)
                    if i < len(base_lines):
                        target_lines.append(base_lines[i])
                        i += 1
                
                elif line.startswith('-'):
                    # Deleted line (skip in base)
                    i += 1
                
                elif line.startswith('+'):
                    # Added line
                    target_lines.append(line[1:])
            
            # Add remaining unchanged lines
            while i < len(base_lines):
                target_lines.append(base_lines[i])
                i += 1
            
            target_content = ''.join(target_lines)
            
            # Verify target content hash
            target_hash = ContentHasher.hash_content(target_content)
            if target_hash != delta_entry.target_hash:
                raise IntegrityError(
                    f"Target content hash mismatch after applying delta",
                    expected_hash=delta_entry.target_hash,
                    actual_hash=target_hash
                )
            
            return target_content
            
        except Exception as e:
            if isinstance(e, IntegrityError):
                raise
            raise IntegrityError(f"Failed to apply delta: {e}")

class ContentStore:
    """Content-addressable storage with delta compression"""
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = Path(storage_dir)
        self.objects_dir = self.storage_dir / 'objects'
        self.deltas_dir = self.storage_dir / 'deltas'
        self.index_db = self.storage_dir / 'index.db'
        
        # Create directories
        self.objects_dir.mkdir(parents=True, exist_ok=True)
        self.deltas_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize SQLite index
        self._init_index_db()
        
        # Thread safety
        self._lock = threading.RLock()
    
    def _init_index_db(self):
        """Initialize SQLite database for indexing"""
        with sqlite3.connect(str(self.index_db)) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS objects (
                    hash TEXT PRIMARY KEY,
                    size INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS deltas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    base_hash TEXT NOT NULL,
                    target_hash TEXT NOT NULL,
                    compression_ratio REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(base_hash, target_hash)
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_objects_type ON objects(type)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_deltas_base ON deltas(base_hash)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_deltas_target ON deltas(target_hash)
            ''')
            
            conn.commit()
    
    def _get_object_path(self, content_hash: str) -> Path:
        """Get storage path for content hash"""
        # Use Git-style object storage: first 2 chars as directory
        prefix = content_hash[:2]
        suffix = content_hash[2:]
        return self.objects_dir / prefix / suffix
    
    def _get_delta_path(self, base_hash: str, target_hash: str) -> Path:
        """Get storage path for delta"""
        delta_name = f"{base_hash[:8]}_{target_hash[:8]}.delta"
        return self.deltas_dir / delta_name
    
    def store_content(self, content: str, content_type: str = "text") -> str:
        """Store content and return its hash"""
        content_hash = ContentHasher.hash_content(content)
        
        with self._lock:
            object_path = self._get_object_path(content_hash)
            
            # Check if already exists
            if object_path.exists():
                self._update_access_time(content_hash)
                return content_hash
            
            # Store content atomically
            object_path.parent.mkdir(parents=True, exist_ok=True)
            stored_hash = AtomicFileOperations.write_text_atomic(object_path, content)
            
            # Update index
            with sqlite3.connect(str(self.index_db)) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO objects 
                    (hash, size, type, created_at, access_count, last_accessed)
                    VALUES (?, ?, ?, ?, 1, ?)
                ''', (
                    content_hash,
                    len(content.encode('utf-8')),
                    content_type,
                    time.time(),
                    time.time()
                ))
                conn.commit()
            
            logger.debug(f"Stored content {content_hash[:8]} ({len(content)} bytes)")
            return content_hash
    
    def retrieve_content(self, content_hash: str) -> Optional[str]:
        """Retrieve content by hash"""
        with self._lock:
            object_path = self._get_object_path(content_hash)
            
            if not object_path.exists():
                # Try to reconstruct from delta
                reconstructed = self._reconstruct_from_delta(content_hash)
                if reconstructed:
                    # Store reconstructed content for future access
                    self.store_content(reconstructed)
                    return reconstructed
                return None
            
            try:
                content, actual_hash = AtomicFileOperations.read_text_verified(object_path, content_hash)
                self._update_access_time(content_hash)
                return content
            except IntegrityError as e:
                logger.error(f"Content integrity error for {content_hash}: {e}")
                return None
    
    def store_with_delta(self, content: str, base_hash: Optional[str] = None, content_type: str = "text") -> str:
        """Store content with delta compression against base"""
        content_hash = ContentHasher.hash_content(content)
        
        with self._lock:
            # Always store the full content first
            self.store_content(content, content_type)
            
            # If we have a base, create delta
            if base_hash and base_hash != content_hash:
                base_content = self.retrieve_content(base_hash)
                if base_content:
                    delta_entry = DeltaCompressor.create_delta(base_content, content)
                    
                    # Only store delta if it provides good compression
                    if delta_entry.compression_ratio < 0.8:  # 20% savings or better
                        self._store_delta(delta_entry)
                        logger.debug(f"Created delta {base_hash[:8]} -> {content_hash[:8]} "
                                   f"(ratio: {delta_entry.compression_ratio:.2f})")
            
            return content_hash
    
    def _store_delta(self, delta_entry: DeltaEntry):
        """Store a delta entry"""
        delta_path = self._get_delta_path(delta_entry.base_hash, delta_entry.target_hash)
        delta_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Store delta data
        delta_dict = delta_entry.to_dict()
        AtomicFileOperations.write_json_atomic(delta_path, delta_dict)
        
        # Update index
        with sqlite3.connect(str(self.index_db)) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO deltas 
                (base_hash, target_hash, compression_ratio, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                delta_entry.base_hash,
                delta_entry.target_hash,
                delta_entry.compression_ratio,
                delta_entry.created_at
            ))
            conn.commit()
    
    def _reconstruct_from_delta(self, target_hash: str) -> Optional[str]:
        """Try to reconstruct content from available deltas"""
        with sqlite3.connect(str(self.index_db)) as conn:
            cursor = conn.execute('''
                SELECT base_hash FROM deltas WHERE target_hash = ?
            ''', (target_hash,))
            
            for (base_hash,) in cursor:
                base_content = self.retrieve_content(base_hash)
                if base_content:
                    delta_path = self._get_delta_path(base_hash, target_hash)
                    if delta_path.exists():
                        try:
                            delta_dict, _ = AtomicFileOperations.read_json_verified(delta_path)
                            delta_entry = DeltaEntry.from_dict(delta_dict)
                            reconstructed = DeltaCompressor.apply_delta(base_content, delta_entry)
                            logger.debug(f"Reconstructed {target_hash[:8]} from delta")
                            return reconstructed
                        except Exception as e:
                            logger.warning(f"Failed to apply delta {base_hash[:8]} -> {target_hash[:8]}: {e}")
                            continue
        
        return None
    
    def _update_access_time(self, content_hash: str):
        """Update access statistics"""
        with sqlite3.connect(str(self.index_db)) as conn:
            conn.execute('''
                UPDATE objects 
                SET access_count = access_count + 1, last_accessed = ?
                WHERE hash = ?
            ''', (time.time(), content_hash))
            conn.commit()
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        with sqlite3.connect(str(self.index_db)) as conn:
            # Object stats
            cursor = conn.execute('''
                SELECT COUNT(*), SUM(size), AVG(size) FROM objects
            ''')
            obj_count, total_size, avg_size = cursor.fetchone()
            
            # Delta stats
            cursor = conn.execute('''
                SELECT COUNT(*), AVG(compression_ratio) FROM deltas
            ''')
            delta_count, avg_compression = cursor.fetchone()
            
            return {
                'object_count': obj_count or 0,
                'total_size_bytes': total_size or 0,
                'average_size_bytes': avg_size or 0,
                'delta_count': delta_count or 0,
                'average_compression_ratio': avg_compression or 1.0
            }
    
    def cleanup_unused_objects(self, min_age_days: int = 30) -> int:
        """Clean up objects that haven't been accessed recently"""
        cutoff_time = time.time() - (min_age_days * 24 * 60 * 60)
        
        with self._lock:
            with sqlite3.connect(str(self.index_db)) as conn:
                # Find unused objects
                cursor = conn.execute('''
                    SELECT hash FROM objects 
                    WHERE last_accessed < ? AND access_count <= 1
                ''', (cutoff_time,))
                
                removed_count = 0
                for (content_hash,) in cursor:
                    object_path = self._get_object_path(content_hash)
                    try:
                        if object_path.exists():
                            object_path.unlink()
                            removed_count += 1
                    except Exception as e:
                        logger.warning(f"Failed to remove unused object {content_hash}: {e}")
                
                # Remove from index
                conn.execute('''
                    DELETE FROM objects 
                    WHERE last_accessed < ? AND access_count <= 1
                ''', (cutoff_time,))
                conn.commit()
                
                logger.info(f"Cleaned up {removed_count} unused objects")
                return removed_count

class StorageManager:
    """High-level storage manager combining all storage features"""
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = Path(storage_dir)
        self.content_store = ContentStore(self.storage_dir / 'content')
        
        # Create directories
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def store(self, content: str, content_type: str = "text", base_hash: str = None) -> str:
        """Store content with optional delta compression"""
        content_hash = ContentHasher.hash_content(content)
        
        # Store to persistent storage
        if base_hash:
            stored_hash = self.content_store.store_with_delta(content, base_hash, content_type)
        else:
            stored_hash = self.content_store.store_content(content, content_type)
        
        return stored_hash
    
    def retrieve(self, content_hash: str) -> Optional[str]:
        """Retrieve content"""
        return self.content_store.retrieve_content(content_hash)
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive storage statistics"""
        storage_stats = self.content_store.get_storage_stats()
        
        return {
            'storage': storage_stats,
            'total_efficiency': {
                'compression_saving': 1.0 - storage_stats.get('average_compression_ratio', 1.0),
            }
        }
    
    def maintenance(self, cleanup_days: int = 30) -> Dict[str, Any]:
        """Perform maintenance operations"""
        # Cleanup old objects
        removed_count = self.content_store.cleanup_unused_objects(cleanup_days)
        
        return {
            'objects_removed': removed_count
        } 