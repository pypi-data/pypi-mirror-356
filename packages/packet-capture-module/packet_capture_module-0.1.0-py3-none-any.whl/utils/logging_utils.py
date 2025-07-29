"""
Comprehensive logging utilities for the DPI system.
Handles both system logging and packet logging with rotation and different formats.
"""
import logging
import logging.handlers
import os
import json
import csv
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from packet_capture_module.core.packet import Packet


class PacketLogger:
    """Dedicated packet logger with rotation and multiple format support"""
    
    def __init__(self, log_file: str, format_type: str = "json", 
                 max_size_mb: int = 10, rotation_count: int = 5):
        self.log_file = Path(log_file).resolve()
        self.format_type = format_type.lower()
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.rotation_count = rotation_count
        
        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize CSV header if needed
        if self.format_type == "csv" and not self.log_file.exists():
            self._write_csv_header()

    def log_packet(self, packet: Packet) -> None:
        """Log packet information in specified format"""
        try:
            # Check if rotation is needed
            if self.log_file.exists() and self.log_file.stat().st_size > self.max_size_bytes:
                self._rotate_log_file()

            # Prepare packet data
            payload = packet.get_payload()
            payload_sample = payload[:64].hex() if payload else ""
            
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "src_ip": packet.src_ip,
                "dst_ip": packet.dst_ip,
                "src_port": packet.src_port,
                "dst_port": packet.dst_port,
                "protocol": packet.get_protocol(),
                "length": packet.get_size(),
                "payload_sample": payload_sample,
                "is_multicast": packet.is_multicast(),
                "metadata": packet.metadata
            }

            # Write in specified format
            if self.format_type == "json":
                self._write_json(log_data)
            elif self.format_type == "csv":
                self._write_csv(log_data)
            else:  # text format
                self._write_text(log_data)
                
        except Exception as e:
            # Use system logger for packet logging errors
            logging.getLogger("packet_logger").error(f"Error logging packet: {e}", exc_info=True)

    def _write_json(self, log_data: Dict[str, Any]) -> None:
        """Write log data in JSON format"""
        with open(self.log_file, "a", encoding='utf-8') as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + "\n")

    def _write_csv(self, log_data: Dict[str, Any]) -> None:
        """Write log data in CSV format"""
        # Flatten metadata for CSV
        flattened_data = log_data.copy()
        flattened_data.pop('metadata', None)
        
        with open(self.log_file, "a", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=flattened_data.keys())
            writer.writerow(flattened_data)

    def _write_text(self, log_data: Dict[str, Any]) -> None:
        """Write log data in human-readable text format"""
        line = (f"[{log_data['timestamp']}] "
                f"{log_data['src_ip']}:{log_data['src_port']} -> "
                f"{log_data['dst_ip']}:{log_data['dst_port']} "
                f"{log_data['protocol']} len={log_data['length']}")
        
        if log_data['is_multicast']:
            line += " [MULTICAST]"
        
        if log_data['payload_sample']:
            line += f" payload={log_data['payload_sample'][:32]}..."
            
        line += "\n"
        
        with open(self.log_file, "a", encoding='utf-8') as f:
            f.write(line)

    def _write_csv_header(self) -> None:
        """Write CSV header row"""
        headers = [
            "timestamp", "src_ip", "dst_ip", "src_port", "dst_port",
            "protocol", "length", "payload_sample", "is_multicast"
        ]
        
        with open(self.log_file, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def _rotate_log_file(self) -> None:
        """Rotate log files when size limit is reached"""
        try:
            # Remove oldest log file if it exists
            oldest_log = Path(f"{self.log_file}.{self.rotation_count}")
            if oldest_log.exists():
                oldest_log.unlink()

            # Shift existing log files
            for i in range(self.rotation_count - 1, 0, -1):
                old_file = Path(f"{self.log_file}.{i}")
                new_file = Path(f"{self.log_file}.{i + 1}")
                if old_file.exists():
                    old_file.rename(new_file)

            # Move current log to .1
            if self.log_file.exists():
                self.log_file.rename(Path(f"{self.log_file}.1"))

            # Recreate CSV header if needed
            if self.format_type == "csv":
                self._write_csv_header()
                
            logging.getLogger("packet_logger").info(f"Log file rotated: {self.log_file}")
            
        except Exception as e:
            logging.getLogger("packet_logger").error(f"Error rotating log file: {e}", exc_info=True)


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for better readability"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        log_message = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        return f"{color}{log_message}{self.COLORS['RESET']}"


def setup_logger(name: str, log_level: str = "INFO", 
                 console_output: bool = True, 
                 file_output: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with both console and file handlers.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Enable console output
        file_output: Optional file path for file output
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Console handler with colors
    if console_output:
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler with rotation
    if file_output:
        file_handler = logging.handlers.RotatingFileHandler(
            file_output, maxBytes=10*1024*1024, backupCount=5
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def setup_system_logging(logging_config) -> None:
    """
    Configure system-wide logging based on configuration.
    
    Args:
        logging_config: LoggingConfig object with logging settings
    """
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, logging_config.log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # System log file handler
    system_log_file = f"system_{logging_config.log_file}"
    file_handler = logging.handlers.RotatingFileHandler(
        system_log_file, 
        maxBytes=logging_config.max_size_mb * 1024 * 1024,
        backupCount=logging_config.rotation
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Suppress noisy third-party loggers
    logging.getLogger('pyshark').setLevel(logging.WARNING)
    logging.getLogger('scapy').setLevel(logging.WARNING)
    logging.getLogger('dpkt').setLevel(logging.WARNING)
    
    logging.info(f"System logging configured - Level: {logging_config.log_level}, File: {system_log_file}")


def get_packet_logger(logging_config) -> Optional[PacketLogger]:
    """
    Create and return a packet logger if packet logging is enabled.
    
    Args:
        logging_config: LoggingConfig object
        
    Returns:
        PacketLogger instance or None if disabled
    """
    if not logging_config.enable_packet_logging:
        return None
        
    return PacketLogger(
        log_file=logging_config.log_file,
        format_type=logging_config.format,
        max_size_mb=logging_config.max_size_mb,
        rotation_count=logging_config.rotation
    )


def log_system_stats(stats: Dict[str, Any], logger_name: str = "system_stats") -> None:
    """
    Log system statistics in a formatted way.
    
    Args:
        stats: Dictionary containing system statistics
        logger_name: Logger name to use
    """
    logger = logging.getLogger(logger_name)
    
    stats_lines = ["=== System Statistics ==="]
    for key, value in stats.items():
        if isinstance(value, dict):
            stats_lines.append(f"{key}:")
            for sub_key, sub_value in value.items():
                stats_lines.append(f"  {sub_key}: {sub_value}")
        else:
            stats_lines.append(f"{key}: {value}")
    
    logger.info("\n".join(stats_lines))


def log_error_with_context(logger: logging.Logger, error: Exception, 
                          context: str = "", packet: Optional[Packet] = None) -> None:
    """
    Log error with additional context information.
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context information
        packet: Optional packet that caused the error
    """
    error_msg = f"Error in {context}: {str(error)}"
    
    if packet and hasattr(packet, 'src_ip') and hasattr(packet, 'src_port') and hasattr(packet, 'dst_ip') and hasattr(packet, 'dst_port'):
        error_msg += f" [Packet: {packet.src_ip}:{packet.src_port} -> {packet.dst_ip}:{packet.dst_port}]"
    elif packet:
        error_msg += f" [Context: {packet}]"
    
    logger.error(error_msg, exc_info=True)