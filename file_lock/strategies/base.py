from abc import ABC, abstractmethod
from typing import TextIO

class FileLockStrategy(ABC):
    """Abstract base class for file locking strategies"""
    
    @abstractmethod
    def acquire_lock(self, file_handle: TextIO) -> bool:
        """Acquire a lock on the file"""
        pass
    
    @abstractmethod
    def release_lock(self, file_handle: TextIO) -> None:
        """Release the lock on the file"""
        pass 