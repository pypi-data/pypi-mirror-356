# locktools

A file-based lock utility for Python applications and services. Useful for coordinating access to shared resources, pausing/resuming processes, and ensuring data consistency between distributed components.

## Features
- JSON lock file with status, timestamp, service, flush status, and unique lock ID
- Acquire and release locks
- Update and monitor flush status
- Wait for flush completion with timeout
- Read lock file status as a dictionary
- Option to delete or empty the lock file on release

## Installation

```sh
pip install locktools
```

## Usage

```python
from locktools import LockFile

# Create a lock file for a generic service
lock = LockFile(lockfile_path='lockfile.txt', service='myservice', timeout=10)
lock.acquire()  # Acquire the lock

# Check if locked
if lock.is_locked():
    print("Locked!")

# Update flush status (e.g., after a flush or checkpoint)
lock.update_flush_status('done')

# Wait for flush status to become 'done' (returns True if successful within timeout)
lock.wait_for_flush(expected_status='done')

# Read lock file status
status = lock.read_status()
print(status)

# Release the lock (default: empties the file)
lock.release()

# Optionally, delete the lock file on release
lock2 = LockFile(delete_on_release=True)
lock2.acquire()
lock2.release()  # This will delete the file
```

## Lock File JSON Example
```json
{
  "status": "locked",
  "timestamp": "2024-06-10T12:34:56.789Z",
  "service": "myservice",
  "flush_status": "pending",
  "lock_id": "uuid-1234-abcd"
}
```

## License
MIT
