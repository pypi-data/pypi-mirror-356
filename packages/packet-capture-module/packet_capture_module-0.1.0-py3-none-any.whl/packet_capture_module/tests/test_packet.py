import unittest
import dpkt
import socket
import time
import struct
from io import BytesIO
from packet_capture_module.core.packet import Packet

class TestPacket(unittest.TestCase):
    def setUp(self):
        # Helper function to create IP headers
        def create_ip_header(src_ip, dst_ip, proto, payload=b''):
            ip = dpkt.ip.IP(
                src=socket.inet_aton(src_ip),
                dst=socket.inet_aton(dst_ip),
                p=proto,
                data=payload
            )
            ip.len += len(payload)
            return ip

        # TCP packet with HTTP payload
        tcp = dpkt.tcp.TCP(sport=1234, dport=80, data=b'HTTP GET /')
        tcp_ip = create_ip_header('192.168.1.1', '192.168.1.2', dpkt.ip.IP_PROTO_TCP, tcp)
        self.tcp_packet = dpkt.ethernet.Ethernet(
            dst=b'\x00\x11\x22\x33\x44\x55',
            src=b'\x00\x11\x22\x33\x44\x56',
            type=dpkt.ethernet.ETH_TYPE_IP,
            data=tcp_ip
        )

        # UDP multicast packet
        udp = dpkt.udp.UDP(sport=5000, dport=5001, data=b'Multicast Data')
        udp_ip = create_ip_header('192.168.1.100', '224.0.0.1', dpkt.ip.IP_PROTO_UDP, udp)
        self.udp_packet = dpkt.ethernet.Ethernet(
            dst=b'\x01\x00\x5e\x00\x00\x01',  # Multicast MAC
            src=b'\x00\x11\x22\x33\x44\x57',
            type=dpkt.ethernet.ETH_TYPE_IP,
            data=udp_ip
        )

    def test_basic_packet(self):
        """Test basic packet creation and properties"""
        raw_data = bytes(self.tcp_packet)
        pkt = Packet(raw_data)
        
        self.assertEqual(pkt.src_ip, '192.168.1.1')
        self.assertEqual(pkt.dst_ip, '192.168.1.2')
        self.assertEqual(pkt.src_port, 1234)
        self.assertEqual(pkt.dst_port, 80)
        self.assertEqual(pkt.get_protocol(), 'TCP')
        self.assertEqual(pkt.get_size(), len(raw_data))
        self.assertFalse(pkt.is_multicast())

    def test_multicast_packet(self):
        """Test multicast packet detection"""
        raw_data = bytes(self.udp_packet)
        pkt = Packet(raw_data)
        
        self.assertEqual(pkt.src_ip, '192.168.1.100')
        self.assertEqual(pkt.dst_ip, '224.0.0.1')
        self.assertEqual(pkt.src_port, 5000)
        self.assertEqual(pkt.dst_port, 5001)
        self.assertEqual(pkt.get_protocol(), 'UDP')
        self.assertTrue(pkt.is_multicast())

    def test_metadata(self):
        """Test metadata handling"""
        pkt = Packet(b'', metadata={'initial': 'data'})
        pkt.add_metadata('test', 123)
        
        self.assertEqual(pkt.metadata['initial'], 'data')
        self.assertEqual(pkt.metadata['test'], 123)

    def test_payload_extraction(self):
        """Test payload extraction"""
        raw_data = bytes(self.tcp_packet)
        pkt = Packet(raw_data)
        
        self.assertEqual(pkt.get_payload(), b'HTTP GET /')

    def test_invalid_packet(self):
        """Test handling of invalid packets"""
        pkt = Packet(b'invalid packet data')
        
        self.assertEqual(pkt.get_protocol(), 'UNKNOWN')
        self.assertEqual(pkt.get_size(), 19)

    def test_custom_timestamp(self):
        """Test custom timestamp handling"""
        test_time = time.time() - 3600  # 1 hour ago
        pkt = Packet(b'', timestamp=test_time)
        
        self.assertEqual(pkt.timestamp, test_time)

if __name__ == '__main__':
    unittest.main()