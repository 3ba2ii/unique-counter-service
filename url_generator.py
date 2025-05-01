from typing import Optional
from counter_service import CounterConfig, CounterService
from utils.base62_generator import Base62Generator


class ShortCodeGenerator:
    """Generator for unique short codes using base62 encoding"""

    def __init__(self, counter_config: Optional[CounterConfig] = None):
        """
        Initialize the generator with optional counter configuration.

        Args:
            counter_config: Optional configuration for the counter service
        """
        self.counter_service = CounterService(counter_config)

    def generate_code(self) -> str:
        """
        Generate a unique short code.

        Returns:
            str: A unique base62 encoded string

        Raises:
            Exception: If unable to generate a code after max retries
        """
        number = self.counter_service.get_next_number()
        return Base62Generator.encode(number)

    def reset_counter(self, new_value: Optional[int] = None) -> None:
        """
        Reset the counter to a specific value or its initial value.

        Args:
            new_value: Optional value to reset the counter to
        """
        self.counter_service.reset_counter(new_value)
