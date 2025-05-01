# Base62 URL Generator

A thread-safe, file-based URL shortener that generates unique short codes using base62 encoding.

## Features

- Thread-safe counter service using file-based storage
- Cross-platform file locking mechanism
- Base62 encoding for short, URL-friendly codes
- Configurable counter service with exponential backoff
- Concurrent testing capabilities

## Components

### Core Components

- `url_generator.py`: Main generator class that creates unique short codes
- `counter_service.py`: Thread-safe counter service with file-based storage
- `utils/base62_generator.py`: Base62 encoding implementation
- `file_lock/`: Cross-platform file locking mechanism

### Testing

- `test_concurrent.py`: Concurrent testing tool to verify thread safety

## Usage

### Basic Usage

```python
from url_generator import ShortCodeGenerator

# Create a generator with default settings
generator = ShortCodeGenerator()

# Generate a unique short code
short_code = generator.generate_code()
print(short_code)  # e.g., "1aB2"
```

### Custom Configuration

```python
from url_generator import ShortCodeGenerator
from counter_service import CounterConfig

# Create custom configuration
config = CounterConfig(
    counter_file="custom_counter.json",
    max_retries=15,
    base_delay=0.1,
    lock_timeout=5.0,
    initial_value=1000
)

# Create generator with custom config
generator = ShortCodeGenerator(config)

# Generate codes
code1 = generator.generate_code()
code2 = generator.generate_code()
```

### Resetting Counter

```python
# Reset to initial value
generator.reset_counter()

# Reset to specific value
generator.reset_counter(1000)
```

### Concurrent Testing

```python
from test_concurrent import ConcurrentTester

# Test with 1000 concurrent users
tester = ConcurrentTester(num_users=1000)
results = tester.run_test()

# Print test results
print(f"Success rate: {results['success_rate']:.2f}%")
print(f"Unique codes: {results['unique_codes']}")
```

## Requirements

- Python 3.6+
- No external dependencies

## Thread Safety

The system ensures thread safety through:
- File-based locking mechanism
- Exponential backoff for lock acquisition
- Atomic file operations
- Cross-platform compatibility

## Performance

- Designed for high concurrency
- Configurable retry mechanism
- Efficient base62 encoding
- Minimal file I/O operations

## License

MIT License 