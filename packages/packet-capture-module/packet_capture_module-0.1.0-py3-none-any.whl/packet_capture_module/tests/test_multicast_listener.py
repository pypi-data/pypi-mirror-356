#!/usr/bin/env python3
"""
Comprehensive test suite for MulticastListener class.
Includes unit tests, integration tests, and demo functionality.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
import threading
import time
import sys
import os
from typing import List, Dict, Any

# Determine the correct import path based on project structure
try:
    # Try importing as if running from the project root
    from packet_capture_module.core.multicast_listener import MulticastListener
    from packet_capture_module.core.packet import Packet
    MODULE_PATH = 'packet_capture_module.core.multicast_listener'
except ImportError:
    try:
        # Try importing as if the module is in the current directory
        from packet_capture_module.core.multicast_listener import MulticastListener
        from packet_capture_module.core.packet import Packet
        MODULE_PATH = 'multicast_listener'
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure the multicast_listener module and dependencies are available")
        print("Expected structure:")
        print("  packet_capture_module/")
        print("    multicast_listener.py")
        print("    core/")
        print("      packet.py")
        sys.exit(1)


class TestMulticastListener(unittest.TestCase):
    """Unit tests for MulticastListener class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.interface = "eth0"
        self.listener = MulticastListener(interface=self.interface)
        self.captured_packets = []
        self.callback_called = threading.Event()
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'listener'):
            self.listener.stop_capture()
    
    def test_init(self):
        """Test MulticastListener initialization."""
        listener = MulticastListener()
        self.assertEqual(listener.interface, "eth0")  # Default interface
        self.assertIsNone(listener.capture)
        self.assertIsNone(listener.capture_thread)
        self.assertFalse(listener.running)
        self.assertIsNone(listener.callback)
        
        custom_listener = MulticastListener(interface="wlan0")
        self.assertEqual(custom_listener.interface, "wlan0")
    
    def test_context_manager(self):
        """Test context manager functionality."""
        with patch.object(MulticastListener, 'stop_capture') as mock_stop:
            with MulticastListener() as listener:
                self.assertIsInstance(listener, MulticastListener)
            mock_stop.assert_called_once()
    
    @patch(f'{MODULE_PATH}.pyshark.LiveCapture')
    def test_start_capture_success(self, mock_live_capture):
        """Test successful capture start."""
        mock_capture = MagicMock()
        mock_live_capture.return_value = mock_capture
        
        callback = Mock()
        
        with patch.object(self.listener, '_capture_loop'):
            result = self.listener.start_capture(callback)
        
        self.assertTrue(result)
        self.assertTrue(self.listener.running)
        self.assertEqual(self.listener.callback, callback)
        self.assertIsNotNone(self.listener.capture_thread)
        
        # Verify pyshark.LiveCapture was called with correct parameters
        mock_live_capture.assert_called_once_with(
            interface=self.interface,
            bpf_filter='(ip multicast || ip6 multicast)',
            use_json=True,
            include_raw=True,
            display_filter=''
        )
    
    @patch(f'{MODULE_PATH}.pyshark.LiveCapture')
    def test_start_capture_already_running(self, mock_live_capture):
        """Test starting capture when already running."""
        self.listener.running = True
        callback = Mock()
        
        result = self.listener.start_capture(callback)
        
        self.assertFalse(result)
        mock_live_capture.assert_not_called()
    
    @patch(f'{MODULE_PATH}.pyshark.LiveCapture')
    def test_start_capture_exception(self, mock_live_capture):
        """Test capture start with exception."""
        mock_live_capture.side_effect = Exception("Test exception")
        callback = Mock()
        
        result = self.listener.start_capture(callback)
        
        self.assertFalse(result)
        self.assertFalse(self.listener.running)
    
    def test_stop_capture_not_running(self):
        """Test stopping capture when not running."""
        # Should not raise exception
        self.listener.stop_capture()
        self.assertFalse(self.listener.running)
    
    @patch(f'{MODULE_PATH}.pyshark.LiveCapture')
    def test_stop_capture_running(self, mock_live_capture):
        """Test stopping running capture."""
        mock_capture = MagicMock()
        mock_live_capture.return_value = mock_capture
        
        # Start capture
        callback = Mock()
        with patch.object(self.listener, '_capture_loop'):
            self.listener.start_capture(callback)
        
        # Stop capture
        self.listener.stop_capture()
        
        self.assertFalse(self.listener.running)
        mock_capture.close.assert_called_once()
    
    def test_packet_callback(self):
        """Test packet processing callback."""
        def test_callback(packet):
            self.captured_packets.append(packet)
            self.callback_called.set()
        
        # Create mock packet data
        mock_packet_data = MagicMock()
        mock_packet_data.frame_raw.value = "deadbeef"
        mock_packet_data.sniff_time.timestamp.return_value = 1234567890.123
        
        # Test packet processing
        with patch(f'{MODULE_PATH}.Packet') as mock_packet_class:
            mock_packet = MagicMock()
            mock_packet.metadata = {}
            mock_packet_class.return_value = mock_packet
            
            self.listener.callback = test_callback
            self.listener.interface = "test_interface"
            self.listener.running = True
            
            # Simulate packet processing
            raw_data = bytes.fromhex("deadbeef")
            
            # Create a mock packet that behaves like the real Packet class
            mock_packet.raw_data = raw_data
            mock_packet.metadata = {
                'capture_time': 1234567890.123,
                'interface': 'test_interface',
                'packet_length': len(raw_data)
            }
            
            test_callback(mock_packet)
            
            self.assertTrue(self.callback_called.is_set())
            self.assertEqual(len(self.captured_packets), 1)
            self.assertEqual(self.captured_packets[0], mock_packet)


