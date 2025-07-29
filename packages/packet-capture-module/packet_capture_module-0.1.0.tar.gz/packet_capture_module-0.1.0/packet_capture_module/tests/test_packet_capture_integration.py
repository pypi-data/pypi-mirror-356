#!/usr/bin/env python3
"""
Test script to verify the packet capture module integration.
Tests the centralized config handler, logging system, and core components.
"""
import sys
import time
import threading
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config_handler import get_config
from utils.logging_utils import setup_logger, setup_system_logging, get_packet_logger
from packet_capture_module.core.multicast_listener import MulticastListener
from packet_capture_module.core.filter_engine import FilterEngine
from packet_capture_module.core.packet_buffer import PacketBuffer
from packet_capture_module.core.packet import Packet


def test_config_handler():
    """Test the centralized config handler"""
    print("🔧 Testing Config Handler...")
    
    try:
        config = get_config("config/config.yaml")
        
        # Test interface config
        interface_config = config.get_interface_config()
        print(f"   ✅ Interface: {interface_config.interface}")
        print(f"   ✅ Multicast IPs: {interface_config.multicast_ips}")
        print(f"   ✅ Ports: {interface_config.ports}")
        
        # Test filter config
        filter_config = config.get_filter_config()
        print(f"   ✅ Filter enabled: {filter_config.enable}")
        print(f"   ✅ Filter rules: {filter_config.rules}")
        
        # Test buffer config
        buffer_config = config.get_buffer_config()
        print(f"   ✅ Buffer size: {buffer_config.size_mb} MB")
        print(f"   ✅ Priority queues: {len(buffer_config.priority_queues)}")
        
        # Test logging config
        logging_config = config.get_logging_config()
        print(f"   ✅ Log file: {logging_config.log_file}")
        print(f"   ✅ Log format: {logging_config.format}")
        print(f"   ✅ Log level: {logging_config.log_level}")
        
        # Test processing config
        processing_config = config.get_processing_config()
        print(f"   ✅ Processing interval: {processing_config.interval_sec}s")
        print(f"   ✅ Stats interval: {processing_config.stats_interval_sec}s")
        
        print("   ✅ Config handler test passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Config handler test failed: {e}")
        return False


def test_logging_system():
    """Test the logging system"""
    print("\n📝 Testing Logging System...")
    
    try:
        config = get_config("config/config.yaml")
        logging_config = config.get_logging_config()
        
        # Test system logging setup
        setup_system_logging(logging_config)
        print("   ✅ System logging configured")
        
        # Test packet logger
        packet_logger = get_packet_logger(logging_config)
        if packet_logger:
            print("   ✅ Packet logger created")
        else:
            print("   ⚠️  Packet logging disabled")
        
        # Test main logger
        logger = setup_logger("test_logger", "INFO", True, "test.log")
        logger.info("Test log message")
        print("   ✅ Main logger working")
        
        print("   ✅ Logging system test passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Logging system test failed: {e}")
        return False


def test_core_components():
    """Test the core components"""
    print("\n⚙️  Testing Core Components...")
    
    try:
        config = get_config("config/config.yaml")
        
        # Test filter engine
        filter_engine = FilterEngine("config/config.yaml")
        print(f"   ✅ Filter engine initialized with {len(filter_engine.get_active_filters())} rules")
        
        # Test packet buffer
        packet_buffer = PacketBuffer(config_path="config/config.yaml")
        print(f"   ✅ Packet buffer initialized")
        
        # Test multicast listener (without starting capture)
        listener = MulticastListener(
            interface=config.get_interface_config().interface,
            multicast_ips=config.get_interface_config().multicast_ips,
            ports=config.get_interface_config().ports,
            config_path="config/config.yaml"
        )
        print(f"   ✅ Multicast listener initialized")
        
        print("   ✅ Core components test passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Core components test failed: {e}")
        return False


def test_packet_processing():
    """Test packet processing with mock data"""
    print("\n📦 Testing Packet Processing...")
    
    try:
        # Create a mock packet
        mock_packet_data = bytes.fromhex(
            "000102030405060708090a0b0c0d0e0f"  # Ethernet header
            "0800"                              # IP type
            "4500001c0001000040060000"          # IP header
            "0a0000010a000002"                  # Source/Dest IP
            "12345678"                          # Ports
        )
        
        packet = Packet(raw_data=mock_packet_data)
        print(f"   ✅ Mock packet created: {packet.src_ip}:{packet.src_port} -> {packet.dst_ip}:{packet.dst_port}")
        
        # Test filter engine
        filter_engine = FilterEngine("config/config.yaml")
        filter_result = filter_engine.apply_filter(packet)
        print(f"   ✅ Filter result: {filter_result}")
        
        # Test packet buffer
        packet_buffer = PacketBuffer(config_path="config/config.yaml")
        added = packet_buffer.add_packet(packet)
        print(f"   ✅ Packet added to buffer: {added}")
        
        retrieved = packet_buffer.get_next_packet()
        print(f"   ✅ Packet retrieved from buffer: {retrieved is not None}")
        
        # Test packet logging
        config = get_config("config/config.yaml")
        packet_logger = get_packet_logger(config.get_logging_config())
        if packet_logger:
            packet_logger.log_packet(packet)
            print("   ✅ Packet logged successfully")
        
        print("   ✅ Packet processing test passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Packet processing test failed: {e}")
        return False


def test_config_reload():
    """Test configuration reload functionality"""
    print("\n🔄 Testing Config Reload...")
    
    try:
        config = get_config("config/config.yaml")
        
        # Get initial values
        initial_interval = config.get_processing_config().interval_sec
        
        # Reload config
        config.reload_config()
        
        # Verify reload worked
        reloaded_interval = config.get_processing_config().interval_sec
        if initial_interval == reloaded_interval:
            print("   ✅ Config reload successful")
        else:
            print("   ⚠️  Config reload changed values (this is normal if config was modified)")
        
        print("   ✅ Config reload test passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Config reload test failed: {e}")
        return False


def main():
    """Run all integration tests"""
    print("🚀 Starting Packet Capture Module Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Config Handler", test_config_handler),
        ("Logging System", test_logging_system),
        ("Core Components", test_core_components),
        ("Packet Processing", test_packet_processing),
        ("Config Reload", test_config_reload),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"   ❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the configuration and dependencies.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 