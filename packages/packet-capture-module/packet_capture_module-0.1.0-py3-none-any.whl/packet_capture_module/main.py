"""
Main entry point for the Packet Capture Module.
Provides a clean, structured interface for the DPI system.
"""
import sys
import signal
import threading
import time
from collections import defaultdict
from typing import Optional, Dict, Any
from dataclasses import dataclass

from utils.logging_utils import (
    setup_logger, setup_system_logging, get_packet_logger, 
    log_system_stats, log_error_with_context
)
from utils.config_handler import get_config
from packet_capture_module.core.packet import Packet
from packet_capture_module.core.multicast_listener import MulticastListener
from packet_capture_module.core.filter_engine import FilterEngine
from packet_capture_module.core.packet_buffer import PacketBuffer


@dataclass
class SystemStats:
    """System statistics container"""
    total_packets_captured: int = 0
    total_packets_analyzed: int = 0
    total_packets_dropped: int = 0
    total_packets_logged: int = 0
    conversation_stats: Dict = None
    protocol_stats: Dict = None
    
    def __post_init__(self):
        if self.conversation_stats is None:
            self.conversation_stats = defaultdict(int)
        if self.protocol_stats is None:
            self.protocol_stats = defaultdict(int)


class PacketCaptureSystem:
    """
    Main packet capture system that orchestrates all components.
    Provides a clean, structured interface for the DPI system.
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the packet capture system with configuration"""
        # Load centralized configuration
        self.config = get_config(config_path)
        
        # Get configuration sections
        self.interface_config = self.config.get_interface_config()
        self.logging_config = self.config.get_logging_config()
        self.processing_config = self.config.get_processing_config()
        self.fault_tolerance_config = self.config.get_fault_tolerance_config()
        
        # Set up logging
        self._setup_logging()
        
        # Initialize components
        self.running = False
        self._shutdown_called = False  # Flag to prevent double shutdown
        self.listener: Optional[MulticastListener] = None
        self.buffer = PacketBuffer(config_path=config_path)
        self.filter_engine = FilterEngine(config_path=config_path)
        self.packet_logger = get_packet_logger(self.logging_config)
        
        # Statistics
        self.stats = SystemStats()
        
        # Threading
        self.processing_thread: Optional[threading.Thread] = None
        self.stats_thread: Optional[threading.Thread] = None
        
        self.logger.info(f"PacketCaptureSystem initialized with config: {config_path}")
    
    def _setup_logging(self) -> None:
        """Set up system logging and main logger"""
        # Set up system-wide logging
        setup_system_logging(self.logging_config)
        
        # Set up main system logger (without console output to avoid duplication)
        self.logger = setup_logger(
            name="packet_capture_system",
            log_level="INFO",
            console_output=False,  # Disable console output to avoid duplication
            file_output=f"system_{self.logging_config.log_file}"
        )
    
    def initialize(self) -> bool:
        """Initialize the system components"""
        try:
            # Verify interface availability using config handler
            if not self.config.verify_interface_availability():
                print(f"❌ Error: Interface {self.interface_config.interface} is not available or not up")
                return False
            
            # Initialize multicast listener
            self.listener = MulticastListener(
                interface=self.interface_config.interface,
                multicast_ips=self.interface_config.multicast_ips,
                ports=self.interface_config.ports,
                config_path=self.config.config_path
            )
            
            print(f"✅ System initialized successfully on interface: {self.interface_config.interface}")
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            return False
    
    def _update_statistics(self, packet: Packet) -> None:
        """Update system statistics with packet information"""
        # Update conversation statistics
        conv_key = (
            packet.src_ip, packet.src_port, 
            packet.dst_ip, packet.dst_port, 
            packet.get_protocol()
        )
        self.stats.conversation_stats[conv_key] += 1
        
        # Update protocol statistics
        self.stats.protocol_stats[packet.get_protocol()] += 1
    
    def packet_handler(self, packet: Packet) -> None:
        """Handle incoming packets from the multicast listener"""
        try:
            self.stats.total_packets_captured += 1
            
            # Update statistics
            self._update_statistics(packet)
            
            # Apply filtering
            filter_result = self.filter_engine.apply_filter(packet)
            if filter_result:
                # Add to buffer for processing
                buffer_result = self.buffer.add_packet(packet)
                if buffer_result:
                    # Log packet if enabled
                    if self.packet_logger:
                        self.packet_logger.log_packet(packet)
                        self.stats.total_packets_logged += 1
                else:
                    self.stats.total_packets_dropped += 1
                    print(f"⚠️  Packet dropped by buffer: {packet.src_ip}:{packet.src_port} -> {packet.dst_ip}:{packet.dst_port} [{packet.get_protocol()}]")
            else:
                self.stats.total_packets_dropped += 1
                print(f"⚠️  Packet dropped by filter: {packet.src_ip}:{packet.src_port} -> {packet.dst_ip}:{packet.dst_port} [{packet.get_protocol()}]")
                
        except Exception as e:
            print(f"❌ Error handling packet: {e}")
    
    def process_buffer(self) -> None:
        """Process packets from the buffer"""
        while self.running:
            try:
                packet = self.buffer.get_next_packet()
                if packet:
                    self.stats.total_packets_analyzed += 1
                    self._analyze_packet(packet)
                
                time.sleep(self.processing_config.interval_sec)
                
            except Exception as e:
                print(f"❌ Buffer processing error: {e}")
    
    def _analyze_packet(self, packet: Packet) -> None:
        """Analyze a packet (placeholder for DPI analysis)"""
        # This is where you would implement your DPI analysis logic
        # For now, we just log basic packet information
        pass
    
    def _get_simple_statistics(self) -> str:
        """Get simple one-line statistics for console output"""
        buffer_stats = self.buffer.get_stats()
        drop_rate = (self.stats.total_packets_dropped / self.stats.total_packets_captured * 100) if self.stats.total_packets_captured > 0 else 0
        
        return (f"📊 Captured: {self.stats.total_packets_captured:,} | "
                f"Analyzed: {self.stats.total_packets_analyzed:,} | "
                f"Dropped: {self.stats.total_packets_dropped:,} ({drop_rate:.1f}%) | "
                f"Buffer: {buffer_stats['usage_percentage']:.1f}% | "
                f"Logged: {self.stats.total_packets_logged:,}")
    
    def log_statistics(self) -> None:
        """Log system statistics periodically (simplified one-line output)"""
        while self.running:
            try:
                # Print simple one-line statistics
                print(self._get_simple_statistics())
                time.sleep(3.0)  # Print every 3 seconds
                
            except Exception as e:
                print(f"❌ Statistics logging error: {e}")
    
    def reload_configuration(self) -> None:
        """Reload configuration from file and update components"""
        try:
            print("🔄 Reloading configuration...")
            
            # Reload main configuration
            self.config.reload_config()
            
            # Update configuration sections
            self.interface_config = self.config.get_interface_config()
            self.logging_config = self.config.get_logging_config()
            self.processing_config = self.config.get_processing_config()
            
            # Update component configurations
            self.buffer.reload_config()
            self.filter_engine.reload_config()
            
            # Update packet logger
            self.packet_logger = get_packet_logger(self.logging_config)
            
            print("✅ Configuration reloaded successfully")
            
        except Exception as e:
            print(f"❌ Failed to reload configuration: {e}")
    
    def _start_background_threads(self) -> None:
        """Start background processing threads"""
        self.processing_thread = threading.Thread(
            target=self.process_buffer, 
            name="PacketProcessor",
            daemon=True
        )
        self.stats_thread = threading.Thread(
            target=self.log_statistics, 
            name="StatsLogger",
            daemon=True
        )
        
        self.processing_thread.start()
        self.stats_thread.start()
    
    def _wait_for_threads(self) -> None:
        """Wait for background threads to finish"""
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=5)
        
        if self.stats_thread and self.stats_thread.is_alive():
            self.stats_thread.join(timeout=5)
    
    def _format_statistics_output(self) -> str:
        """Format statistics for console output"""
        lines = []
        lines.append("=" * 50)
        lines.append("PACKET CAPTURE SYSTEM - FINAL STATISTICS")
        lines.append("=" * 50)
        
        # Capture statistics
        lines.append(f"\n📊 CAPTURE STATISTICS:")
        lines.append(f"   Total packets captured: {self.stats.total_packets_captured:,}")
        lines.append(f"   Total packets analyzed: {self.stats.total_packets_analyzed:,}")
        lines.append(f"   Total packets dropped: {self.stats.total_packets_dropped:,}")
        lines.append(f"   Total packets logged: {self.stats.total_packets_logged:,}")
        
        if self.stats.total_packets_captured > 0:
            drop_rate = (self.stats.total_packets_dropped / self.stats.total_packets_captured) * 100
            lines.append(f"   Drop rate: {drop_rate:.2f}%")
        
        # Protocol distribution
        lines.append(f"\n🌐 PROTOCOL DISTRIBUTION:")
        for protocol, count in sorted(
            self.stats.protocol_stats.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]:
            percentage = (count / self.stats.total_packets_captured * 100) if self.stats.total_packets_captured > 0 else 0
            lines.append(f"   {protocol}: {count:,} packets ({percentage:.1f}%)")
        
        # Top conversations
        lines.append(f"\n💬 TOP CONVERSATIONS:")
        top_conversations = sorted(
            self.stats.conversation_stats.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        for conv, count in top_conversations:
            src_ip, src_port, dst_ip, dst_port, protocol = conv
            lines.append(f"   {src_ip}:{src_port} → {dst_ip}:{dst_port} [{protocol}]: {count:,} packets")
        
        lines.append("\n" + "=" * 50)
        return "\n".join(lines)
    
    def print_final_statistics(self) -> None:
        """Print comprehensive statistics at shutdown"""
        print(self._format_statistics_output())
    
    def start(self) -> None:
        """Start the packet capture system"""
        if not self.initialize():
            print("❌ Failed to initialize system")
            sys.exit(1)
        
        self.running = True
        
        # Start background threads
        self._start_background_threads()
        
        try:
            # Start packet capture
            with self.listener as listener:
                self._log_startup_info()
                listener.start_capture(self.packet_handler)
                
                print("🎯 Packet capture system is running. Press Ctrl+C to stop...")
                
                # Main loop
                while self.running:
                    time.sleep(0.5)
                    
        except KeyboardInterrupt:
            print("\n⏹️  Received interrupt signal")
        except Exception as e:
            print(f"❌ Main capture loop error: {e}")
        finally:
            self.shutdown()
    
    def _log_startup_info(self) -> None:
        """Log startup information"""
        print(f"🚀 Starting capture on interface: {self.interface_config.interface}")
        print(f"📡 Monitoring multicast IPs: {self.interface_config.multicast_ips}")
        print(f"🔌 Monitoring ports: {self.interface_config.ports}")
        
        # Show filter information
        filter_config = self.config.get_filter_config()
        if filter_config.enable:
            active_filters = self.filter_engine.get_active_filters()
            print(f"🔍 Active filters ({len(active_filters)}): {active_filters}")
        else:
            print("🔍 Filtering is disabled")
    
    def shutdown(self) -> None:
        """Shutdown the system gracefully"""
        # Prevent double shutdown
        if self._shutdown_called:
            return
        self._shutdown_called = True
        
        print("🛑 Shutting down packet capture system...")
        
        self.running = False
        
        # Stop capture
        if self.listener:
            self.listener.stop_capture()
        
        # Wait for threads to finish
        self._wait_for_threads()
        
        # Print final statistics
        self.print_final_statistics()
        
        print("✅ Packet capture system stopped")


def main():
    """Main entry point"""
    # Create system instance
    system = PacketCaptureSystem()
    
    # Set up signal handlers
    def signal_handler(signum, frame):
        print(f"📡 Received signal {signum}")
        system.shutdown()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the system
    system.start()


if __name__ == "__main__":
    main()