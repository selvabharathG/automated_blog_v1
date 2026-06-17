"""
Module: Logger
Purpose: Industry-standard logging setup for the entire application
Author: Research Team
"""

import sys
import os
from loguru import logger as loguru_logger
from typing import Optional

class Logger:
    """Centralized logging configuration"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.setup_complete = False
    
    @staticmethod
    def setup(log_level: str = "INFO", log_dir: str = "logs") -> None:
        """Configure industry-standard logging"""
        
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Remove default handler
        loguru_logger.remove()
        
        # Standard format with rich information
        log_format = (
            "<level>{level: <8}</level> | "
            "<cyan>{name}:{function}:{line}</cyan> | "
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{message}</level>"
        )
        
        console_format = (
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan> - "
            "<level>{message}</level>"
        )
        
        # Console handler (stdout)
        loguru_logger.add(
            sys.stdout,
            format=console_format,
            level=log_level,
            colorize=True
        )
        
        # File handler - Main application log
        loguru_logger.add(
            os.path.join(log_dir, "app.log"),
            format=log_format,
            level=log_level,
            rotation="500 MB",
            retention="30 days",
            enqueue=True,  # Async logging for better performance
            backtrace=True,
            diagnose=True
        )
        
        # File handler - Error log
        loguru_logger.add(
            os.path.join(log_dir, "errors.log"),
            format=log_format,
            level="ERROR",
            rotation="500 MB",
            retention="90 days",
            enqueue=True,
            backtrace=True,
            diagnose=True
        )
        
        # File handler - Debug log (detailed)
        if log_level == "DEBUG":
            loguru_logger.add(
                os.path.join(log_dir, "debug.log"),
                format=log_format,
                level="DEBUG",
                rotation="500 MB",
                retention="7 days",
                enqueue=True
            )

def get_logger(name: Optional[str] = None):
    """Get logger instance with optional module name"""
    return loguru_logger.bind(name=name or "app")

# Initialize logger on module import
Logger.setup()
logger = get_logger()
