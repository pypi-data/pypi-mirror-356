"""
Logging utilities for vHTML processing.
"""
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime

class VHTMLLogger:
    """Custom logger for vHTML processing."""
    
    def __init__(self, log_dir: str = "logs", log_level: int = logging.INFO):
        """Initialize the logger.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (default: INFO)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        self.logger = logging.getLogger('vhtml')
        self.logger.setLevel(log_level)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            
            # File handler for all logs
            log_file = self.log_dir / 'vhtml_processing.log'
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def get_document_logger(self, document_path: str, output_dir: Optional[str] = None) -> logging.Logger:
        """Get a logger for a specific document.
        
        Args:
            document_path: Path to the document being processed
            output_dir: Directory where the document will be saved (default: same as log_dir)
            
        Returns:
            Configured logger instance for the document
        """
        doc_path = Path(document_path)
        doc_name = doc_path.stem
        
        # Create a logger for this document
        doc_logger = logging.getLogger(f'vhtml.{doc_name}')
        doc_logger.setLevel(self.logger.level)
        
        # Determine log file path
        if output_dir:
            output_dir = Path(output_dir)
            #output_dir.mkdir(parents=True, exist_ok=True)
            log_file = output_dir / f'{doc_name}.log'
        else:
            log_file = self.log_dir / f'{doc_name}.log'
        
        # Add file handler if not already added
        if not any(isinstance(h, logging.FileHandler) for h in doc_logger.handlers):
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(self.logger.level)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            doc_logger.addHandler(file_handler)
        
        return doc_logger
    
    def log_processing_start(self, document_path: str, output_dir: str, **kwargs):
        """Log the start of document processing."""
        doc_logger = self.get_document_logger(document_path, output_dir)
        doc_logger.info(f"Starting processing of document: {document_path}")
        doc_logger.info(f"Output directory: {output_dir}")
        if kwargs:
            doc_logger.info("Processing parameters: %s", json.dumps(kwargs, indent=2, default=str))
    
    def log_processing_stage(self, document_path: str, stage: str, message: str, **extra):
        """Log a processing stage with additional context."""
        doc_logger = self.get_document_logger(document_path)
        log_message = f"[{stage.upper()}] {message}"
        if extra:
            log_message += f"\n{json.dumps(extra, indent=2, default=str)}"
        doc_logger.info(log_message)
    
    def log_processing_end(self, document_path: str, result: Dict[str, Any]):
        """Log the end of document processing with results."""
        doc_logger = self.get_document_logger(document_path)
        doc_logger.info("Processing completed successfully")
        doc_logger.info("Processing results: %s", json.dumps({
            k: v for k, v in result.items() if k != 'metadata'
        }, indent=2, default=str))
    
    def log_error(self, document_path: str, error: Exception, context: str = None):
        """Log an error that occurred during processing."""
        doc_logger = self.get_document_logger(document_path)
        error_msg = f"Error during processing: {str(error)}"
        if context:
            error_msg = f"{context}: {error_msg}"
        doc_logger.error(error_msg, exc_info=True)

# Global logger instance
logger = VHTMLLogger()

def setup_logging(log_level: int = logging.INFO, log_dir: str = "logs"):
    """Set up the global logger.
    
    Args:
        log_level: Logging level (default: INFO)
        log_dir: Directory to store log files
    """
    global logger
    logger = VHTMLLogger(log_dir=log_dir, log_level=log_level)
    return logger
