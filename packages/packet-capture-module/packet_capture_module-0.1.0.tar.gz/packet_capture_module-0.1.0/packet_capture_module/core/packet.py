"""
Packet class for representing and analyzing network packets in the DPI system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import time
import dpkt
import socket
import struct
from ipaddress import ip_address, IPv4Address


@dataclass
class Packet:
    """
    Represents a network packet captured from a network stream with comprehensive
    protocol analysis capabilities.

    Attributes:
        raw_data (bytes): The raw packet data
        timestamp (float): Capture timestamp (default: current time)
        src_ip (str): Source IP address (extracted from packet if not provided)
        dst_ip (str): Destination IP address (extracted from packet if not provided)
        src_port (int): Source port number (extracted from packet if not provided)
        dst_port (int): Destination port number (extracted from packet if not provided)
        metadata (Dict[str, Any]): Additional packet metadata (default: empty dict)
    """

    raw_data: bytes
    timestamp: float = field(default_factory=time.time)
    src_ip: str = ""
    dst_ip: str = ""
    src_port: int = 0
    dst_port: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Extract network layer information from raw data if not provided."""
        try:
            eth = dpkt.ethernet.Ethernet(self.raw_data)
            
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if not self.src_ip:
                    self.src_ip = socket.inet_ntoa(ip.src)
                if not self.dst_ip:
                    self.dst_ip = socket.inet_ntoa(ip.dst)
                
                # Transport layer parsing - explicitly check against default 0
                if isinstance(ip.data, (dpkt.tcp.TCP, dpkt.udp.UDP)):
                    transport = ip.data
                    if self.src_port == 0:
                        self.src_port = transport.sport
                    if self.dst_port == 0:
                        self.dst_port = transport.dport

        except Exception:
            # Silently handle parsing errors
            pass

    def get_protocol(self) -> str:
        """
        Determine the protocol of the packet.
        Returns 'UNKNOWN' for any malformed or unsupported packets.
        """
        try:
            # First verify we have enough data for an Ethernet header
            if len(self.raw_data) < 14:  # Minimum Ethernet frame size
                return "UNKNOWN"
                
            eth = dpkt.ethernet.Ethernet(self.raw_data)
            
            # Check for supported Ethernet types
            if eth.type not in (dpkt.ethernet.ETH_TYPE_IP, dpkt.ethernet.ETH_TYPE_ARP):
                return "UNKNOWN"
                
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                protocol_map = {
                    dpkt.ip.IP_PROTO_TCP: "TCP",
                    dpkt.ip.IP_PROTO_UDP: "UDP",
                    dpkt.ip.IP_PROTO_IGMP: "IGMP",
                    dpkt.ip.IP_PROTO_ICMP: "ICMP"
                }
                return protocol_map.get(ip.p, f"IP-{ip.p}")
            
            if isinstance(eth.data, dpkt.arp.ARP):
                return "ARP"
            
            return "UNKNOWN"
        
        except (dpkt.dpkt.UnpackError, dpkt.dpkt.NeedData, struct.error):
            return "UNKNOWN"
        except Exception:
            # Catch any other unexpected errors
            return "UNKNOWN"

    def get_size(self) -> int:
        """
        Get the size of the packet in bytes.
        
        Returns:
            int: Size in bytes
        """
        return len(self.raw_data)

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add metadata to the packet.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value

    def is_multicast(self) -> bool:
        """
        Check if this is a multicast packet.
        
        Returns:
            bool: True if packet has a multicast destination address
        """
        try:
            eth = dpkt.ethernet.Ethernet(self.raw_data)
            
            # Check for IP multicast
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                dest_ip = socket.inet_ntoa(ip.dst)
                try:
                    ip_obj = ip_address(dest_ip)
                    return ip_obj.is_multicast
                except ValueError:
                    return False
                
            # Check for Ethernet multicast (MAC address with LSB of first byte set)
            return bool(eth.dst[0] & 0x01)
            
        except Exception:
            return False

    def get_payload(self) -> Optional[bytes]:
        """
        Extract the transport layer payload if available.
        
        Returns:
            Optional[bytes]: Payload data or None if not available
        """
        try:
            eth = dpkt.ethernet.Ethernet(self.raw_data)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if isinstance(ip.data, (dpkt.tcp.TCP, dpkt.udp.UDP)):
                    return ip.data.data
            return None
        except Exception:
            return None
    
    def has_dpi_analysis(self) -> bool:
        """
        Check if this packet has been analyzed by DPI.
        
        Returns:
            bool: True if DPI analysis has been performed
        """
        return self.metadata.get("dpi_analyzed", False)
    
    def get_dpi_application_protocol(self) -> Optional[str]:
        """
        Get the application protocol identified by DPI.
        
        Returns:
            Optional[str]: Application protocol name or None if not analyzed/identified
        """
        return self.metadata.get("dpi_application_protocol")
    
    def get_dpi_confidence(self) -> float:
        """
        Get the confidence level of DPI analysis.
        
        Returns:
            float: Confidence level (0.0 to 1.0) or 0.0 if not analyzed
        """
        return self.metadata.get("dpi_confidence", 0.0)
    
    def is_encrypted_traffic(self) -> bool:
        """
        Check if this packet contains encrypted traffic according to DPI.
        
        Returns:
            bool: True if encrypted traffic detected
        """
        return self.metadata.get("dpi_encrypted", False)
    
    def get_encrypted_application(self) -> Optional[str]:
        """
        Get the estimated encrypted application.
        
        Returns:
            Optional[str]: Estimated application name or None if not encrypted/analyzed
        """
        return self.metadata.get("dpi_encrypted_app")
    
    def get_dpi_signatures(self) -> list:
        """
        Get the signature matches found by DPI.
        
        Returns:
            list: List of signature matches or empty list if none found
        """
        return self.metadata.get("dpi_signatures", [])
    
    def get_dpi_processing_time(self) -> float:
        """
        Get the DPI processing time in milliseconds.
        
        Returns:
            float: Processing time in ms or 0.0 if not analyzed
        """
        return self.metadata.get("dpi_processing_time_ms", 0.0)
    
    def get_dpi_error(self) -> Optional[str]:
        """
        Get any DPI analysis error.
        
        Returns:
            Optional[str]: Error message or None if no error
        """
        return self.metadata.get("dpi_error")
    
    def get_dpi_summary(self) -> dict:
        """
        Get a summary of DPI analysis results.
        
        Returns:
            dict: Summary of DPI analysis including protocol, confidence, encrypted status, etc.
        """
        if not self.has_dpi_analysis():
            return {"analyzed": False}
        
        return {
            "analyzed": True,
            "application_protocol": self.get_dpi_application_protocol(),
            "confidence": self.get_dpi_confidence(),
            "encrypted": self.is_encrypted_traffic(),
            "encrypted_app": self.get_encrypted_application(),
            "signature_count": len(self.get_dpi_signatures()),
            "processing_time_ms": self.get_dpi_processing_time(),
            "error": self.get_dpi_error()
        }