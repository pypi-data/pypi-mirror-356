"""
Base module class for all Wolf modules
"""

import logging
from abc import ABC, abstractmethod
from wolf.core.logger import Logger

class BaseModule(ABC):
    """
    Abstract base class for all Wolf modules
    Provides common functionality and structure
    """
    
    def __init__(self, name=None):
        """
        Initialize the base module
        
        Args:
            name (str): Name of the module
        """
        self.name = name or self.__class__.__name__
        self.logger = Logger(self.name).get_logger()
        self._setup()
    
    def _setup(self):
        """
        Setup method called during initialization
        Override in subclasses for module-specific setup
        """
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Main execution method for the module
        Must be implemented by all subclasses
        """
        pass
    
    def validate_input(self, **kwargs):
        """
        Validate input parameters
        Override in subclasses for specific validation
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return True
    
    def log_info(self, message):
        """Log info message"""
        self.logger.info(f"[{self.name}] {message}")
    
    def log_warning(self, message):
        """Log warning message"""
        self.logger.warning(f"[{self.name}] {message}")
    
    def log_error(self, message):
        """Log error message"""
        self.logger.error(f"[{self.name}] {message}")
    
    def log_debug(self, message):
        """Log debug message"""
        self.logger.debug(f"[{self.name}] {message}")
