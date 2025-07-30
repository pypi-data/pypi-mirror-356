"""
Storage configuration and factory.
"""

import os
from typing import Union
from .file_storage import FileStore
from .postgres_storage import PostgresStore


class StorageConfig:
    """Configuration for storage backends."""

    def __init__(self):
        self.storage_type = os.getenv("METRICLLM_STORAGE_TYPE", "file")

        # File storage config
        self.file_base_path = os.getenv("METRICLLM_FILE_BASE_PATH", "data")

        # PostgreSQL config
        self.postgres_host = os.getenv("METRICLLM_POSTGRES_HOST", "localhost")
        self.postgres_port = int(os.getenv("METRICLLM_POSTGRES_PORT", "5432"))
        self.postgres_database = os.getenv("METRICLLM_POSTGRES_DATABASE", "metricllm")
        self.postgres_username = os.getenv("METRICLLM_POSTGRES_USERNAME", "postgres")
        self.postgres_password = os.getenv("METRICLLM_POSTGRES_PASSWORD", "")

    def create_storage(self) -> Union[FileStore, PostgresStore]:
        """Create storage instance based on configuration."""
        if self.storage_type.lower() == "file":
            return FileStore(base_path=self.file_base_path)
        elif self.storage_type.lower() == "postgres":
            return PostgresStore(
                host=self.postgres_host,
                port=self.postgres_port,
                database=self.postgres_database,
                username=self.postgres_username,
                password=self.postgres_password,
                base_path=self.file_base_path  # For exports
            )
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")


# Global storage instance
_storage_config = StorageConfig()
storage = _storage_config.create_storage()