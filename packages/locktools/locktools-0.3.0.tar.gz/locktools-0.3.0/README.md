# locktools

A file-based lock utility for Python applications and services. Useful for coordinating access to shared resources, pausing/resuming processes, and ensuring data consistency between distributed components.

## Features
- JSON lock file with status, timestamp, service, flush status, and unique lock ID
- Acquire and release locks
- Update and monitor flush status
- Wait for flush completion with timeout
- Read lock file status as a dictionary

## Installation

```sh
pip install locktools
```

## Usage

```python
from locktools import LockFile

# Create a lock file for the 'dumper' service
lock = LockFile(lockfile_path='.lock', service='dumper', timeout=10)
lock.acquire()  # Acquire the lock

# Check if locked
if lock.is_locked():
    print("Locked!")

# Update flush status (e.g., after consumer flushes data)
lock.update_flush_status('done')

# Wait for flush status to become 'done' (returns True if successful within timeout)
lock.wait_for_flush(expected_status='done')

# Read lock file status
status = lock.read_status()
print(status)

# Release the lock
lock.release()
```

## Lock File JSON Example
```json
{
  "status": "locked",
  "timestamp": "2024-06-10T12:34:56.789Z",
  "service": "dumper",
  "flush_status": "pending",
  "lock_id": "uuid-1234-abcd"
}
```

## License
MIT
