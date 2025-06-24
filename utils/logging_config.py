from loguru import logger
import sys
import os
from config import DEBUG_MODE

def setup_logging():
    logger.remove() # Remove any default handlers

    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True) # Ensure log directory exists

    # Determine effective log level from your constants file
    effective_log_level = "DEBUG" if DEBUG_MODE else "INFO"

    # Max file size and backup count from your original config
    max_file_size_bytes = 5 * 1024 * 1024 # 5MB
    backup_count = 5 # How many rotated files to keep

    # File logging
    log_file_path = os.path.join(log_dir, "log_{time:YYYY-MM-DD}.log")
    logger.add(
        log_file_path,
        rotation=f"{max_file_size_bytes}B", # Rotate when file size is reached
        retention=backup_count,             # Number of backup files to keep
        level=effective_log_level,
        encoding="utf-8",
        enqueue=True  # Make logging asynchronous and thread-safe
    )

    # Console logging
    logger.add(
        sys.stderr,
        colorize=True,
        level=effective_log_level,
    )