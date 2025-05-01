from typing import TextIO
from .base import FileLockStrategy

class WindowsFileLockStrategy(FileLockStrategy):
    """Windows-specific file locking strategy"""
    
    def acquire_lock(self, file_handle: TextIO) -> bool:
        try:
            import msvcrt
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_NBLCK, 1)
            return True
        except (IOError, OSError):
            return False
    
    def release_lock(self, file_handle: TextIO) -> None:
        try:
            import msvcrt
            msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass 