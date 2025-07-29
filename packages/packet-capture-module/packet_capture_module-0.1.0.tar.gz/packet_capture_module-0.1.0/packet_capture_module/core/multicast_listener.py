"""
Multicast Listener implementation for Linux using pyshark with centralized config support.
"""
import threading
import time
import os
from typing import Callable, Optional, Dict, Any
from pathlib import Path
import pyshark
from packet_capture_module.core.packet import Packet
from utils.logging_utils import setup_logger
from utils.config_handler import get_config

logger = setup_logger("multicast_listener")

class MulticastListener:
    def __init__(
        self,
        interface: Optional[str] = None,
        multicast_ips: Optional[list] = None,
        ports: Optional[list] = None,
        config_path: Optional[str] = None,
    ):
        """
        Initialize multicast listener with centralized config support.
        
        Args:
            interface: Network interface to listen on (overrides config)
            multicast_ips: List of multicast IPs to filter (overrides config)
            ports: List of ports to filter (overrides config)
            config_path: Path to YAML config file (optional, uses default if not provided)
        """
        # Load centralized configuration
        self.config = get_config(config_path or "config/config.yaml")
        self.interface_config = self.config.get_interface_config()
        
        # Override with explicit parameters if provided
        if interface:
            self.interface_config.interface = interface
        if multicast_ips:
            self.interface_config.multicast_ips = multicast_ips
        if ports:
            self.interface_config.ports = ports
            
        # Initialize other members
        self.capture = None
        self.capture_thread = None
        self.running = False
        self.callback = None
        self._lock = threading.Lock()
        
        logger.info(f"Initialized MulticastListener with interface: {self.interface_config.interface}")
    
    def __enter__(self):
        """Context manager entry point."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        Ensures resources are cleaned up even if an exception occurs.
        """
        self.stop_capture()
        if exc_type is not None:
            logger.error(f"Exception occurred: {exc_val}", exc_info=(exc_type, exc_val, exc_tb))
        return False

    def _generate_bpf_filter(self) -> str:
        """Generate BPF filter from configuration."""
        filters = []
        
        # IP filters
        if self.interface_config.multicast_ips:
            ip_filters = []
            for ip in self.interface_config.multicast_ips:
                if ':' in ip:  # IPv6
                    ip_filters.append(f'dst host {ip}')
                else:  # IPv4
                    ip_filters.append(f'dst host {ip}')
            filters.append(f'({" or ".join(ip_filters)})')
        
        # Port filters
        if self.interface_config.ports:
            port_filters = [f'dst port {port}' for port in self.interface_config.ports]
            filters.append(f'({" or ".join(port_filters)})')
        
        return ' && '.join(filters) if filters else '(ip multicast || ip6 multicast)'

    def start_capture(self, callback: Callable[[Packet], None]) -> bool:
        """
        Start multicast packet capture with configured settings.
        """
        if self.running:
            logger.warning("Capture already running")
            return False

        try:
            bpf_filter = self._generate_bpf_filter()
            logger.info(f"Starting capture with BPF filter: {bpf_filter}")
            
            # Get processing config for capture options
            processing_config = self.config.get_processing_config()
            
            self.capture = pyshark.LiveCapture(
                interface=self.interface_config.interface,
                bpf_filter=bpf_filter,
                use_json=True,
                include_raw=True,
                display_filter=''
            )
            
            self.callback = callback
            self.running = True
            self.capture_thread = threading.Thread(
                target=self._capture_loop,
                name=f"MulticastListener-{self.interface_config.interface}",
                daemon=True
            )
            self.capture_thread.start()
            
            time.sleep(0.2)
            if not self.capture_thread.is_alive():
                raise RuntimeError("Capture thread failed to start")
                
            logger.info(
                f"Started multicast capture on {self.interface_config.interface}\n"
                f"Multicast IPs: {self.interface_config.multicast_ips}\n"
                f"Ports: {self.interface_config.ports}"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to start capture: {e}", exc_info=True)
            self.stop_capture()
            return False

    def _capture_loop(self):
        """Main capture loop running in background thread."""
        try:
            for pyshark_packet in self.capture.sniff_continuously(packet_count=0):
                if not self.running:
                    break
                    
                try:
                    if not hasattr(pyshark_packet, 'frame_raw'):
                        continue
                        
                    raw_data = bytes.fromhex(pyshark_packet.frame_raw.value)
                    packet = Packet(raw_data=raw_data)
                    
                    # Add metadata
                    with self._lock:
                        packet.metadata.update({
                            'capture_time': pyshark_packet.sniff_time.timestamp(),
                            'interface': self.interface_config.interface,
                            'packet_length': len(raw_data)
                        })
                    
                    if self.callback:
                        self.callback(packet)
                        
                except Exception as e:
                    logger.error(f"Error processing packet: {e}", exc_info=True)
                    
        except Exception as e:
            logger.error(f"Capture loop error: {e}", exc_info=True)
        finally:
            self.stop_capture()

    def stop_capture(self):
        """Stop the capture and clean up resources."""
        with self._lock:
            if not self.running:
                return
                
            self.running = False
            
            try:
                if self.capture:
                    self.capture.close()
            except Exception as e:
                logger.error(f"Error closing capture: {e}", exc_info=True)
            
            try:
                if (self.capture_thread and 
                    threading.current_thread() is not self.capture_thread and
                    self.capture_thread.is_alive()):
                    self.capture_thread.join(timeout=5)
                    if self.capture_thread.is_alive():
                        logger.warning("Capture thread did not stop cleanly")
            except Exception as e:
                logger.error(f"Error joining thread: {e}", exc_info=True)
                
            logger.info("Multicast capture stopped")

    @property
    def current_config(self) -> Dict[str, Any]:
        """Get current configuration as dictionary."""
        return {
            'interface': self.interface_config.interface,
            'multicast_ips': self.interface_config.multicast_ips,
            'ports': self.interface_config.ports
        }

    def __del__(self):
        """Destructor to ensure cleanup."""
        self.stop_capture()