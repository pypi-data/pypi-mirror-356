"""
Logging configuration for Wolf toolkit
"""

import logging
import os
import sys
from datetime import datetime

class Logger:
    """
    Centralized logging system for Wolf toolkit
    """
    
    _loggers = {}
    _configured = False
    
    def __init__(self, name="wolf", level=None):
        """
        Initialize logger instance
        
        Args:
            name (str): Logger name
            level (str): Logging level
        """
        self.name = name
        self.level = level or os.getenv("WOLF_LOG_LEVEL", "INFO")
        
        if not Logger._configured:
            self._configure_logging()
            Logger._configured = True
    
    def _configure_logging(self):
        """Configure the logging system"""
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, self.level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(
                    os.path.join(log_dir, f"wolf_{datetime.now().strftime('%Y%m%d')}.log")
                )
            ]
        )
    
    def get_logger(self):
        """
        Get or create logger instance
        
        Returns:
            logging.Logger: Logger instance
        """
        if self.name not in Logger._loggers:
            logger = logging.getLogger(self.name)
            logger.setLevel(getattr(logging, self.level.upper()))
            Logger._loggers[self.name] = logger
        
        return Logger._loggers[self.name]
    
    @staticmethod
    def set_global_level(level):
        """
        Set global logging level
        
        Args:
            level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        logging.getLogger().setLevel(getattr(logging, level.upper()))
        for logger in Logger._loggers.values():
            logger.setLevel(getattr(logging, level.upper()))
