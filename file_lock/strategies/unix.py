from typing import TextIO
from .base import FileLockStrategy

class UnixFileLockStrategy(FileLockStrategy):
    """Unix-like systems file locking strategy"""
    
    def acquire_lock(self, file_handle: TextIO) -> bool:
        try:
            import fcntl
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except (IOError, OSError):
            return False
    
    def release_lock(self, file_handle: TextIO) -> None:
        try:
            import fcntl
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)
        except:
            pass 