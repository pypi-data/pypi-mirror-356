"""Logging configuration for Azure Pricing MCP Server.

This module provides comprehensive logging functionality with environment variable configuration.
"""

import asyncio
import json
import logging
import logging.handlers
import os
import sys
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union


class MCPFormatter(logging.Formatter):
    """Custom formatter for MCP server logs with structured output."""
    
    def __init__(self, include_mcp_context: bool = True):
        """Initialize the formatter.
        
        Args:
            include_mcp_context: Whether to include MCP-specific context in logs
        """
        self.include_mcp_context = include_mcp_context
        super().__init__()
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with structured information."""
        # Create base log entry
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add MCP-specific context if available
        if self.include_mcp_context and hasattr(record, 'mcp_context'):
            log_entry['mcp_context'] = record.mcp_context
        
        # Add request/response data if available
        if hasattr(record, 'request_data'):
            log_entry['request_data'] = record.request_data
        
        if hasattr(record, 'response_data'):
            log_entry['response_data'] = record.response_data
        
        # Add execution time if available
        if hasattr(record, 'execution_time'):
            log_entry['execution_time_ms'] = record.execution_time
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Format as JSON for structured logging or plain text for console
        if os.getenv('MCP_LOG_FORMAT', 'json').lower() == 'json':
            return json.dumps(log_entry, default=str, ensure_ascii=False)
        else:
            # Plain text format for console readability
            msg = f"[{log_entry['timestamp']}] {log_entry['level']} - {log_entry['message']}"
            if 'mcp_context' in log_entry:
                msg += f" | Context: {log_entry['mcp_context']}"
            if 'execution_time_ms' in log_entry:
                msg += f" | Time: {log_entry['execution_time_ms']}ms"
            return msg


class MCPLogger:
    """Enhanced logger for MCP server with request/response tracking."""
    
    def __init__(self, name: str):
        """Initialize the MCP logger.
        
        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up logging configuration based on environment variables."""
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Get configuration from environment variables
        debug_logging = os.getenv('MCP_DEBUG_LOGGING', 'false').lower() == 'true'
        log_level = os.getenv('MCP_LOG_LEVEL', 'INFO').upper()
        log_file = os.getenv('MCP_LOG_FILE')
        log_format = os.getenv('MCP_LOG_FORMAT', 'json').lower()
        
        # Set log level
        level = getattr(logging, log_level, logging.INFO)
        if debug_logging:
            level = logging.DEBUG
        
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = MCPFormatter(include_mcp_context=debug_logging)
        
        # IMPORTANT: Only add console handler if no log file is specified
        # This prevents interference with MCP protocol on stdout
        if not log_file:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        else:
            # If log file is specified, send console output to stderr to avoid MCP protocol interference
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(logging.WARNING)  # Only warnings and errors to stderr
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                
                # Use rotating file handler to prevent huge log files
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=10 * 1024 * 1024,  # 10MB
                    backupCount=5
                )
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
                
                # Log to stderr instead of stdout to avoid MCP protocol interference
                print(f"Azure Pricing MCP Server: Logging to file: {log_file}", file=sys.stderr)
            except Exception as e:
                print(f"Azure Pricing MCP Server: Failed to set up file logging: {e}", file=sys.stderr)
        
        # Log configuration to stderr to avoid MCP protocol interference
        print(f"Azure Pricing MCP Server: Logging configured - Level: {log_level}, Debug: {debug_logging}, Format: {log_format}", file=sys.stderr)
    
    def log_request(self, tool_name: str, request_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None):
        """Log an incoming MCP request.
        
        Args:
            tool_name: Name of the MCP tool being called
            request_data: Request parameters
            context: Additional context information
        """
        extra = {
            'mcp_context': {
                'type': 'request',
                'tool': tool_name,
                'timestamp': datetime.now().isoformat()
            },
            'request_data': request_data
        }
        
        if context:
            extra['mcp_context'].update(context)
        
        self.logger.info(f"MCP Request: {tool_name}", extra=extra)
    
    def log_response(self, tool_name: str, response_data: Dict[str, Any], execution_time: Optional[float] = None, context: Optional[Dict[str, Any]] = None):
        """Log an MCP response.
        
        Args:
            tool_name: Name of the MCP tool that was called
            response_data: Response data
            execution_time: Execution time in milliseconds
            context: Additional context information
        """
        extra = {
            'mcp_context': {
                'type': 'response',
                'tool': tool_name,
                'timestamp': datetime.now().isoformat()
            },
            'response_data': response_data
        }
        
        if execution_time is not None:
            extra['execution_time'] = execution_time
        
        if context:
            extra['mcp_context'].update(context)
        
        self.logger.info(f"MCP Response: {tool_name}", extra=extra)
    
    def log_internal_process(self, process_name: str, data: Dict[str, Any], level: str = 'DEBUG'):
        """Log internal MCP processes.
        
        Args:
            process_name: Name of the internal process
            data: Process data
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        extra = {
            'mcp_context': {
                'type': 'internal_process',
                'process': process_name,
                'timestamp': datetime.now().isoformat()
            },
            'request_data': data
        }
        
        log_method = getattr(self.logger, level.lower(), self.logger.debug)
        log_method(f"MCP Internal: {process_name}", extra=extra)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(message, **kwargs)


def log_mcp_tool(logger: MCPLogger):
    """Decorator to automatically log MCP tool requests and responses.
    
    Args:
        logger: MCPLogger instance
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            tool_name = func.__name__
            start_time = time.time()
            
            # Log request
            request_data = {
                'args': args,
                'kwargs': kwargs
            }
            logger.log_request(tool_name, request_data)
            
            try:
                # Execute the function
                result = await func(*args, **kwargs)
                
                # Calculate execution time
                execution_time = (time.time() - start_time) * 1000
                
                # Log response
                logger.log_response(tool_name, result, execution_time)
                
                return result
                
            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                error_response = {
                    'status': 'error',
                    'error': str(e),
                    'type': type(e).__name__
                }
                
                logger.log_response(tool_name, error_response, execution_time)
                logger.error(f"Error in {tool_name}: {e}", exc_info=True)
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            tool_name = func.__name__
            start_time = time.time()
            
            # Log request
            request_data = {
                'args': args,
                'kwargs': kwargs
            }
            logger.log_request(tool_name, request_data)
            
            try:
                # Execute the function
                result = func(*args, **kwargs)
                
                # Calculate execution time
                execution_time = (time.time() - start_time) * 1000
                
                # Log response
                logger.log_response(tool_name, result, execution_time)
                
                return result
                
            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                error_response = {
                    'status': 'error',
                    'error': str(e),
                    'type': type(e).__name__
                }
                
                logger.log_response(tool_name, error_response, execution_time)
                logger.error(f"Error in {tool_name}: {e}", exc_info=True)
                raise
        
        # Return appropriate wrapper based on whether function is async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Global logger instance
mcp_logger = MCPLogger('azure_pricing_mcp_server')
