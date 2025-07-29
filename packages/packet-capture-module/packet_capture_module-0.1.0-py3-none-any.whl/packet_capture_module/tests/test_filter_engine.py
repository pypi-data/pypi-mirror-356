"""
Unit tests for the modern FilterEngine class.
"""
import unittest
from packet_capture_module.core.filter_engine import FilterEngine  # Adjust import path as needed

class TestFilterEngine(unittest.TestCase):
    def setUp(self):
        self.filter_engine = FilterEngine()
    
    def test_update_filters_valid_rules(self):
        valid_rules = [
            "ip multicast",
            "udp portrange 5000-5004",  # Use BPF-compliant syntax
            "tcp port 80",
            "icmp"
        ]
        result = self.filter_engine.update_filters(valid_rules)
        self.assertTrue(result)
        self.assertEqual(self.filter_engine.get_active_filters(), valid_rules)
    
    def test_update_filters_invalid_rule(self):
        invalid_rules = [
            "ip multicast",          # Valid
            "invalid rule syntax",   # Invalid (no BPF keywords)
            "tcp port 80"            # Valid
        ]
        result = self.filter_engine.update_filters(invalid_rules)
        self.assertFalse(result, "Should reject lists with ANY invalid rules")
        # Verify partial update didn't occur
        self.assertEqual(self.filter_engine.get_active_filters(), [])

    def test_get_active_filters_empty_initial(self):
        # Assuming config returns empty or no rules at init
        self.filter_engine.bpf_rules = []
        self.assertEqual(self.filter_engine.get_active_filters(), [])
    
    def test_str_representation(self):
        rules = ["ip multicast", "udp portrange 5000-5004"]
        self.filter_engine.update_filters(rules)
        s = str(self.filter_engine)
        self.assertIn("ip multicast", s)
        self.assertIn("udp portrange 5000-5004", s)

if __name__ == "__main__":
    unittest.main()
