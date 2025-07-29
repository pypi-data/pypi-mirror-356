import logging
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from queue import Queue
import os


def setup_logger(
    name: str = "ApplicationLogger", 
    log_level: int = logging.INFO,
    log_file: str = None,
    max_bytes: int = 10485760,  # 10MB default
    backup_count: int = 5
) -> logging.Logger:
    """
    Set up and return a thread-safe logger using a QueueHandler and QueueListener.
    If log_file is provided, all loggers will write to the same file.
    
    Args:
        name (str): The name of the logger.
        log_level (int): The logging level, e.g., logging.INFO or logging.DEBUG.
        log_file (str, optional): Path to log file. If provided, enables file logging.
        max_bytes (int): Maximum size in bytes before log rotation.
        backup_count (int): Number of backup files to keep.

    Returns:
        logging.Logger: Configured logger.
    """
    # disable litellm
    logger = logging.getLogger("LiteLLM")
    logger.setLevel(logging.CRITICAL + 1) 

    # Configure the root logger if a log file is specified
    if log_file is not None and not logging.getLogger().handlers:
        # Configure the root logger first
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Create a queue for thread-safe logging at the root level
        root_queue = Queue()
        root_queue_handler = QueueHandler(root_queue)
        root_logger.addHandler(root_queue_handler)
        
        # Create handlers
        handlers = []
        
        # Console handler
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)
        
        # File handler with rotation
        if log_file and os.environ.get('LOCAL_RANK', '0') == '0':
            # Ensure the directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
                
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=max_bytes, 
                backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
        
        # Set up the listener with all handlers
        root_listener = QueueListener(root_queue, *handlers)
        root_listener.start()
        
        # Store the listener for cleanup
        root_logger.listener = root_listener
    
    # Now set up the specific named logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # If this logger doesn't have handlers yet, add a queue handler
    # Note: It will inherit the root logger's configuration if we set one up
    if not logger.handlers and not log_file:
        # Create a queue for thread-safe logging
        log_queue = Queue()

        # Set up a queue handler and listener
        queue_handler = QueueHandler(log_queue)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        listener = QueueListener(log_queue, stream_handler)
        listener.start()

        logger.addHandler(queue_handler)
        logger.listener = listener  # Attach the listener for cleanup later

    return logger