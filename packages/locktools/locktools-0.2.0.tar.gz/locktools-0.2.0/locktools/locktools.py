import os
import json
import uuid
from datetime import datetime, timezone
from typing import Optional

class LockFile:
    """
    A file-based lock utility for coordinating access to shared resources between processes or services.
    The lock file is written in JSON format and contains status, timestamp, service, flush status, and a unique lock ID.
    """
    def __init__(self, lockfile_path: str = '.lock', service: str = 'unknown', timeout: int = 10):
        """
        Initialize a LockFile instance.

        Args:
            lockfile_path (str): Path to the lock file. Defaults to '.lock'.
            service (str): Name of the service creating the lock. Defaults to 'unknown'.
            timeout (int): Timeout in seconds for waiting operations. Defaults to 10.
        """
        self.lockfile_path = lockfile_path
        self.service = service
        self.timeout = timeout
        self.lock_id = str(uuid.uuid4())

    def acquire(self):
        """
        Acquire the lock by creating or overwriting the lock file with lock metadata in JSON format.
        Sets status to 'locked', flush_status to 'pending', and records the current timestamp and service.
        """
        data = {
            'status': 'locked',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'service': self.service,
            'flush_status': 'pending',
            'lock_id': self.lock_id
        }
        with open(self.lockfile_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def release(self):
        """
        Release the lock by removing the lock file, if it exists.
        """
        if os.path.exists(self.lockfile_path):
            os.remove(self.lockfile_path)

    def is_locked(self) -> bool:
        """
        Check if the lock file exists, indicating that the resource is currently locked.

        Returns:
            bool: True if the lock file exists, False otherwise.
        """
        return os.path.exists(self.lockfile_path)

    def update_flush_status(self, flush_status: str):
        """
        Update the flush_status field in the lock file and refresh the timestamp.

        Args:
            flush_status (str): The new flush status (e.g., 'pending', 'done', 'failed').
        """
        data = self.read_status()
        if data:
            data['flush_status'] = flush_status
            data['timestamp'] = datetime.now(timezone.utc).isoformat()
            with open(self.lockfile_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)

    def read_status(self) -> Optional[dict]:
        """
        Read and return the contents of the lock file as a dictionary.

        Returns:
            dict or None: The lock file data if it exists and is valid JSON, otherwise None.
        """
        if not os.path.exists(self.lockfile_path):
            return None
        try:
            with open(self.lockfile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def wait_for_flush(self, expected_status: str = 'done') -> bool:
        """
        Wait for the flush_status in the lock file to reach the expected status or until timeout.

        Args:
            expected_status (str): The flush status to wait for (default: 'done').

        Returns:
            bool: True if the expected status is reached within the timeout, False otherwise.
        """
        import time
        start = time.time()
        while time.time() - start < self.timeout:
            data = self.read_status()
            if data and data.get('flush_status') == expected_status:
                return True
            time.sleep(0.5)
        return False 