import platform
from typing import TextIO
from .strategies import WindowsFileLockStrategy, UnixFileLockStrategy

class FileLock:
    """Cross-platform file locking context manager using Strategy Pattern"""
    
    def __init__(self, file_handle: TextIO):
        self.file_handle = file_handle
        self._locked = False
        self._strategy = self._get_strategy()
    
    def _get_strategy(self):
        """Get the appropriate locking strategy based on the OS"""
        if platform.system() == "Windows":
            return WindowsFileLockStrategy()
        return UnixFileLockStrategy()
    
    def __enter__(self) -> bool:
        self._locked = self._strategy.acquire_lock(self.file_handle)
        return self._locked
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._locked:
            return  
        self._strategy.release_lock(self.file_handle)
