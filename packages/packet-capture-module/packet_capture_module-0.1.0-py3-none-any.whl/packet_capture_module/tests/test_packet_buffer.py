"""
Unit tests for the PacketBuffer class.
"""
import unittest
from unittest.mock import MagicMock, patch
from packet_capture_module.core.packet_buffer import PacketBuffer
from packet_capture_module.core.packet import Packet

class TestPacketBuffer(unittest.TestCase):
    def setUp(self):
        # Mock config for testing
        self.mock_config = {
            "buffer": {
                "size_packets": 100,
                "auto_delete_threshold": 80,
                "priority_queues": {
                    0: "RealTime",
                    1: "Streaming",
                    4: "Other"
                }
            }
        }
        
        # Patch config.get_buffer_config
        self.patcher = patch('packet_capture_module.core.packet_buffer.config')
        mock_config = self.patcher.start()
        mock_config.get_buffer_config.return_value = self.mock_config["buffer"]
        
        # Create buffer instance
        self.buffer = PacketBuffer()
        
        # Create test packets
        self.realtime_packet = MagicMock(spec=Packet)
        self.realtime_packet.dst_port = 5000
        self.realtime_packet.get_protocol.return_value = "UDP"
        self.realtime_packet.metadata = {}
        
        self.streaming_packet = MagicMock(spec=Packet)
        self.streaming_packet.dst_port = 80
        self.streaming_packet.get_protocol.return_value = "TCP"
        self.streaming_packet.metadata = {}
        
        self.other_packet = MagicMock(spec=Packet)
        self.other_packet.dst_port = 1234
        self.other_packet.get_protocol.return_value = "UDP"
        self.other_packet.metadata = {}

    def tearDown(self):
        self.patcher.stop()

    def test_initial_state(self):
        """Test buffer initialization with config values."""
        self.assertEqual(self.buffer.buffer_size, 100)
        self.assertEqual(self.buffer.auto_delete_threshold, 80)
        self.assertEqual(sorted(self.buffer.priority_queues.keys()), [0, 1, 4])
        
        stats = self.buffer.get_stats()
        self.assertEqual(stats["current_size"], 0)
        self.assertEqual(stats["usage_percentage"], 0.0)

    def test_priority_detection(self):
        """Test automatic priority detection logic."""
        # RealTime (port 5000)
        self.buffer.add_packet(self.realtime_packet)
        self.assertEqual(len(self.buffer.priority_queues[0]), 1)
        
        # Streaming (TCP port 80)
        self.buffer.add_packet(self.streaming_packet)
        self.assertEqual(len(self.buffer.priority_queues[1]), 1)
        
        # Other (default)
        self.buffer.add_packet(self.other_packet)
        self.assertEqual(len(self.buffer.priority_queues[4]), 1)

    def test_retrieval_order(self):
        """Test packet retrieval respects priority order."""
        # Add packets in mixed order
        self.buffer.add_packet(self.streaming_packet)  # Pri 1
        self.buffer.add_packet(self.other_packet)      # Pri 4
        self.buffer.add_packet(self.realtime_packet)   # Pri 0
        
        # Retrieval order should be 0 → 1 → 4
        self.assertEqual(self.buffer.get_next_packet(), self.realtime_packet)
        self.assertEqual(self.buffer.get_next_packet(), self.streaming_packet)
        self.assertEqual(self.buffer.get_next_packet(), self.other_packet)
        self.assertIsNone(self.buffer.get_next_packet())

    def test_auto_cleanup(self):
        """Test automatic cleanup when buffer nears capacity."""
        # Fill buffer to 90% (threshold is 80%)
        for _ in range(90):
            self.buffer.add_packet(self.other_packet)
        
        stats = self.buffer.get_stats()
        self.assertGreaterEqual(stats["usage_percentage"], 90)
        
        # Next add should trigger cleanup
        self.buffer.add_packet(self.realtime_packet)
        
        # Verify cleanup occurred
        updated_stats = self.buffer.get_stats()
        self.assertLess(updated_stats["usage_percentage"], 90)
        self.assertGreater(updated_stats["dropped_packets"], 0)
        
        # Highest priority packet should remain
        self.assertEqual(self.buffer.get_next_packet(), self.realtime_packet)

    def test_statistics_tracking(self):
        """Test statistics are accurately tracked."""
        # Add 3 packets
        self.buffer.add_packet(self.realtime_packet)
        self.buffer.add_packet(self.streaming_packet)
        self.buffer.add_packet(self.other_packet)
        
        # Retrieve 2 packets
        self.buffer.get_next_packet()
        self.buffer.get_next_packet()
        
        stats = self.buffer.get_stats()
        self.assertEqual(stats["added_packets"], 3)
        self.assertEqual(stats["retrieved_packets"], 2)
        self.assertEqual(stats["current_size"], 1)

    def test_clear_buffer(self):
        """Test buffer clearance functionality."""
        for _ in range(5):
            self.buffer.add_packet(self.realtime_packet)
        
        self.buffer.clear()
        stats = self.buffer.get_stats()
        self.assertEqual(stats["current_size"], 0)
        self.assertEqual(len(self.buffer.priority_queues[0]), 0)

    def test_invalid_priority_fallback(self):
        """Test invalid priority detection falls back to lowest."""
        invalid_packet = MagicMock(spec=Packet)
        invalid_packet.dst_port = 9999
        invalid_packet.get_protocol.return_value = "UNKNOWN"
        
        self.buffer.add_packet(invalid_packet)
        self.assertEqual(len(self.buffer.priority_queues[4]), 1)

if __name__ == "__main__":
    unittest.main()