class TestMulticastListenerIntegration(unittest.TestCase):
    """Integration tests for MulticastListener (requires root privileges)."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.packets_received = []
        self.packet_event = threading.Event()
    
    def packet_handler(self, packet):
        """Handle received packets in integration tests."""
        self.packets_received.append(packet)
        self.packet_event.set()
        print(f"Received packet: {len(packet.raw_data)} bytes, metadata: {packet.metadata}")
    
    @unittest.skipUnless(os.geteuid() == 0, "Integration tests require root privileges")
    def test_real_capture(self):
        """Test real packet capture (requires root)."""
        print("\n=== Integration Test: Real Multicast Capture ===")
        print("This test will capture multicast packets for 10 seconds...")
        print("You may need to generate multicast traffic to see results.")
        
        with MulticastListener(interface="any") as listener:
            success = listener.start_capture(self.packet_handler)
            self.assertTrue(success, "Failed to start packet capture")
            
            # Wait for packets or timeout
            timeout = 10
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.packet_event.wait(timeout=1):
                    break
            
            print(f"Captured {len(self.packets_received)} multicast packets")
            
            if self.packets_received:
                packet = self.packets_received[0]
                self.assertIsNotNone(packet.raw_data)
                self.assertIn('capture_time', packet.metadata)
                self.assertIn('interface', packet.metadata)
                self.assertIn('packet_length', packet.metadata)


class MulticastListenerDemo:
    """Demonstration class for MulticastListener functionality."""
    
    def __init__(self):
        self.packets_count = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def packet_handler(self, packet):
        """Handle packets for demonstration."""
        with self.lock:
            self.packets_count += 1
            
            # Print packet info every 10 packets or for first 5 packets
            if self.packets_count <= 5 or self.packets_count % 10 == 0:
                elapsed = time.time() - self.start_time
                print(f"[{elapsed:.1f}s] Packet #{self.packets_count}: "
                      f"{len(packet.raw_data)} bytes from {packet.metadata.get('interface', 'unknown')}")
                
                # Print first few bytes of packet data
                data_preview = packet.raw_data[:16]
                hex_preview = ' '.join(f'{b:02x}' for b in data_preview)
                print(f"  Data preview: {hex_preview}")
    
    def run_demo(self, interface="any", duration=30):
        """Run demonstration of multicast listening."""
        print(f"\n=== MulticastListener Demo ===")
        print(f"Interface: {interface}")
        print(f"Duration: {duration} seconds")
        print(f"Filter: Multicast packets only")
        print("-" * 50)
        
        try:
            with MulticastListener(interface=interface) as listener:
                success = listener.start_capture(self.packet_handler)
                
                if not success:
                    print("ERROR: Failed to start packet capture!")
                    print("Make sure you have:")
                    print("1. Root/administrator privileges")
                    print("2. Valid network interface")
                    print("3. Required dependencies (pyshark, tshark)")
                    return
                
                print(f"Listening for multicast packets on {interface}...")
                print("Press Ctrl+C to stop early")
                
                try:
                    time.sleep(duration)
                except KeyboardInterrupt:
                    print("\nStopping capture...")
                
                print(f"\nDemo completed!")
                print(f"Total packets captured: {self.packets_count}")
                
                if self.packets_count == 0:
                    print("\nNo multicast packets detected. This could mean:")
                    print("- No multicast traffic on the network")
                    print("- Interface is not receiving multicast packets")
                    print("- Firewall blocking packet capture")
                
        except Exception as e:
            print(f"Demo error: {e}")
            import traceback
            traceback.print_exc()


def run_mock_tests():
    """Run unit tests with mocked dependencies."""
    print("=== Running Unit Tests (Mocked) ===")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMulticastListener)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_integration_tests():
    """Run integration tests (requires root)."""
    print("\n=== Running Integration Tests ===")
    if os.geteuid() != 0:
        print("WARNING: Integration tests require root privileges")
        print("Run with sudo to test real packet capture")
        return True
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMulticastListenerIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def main():
    """Main test runner with options."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MulticastListener Test Suite")
    parser.add_argument("--demo", action="store_true", 
                       help="Run interactive demo")
    parser.add_argument("--interface", default="any",
                       help="Network interface for demo (default: any)")
    parser.add_argument("--duration", type=int, default=30,
                       help="Demo duration in seconds (default: 30)")
    parser.add_argument("--unit-only", action="store_true",
                       help="Run only unit tests (no integration tests)")
    parser.add_argument("--no-tests", action="store_true",
                       help="Skip all tests, only run demo")
    
    args = parser.parse_args()
    
    success = True
    
    if not args.no_tests:
        # Run unit tests
        success &= run_mock_tests()
        
        # Run integration tests unless skipped
        if not args.unit_only:
            success &= run_integration_tests()
    
    # Run demo if requested
    if args.demo:
        demo = MulticastListenerDemo()
        demo.run_demo(interface=args.interface, duration=args.duration)
    
    if not args.no_tests:
        print(f"\n=== Test Results ===")
        print(f"Overall success: {success}")
        
        if not success:
            print("Some tests failed. Check output above for details.")
            sys.exit(1)
        else:
            print("All tests passed!")
    
    return 0


if __name__ == "__main__":
    exit(main())