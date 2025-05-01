import json
import os
import random
import time
from dataclasses import dataclass
from typing import Optional

from file_lock.file_lock_manager import FileLock


@dataclass
class CounterConfig:
    """Configuration for the counter service"""
    counter_file: str = "counter.json"
    max_retries: int = 10
    base_delay: float = 0.05
    lock_timeout: float = 2.0
    initial_value: int = 1

class CounterService:
    """Thread-safe counter service using file-based storage with cross-platform locking"""
    
    def __init__(self, config: Optional[CounterConfig] = None):
        self.config = config or CounterConfig()
        self._ensure_counter_file_exists()

    def _ensure_counter_file_exists(self):
        """Ensure the counter file exists with initial value"""
        if not os.path.exists(self.config.counter_file):
            with open(self.config.counter_file, 'w') as f:
                json.dump({"counter": self.config.initial_value}, f)

    def get_next_number(self) -> int:
        """
        Gets the next unique number from the counter service.
        Uses cross-platform file locking for thread safety.
        
        Returns:
            int: The next unique number
        
        Raises:
            Exception: If unable to get a number after max retries
        """
        last_exception = None
        for attempt in range(self.config.max_retries):
            try:
                with open(self.config.counter_file, 'r+') as f:
                    with FileLock(f) as locked:
                        if not locked:
                            delay = self._calculate_backoff_delay(attempt)
                            time.sleep(delay)
                            continue

                        # Read current value
                        f.seek(0)
                        data = json.load(f)
                        current_counter = data["counter"]

                        # Write new value
                        f.seek(0)
                        json.dump({"counter": current_counter + 1}, f)
                        f.truncate()
                        
                        return current_counter

            except Exception as e:
                last_exception = e
                delay = self._calculate_backoff_delay(attempt)
                time.sleep(delay)

        raise Exception(
            f"Failed to get counter after {self.config.max_retries} attempts: {str(last_exception)}"
        )

    def _calculate_backoff_delay(self, attempt: int) -> float:
        """Calculate the exponential backoff delay with jitter"""
        return min(
            self.config.base_delay * (2 ** attempt) * (1 + random.random()),
            self.config.lock_timeout
        )

    def reset_counter(self, new_value: Optional[int] = None) -> None:
        """Reset the counter to a specific value or the initial value"""
        for attempt in range(self.config.max_retries):
            try:
                with open(self.config.counter_file, 'r+') as f:
                    with FileLock(f) as locked:
                        if not locked:
                            time.sleep(self._calculate_backoff_delay(attempt))
                            continue

                        f.seek(0)
                        json.dump({"counter": new_value or self.config.initial_value}, f)
                        f.truncate()
                        return

            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    raise Exception(f"Failed to reset counter: {str(e)}")
                time.sleep(self._calculate_backoff_delay(attempt)) 