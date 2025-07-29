import os
import yaml
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path

@dataclass
class InterfaceConfig:
    """Configuration for network interface and multicast settings"""
    interface: str
    multicast_ips: List[str]
    ports: Optional[List[int]]

@dataclass
class FilterConfig:
    """Configuration for packet filtering"""
    enable: bool
    rules: List[str]

@dataclass
class BufferConfig:
    """Configuration for packet buffer"""
    size_mb: int
    auto_delete_threshold: int
    checkpoint_interval_sec: int
    priority_queues: Dict[int, str]

@dataclass
class LoggingConfig:
    """Configuration for logging system"""
    log_file: str
    format: str
    max_size_mb: int
    rotation: int
    enable_packet_logging: bool
    log_level: str

@dataclass
class ProcessingConfig:
    """Configuration for packet processing"""
    interval_sec: float
    stats_interval_sec: float

@dataclass
class FaultToleranceConfig:
    """Configuration for fault tolerance and recovery"""
    auto_restart: bool
    max_restart_attempts: int
    restart_cooldown_sec: int

@dataclass
class DPIConfig:
    """Configuration for DPI analysis"""
    signature_database_path: str
    enable_pattern_matching: bool
    batch_size: int
    processing_interval: float
    max_queue_size: int
    result_timeout: float
    enable_background_processing: bool

class ConfigValidationError(Exception):
    """Raised when configuration validation fails"""
    pass

