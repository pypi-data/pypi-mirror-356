"""
NusterDB: High-performance vector database with advanced indexing capabilities.

This package provides:
- Advanced vector operations with multiple distance metrics
- HNSW and Flat indexing with configurable parameters
- Metadata support with tags and timestamps
- Persistent storage with RocksDB backend
- Snapshot functionality for backup and restore
- Multi-platform support and performance optimizations

Example:
    >>> import nusterdb
    >>> 
    >>> # Create database with HNSW indexing
    >>> config = nusterdb.DatabaseConfig.simple(dim=128, use_hnsw=True)
    >>> db = nusterdb.NusterDB.simple("./my_vectors", 128, True)
    >>> 
    >>> # Create and add vectors with metadata
    >>> vector = nusterdb.Vector([0.1, 0.2, 0.3] * 42 + [0.4, 0.5])  # 128-dim
    >>> metadata = nusterdb.Metadata()
    >>> metadata.set("category", "document")
    >>> metadata.add_tag("important")
    >>> 
    >>> db.add(1, vector, metadata)
    >>> 
    >>> # Search with metadata filtering
    >>> query = nusterdb.Vector([0.1, 0.2, 0.3] * 42 + [0.4, 0.5])
    >>> results = db.search(query, k=10, filter={"category": "document"})
    >>> 
    >>> # Create snapshots for backup
    >>> db.snapshot_named("backup_v1")

Classes:
    Vector: N-dimensional vector with advanced math operations
    DistanceMetric: Distance metric enumeration (Euclidean, Cosine, etc.)
    Metadata: Vector metadata with tags and timestamps
    HNSWConfig: Configuration for HNSW indexing
    FlatIndexConfig: Configuration for flat indexing
    DatabaseConfig: Advanced database configuration
    StorageConfiguration: Storage engine configuration
    DatabaseStats: Database statistics and metrics
    NusterDB: Main database class with all advanced features
"""

from .nusterdb import (
    Vector,
    DistanceMetric,
    Metadata,
    HNSWConfig,
    FlatIndexConfig,
    DatabaseConfig,
    StorageConfiguration,
    DatabaseStats,
    NusterDB,
    __version__,
    DEFAULT_HNSW_M,
    DEFAULT_HNSW_EF_CONSTRUCTION,
    DEFAULT_CACHE_SIZE_MB,
)

__all__ = [
    "Vector",
    "DistanceMetric", 
    "Metadata",
    "HNSWConfig",
    "FlatIndexConfig",
    "DatabaseConfig",
    "StorageConfiguration",
    "DatabaseStats",
    "NusterDB",
    "__version__",
    "DEFAULT_HNSW_M",
    "DEFAULT_HNSW_EF_CONSTRUCTION",
    "DEFAULT_CACHE_SIZE_MB",
]
