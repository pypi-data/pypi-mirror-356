"""Logging configuration for StepChain."""

import logging
import sys


def setup_logging(debug: bool = False, log_file: str | None = None) -> None:
    """Configure logging for the SDK.
    
    Args:
        debug: Enable debug level logging
        log_file: Optional file path to write logs to
    """
    # Determine log level
    level = logging.DEBUG if debug else logging.INFO
    
    # Create formatter
    if debug:
        # Detailed format for debugging
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        # Simple format for normal use
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Configure specific loggers
    sdk_logger = logging.getLogger('stepchain')
    sdk_logger.setLevel(level)
    
    # Reduce noise from libraries
    if not debug:
        logging.getLogger('openai').setLevel(logging.WARNING)
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # Log initial setup
    sdk_logger.debug(f"Logging configured: level={level}, debug={debug}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)