class Config:
    """
    Centralized configuration management class that loads YAML once
    and provides typed, validated access to configuration sections.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self._raw_config: Dict[str, Any] = {}
        self._interface_config: Optional[InterfaceConfig] = None
        self._filter_config: Optional[FilterConfig] = None
        self._buffer_config: Optional[BufferConfig] = None
        self._logging_config: Optional[LoggingConfig] = None
        self._processing_config: Optional[ProcessingConfig] = None
        self._fault_tolerance_config: Optional[FaultToleranceConfig] = None
        self._dpi_config: Optional[DPIConfig] = None
        
        self.load_config()
    
    def load_config(self) -> None:
        """Load and validate the YAML configuration file"""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise ConfigValidationError(f"Configuration file not found: {self.config_path}")
            
            with open(config_file, 'r') as f:
                self._raw_config = yaml.safe_load(f) or {}
            
            self._validate_config()
            
        except yaml.YAMLError as e:
            raise ConfigValidationError(f"Invalid YAML syntax in {self.config_path}: {e}")
        except Exception as e:
            raise ConfigValidationError(f"Error loading config: {e}")
    
    def _validate_config(self) -> None:
        """Validate the loaded configuration"""
        required_sections = ['interface', 'multicast_ips']
        
        for section in required_sections:
            if section not in self._raw_config:
                raise ConfigValidationError(f"Missing required configuration section: {section}")
        
        # Validate interface is not empty
        if not self._raw_config.get('interface'):
            raise ConfigValidationError("Interface name cannot be empty")
        
        # Validate multicast IPs
        multicast_ips = self._raw_config.get('multicast_ips', [])
        if not isinstance(multicast_ips, list):
            raise ConfigValidationError("multicast_ips must be a list")
    
    def get_interface_config(self) -> InterfaceConfig:
        """Get interface and multicast configuration"""
        if self._interface_config is None:
            # Handle ports - can be None, empty list, or list of integers
            ports_raw = self._raw_config.get('ports')
            ports = None
            if ports_raw is not None and ports_raw != "None":
                if isinstance(ports_raw, list):
                    ports = [int(p) for p in ports_raw]
                else:
                    ports = [int(ports_raw)]
            
            self._interface_config = InterfaceConfig(
                interface=self._raw_config['interface'],
                multicast_ips=self._raw_config.get('multicast_ips', []),
                ports=ports
            )
        
        return self._interface_config
    
    def get_filter_config(self) -> FilterConfig:
        """Get filter engine configuration"""
        if self._filter_config is None:
            filter_section = self._raw_config.get('filter', {})
            
            self._filter_config = FilterConfig(
                enable=filter_section.get('enable', True),
                rules=filter_section.get('rules', [])
            )
        
        return self._filter_config
    
    def get_buffer_config(self) -> BufferConfig:
        """Get packet buffer configuration"""
        if self._buffer_config is None:
            buffer_section = self._raw_config.get('buffer', {})
            
            # Handle priority queues with proper defaults
            priority_queues = buffer_section.get('priority_queues', {})
            if isinstance(priority_queues, dict):
                # Convert string keys to integers if needed
                priority_queues = {int(k): v for k, v in priority_queues.items()}
            else:
                priority_queues = {}
            
            self._buffer_config = BufferConfig(
                size_mb=buffer_section.get('size_mb', 1000),
                auto_delete_threshold=buffer_section.get('auto_delete_threshold', 90),
                checkpoint_interval_sec=buffer_section.get('checkpoint_interval_sec', 300),
                priority_queues=priority_queues
            )
        
        return self._buffer_config
    
    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration"""
        if self._logging_config is None:
            logging_section = self._raw_config.get('logging', {})
            
            # Validate log format
            log_format = logging_section.get('format', 'json')
            if log_format not in ['json', 'csv', 'text']:
                raise ConfigValidationError(f"Invalid log format: {log_format}. Must be 'json', 'csv', or 'text'")
            
            self._logging_config = LoggingConfig(
                log_file=logging_section.get('log_file', 'packet_capture.log'),
                format=log_format,
                max_size_mb=logging_section.get('max_size_mb', 10),
                rotation=logging_section.get('rotation', 5),
                enable_packet_logging=logging_section.get('enable_packet_logging', True),
                log_level=logging_section.get('log_level', 'INFO')
            )
        
        return self._logging_config
    
    def get_processing_config(self) -> ProcessingConfig:
        """Get processing configuration"""
        if self._processing_config is None:
            processing_section = self._raw_config.get('processing', {})
            
            self._processing_config = ProcessingConfig(
                interval_sec=processing_section.get('interval_sec', 0.1),
                stats_interval_sec=processing_section.get('stats_interval_sec', 5.0)
            )
        
        return self._processing_config
    
    def get_fault_tolerance_config(self) -> FaultToleranceConfig:
        """Get fault tolerance configuration"""
        if self._fault_tolerance_config is None:
            ft_section = self._raw_config.get('fault_tolerance', {})
            
            self._fault_tolerance_config = FaultToleranceConfig(
                auto_restart=ft_section.get('auto_restart', True),
                max_restart_attempts=ft_section.get('max_restart_attempts', 3),
                restart_cooldown_sec=ft_section.get('restart_cooldown_sec', 30)
            )
        
        return self._fault_tolerance_config
    
    def get_dpi_config(self) -> DPIConfig:
        """Get DPI configuration"""
        if self._dpi_config is None:
            dpi_section = self._raw_config.get('dpi', {})
            
            self._dpi_config = DPIConfig(
                signature_database_path=dpi_section.get('signature_database_path', 'config/signatures/treat_signatures.json'),
                enable_pattern_matching=dpi_section.get('enable_pattern_matching', True),
                batch_size=dpi_section.get('batch_size', 10),
                processing_interval=dpi_section.get('processing_interval', 0.1),
                max_queue_size=dpi_section.get('max_queue_size', 1000),
                result_timeout=dpi_section.get('result_timeout', 1.0),
                enable_background_processing=dpi_section.get('enable_background_processing', True)
            )
        
        return self._dpi_config
    
    def get_raw_config(self) -> Dict[str, Any]:
        """Get the raw configuration dictionary (use sparingly)"""
        return self._raw_config.copy()
    
    def reload_config(self) -> None:
        """Reload the configuration from file"""
        # Clear cached configs
        self._interface_config = None
        self._filter_config = None
        self._buffer_config = None
        self._logging_config = None
        self._processing_config = None
        self._fault_tolerance_config = None
        self._dpi_config = None
        
        # Reload from file
        self.load_config()
    
    def verify_interface_availability(self) -> bool:
        """
        Verify that the configured interface is available.
        This is a utility method that can be used by the main system.
        """
        import subprocess
        try:
            interface = self.get_interface_config().interface
            result = subprocess.run(['ip', 'link', 'show', interface], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0 and 'UP' in result.stdout
        except Exception:
            return False
    
    # Convenience methods for main system
    def get_interface_name(self) -> str:
        """Get just the interface name"""
        return self.get_interface_config().interface
    
    def get_multicast_ips(self) -> List[str]:
        """Get just the multicast IPs list"""
        return self.get_interface_config().multicast_ips
    
    def get_ports(self) -> Optional[List[int]]:
        """Get just the ports list"""
        return self.get_interface_config().ports
    
    def is_filter_enabled(self) -> bool:
        """Check if filtering is enabled"""
        return self.get_filter_config().enable
    
    def get_filter_rules(self) -> List[str]:
        """Get just the filter rules"""
        return self.get_filter_config().rules
    
    def get_log_file_path(self) -> str:
        """Get absolute path to log file"""
        log_file = self.get_logging_config().log_file
        return os.path.abspath(log_file)
    
    def should_log_packets(self) -> bool:
        """Check if packet logging is enabled"""
        return self.get_logging_config().enable_packet_logging

# Global config instance - initialize once and reuse
_config_instance: Optional[Config] = None

def get_config(config_path: str = "config.yaml") -> Config:
    """
    Get the global configuration instance.
    Creates it once and reuses it across the application.
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance

def reload_global_config() -> None:
    """Reload the global configuration"""
    global _config_instance
    if _config_instance is not None:
        _config_instance.reload_config()