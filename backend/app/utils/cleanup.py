import os
import time

def cleanup_old_files(directory: str, max_age_seconds: int = 3600):
    """Refactored to check if directory exists first."""
    if not os.path.exists(directory):
        return

    now = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.stat(file_path).st_mtime < now - max_age_seconds:
            os.remove(file_path)
