"""
Enhanced Traffic Metadata model for classification module with better integration.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union
import time
from packet_capture_module.core.packet import Packet

@dataclass
class TrafficMetadata:
    """
    Represents metadata about network traffic for classification purposes.
    """
    protocol: str
    codec: Optional[str] = None
    estimatedBandwidth: float = 0.0
    priorityTag: int = 4  # Default to lowest priority
    
    # Additional metadata
    application: Optional[str] = None
    media_type: Optional[str] = None
    stream_id: Optional[str] = None
    encrypted: bool = False
    traffic_class: Optional[str] = None
    
    # Network layer information
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    packet_size: Optional[int] = None
    
    # Quality of Service metrics
    latency: Optional[float] = None
    jitter: Optional[float] = None
    packet_loss: Optional[float] = None
    
    # Temporal information
    timestamp: float = field(default_factory=time.time)
    flow_duration: Optional[float] = None
    
    # Raw metadata from DPI and packet capture
    raw_metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dpi_result(cls, dpi_result: Dict[str, Any]) -> 'TrafficMetadata':
        """
        Create a TrafficMetadata object from DPI Engine results.
        
        Args:
            dpi_result: DPI Engine analysis result
            
        Returns:
            TrafficMetadata object
        """
        protocol_info = dpi_result.get("protocol_info", {})
        metadata = dpi_result.get("metadata", {})
        
        # Extract main protocol
        protocol = protocol_info.get("application_protocol")
        if not protocol:
            protocol = protocol_info.get("protocol", "UNKNOWN")
        
        # Extract codec if available
        codec = metadata.get("codec")
        
        # Create instance
        instance = cls(
            protocol=protocol,
            codec=codec,
            encrypted=dpi_result.get("encrypted", False),
            timestamp=dpi_result.get("timestamp", time.time()),
            raw_metadata=dpi_result.copy()
        )
        
        # Extract network information if available
        packet_info = dpi_result.get("packet_info", {})
        instance.src_ip = packet_info.get("src_ip")
        instance.dst_ip = packet_info.get("dst_ip")
        instance.src_port = packet_info.get("src_port")
        instance.dst_port = packet_info.get("dst_port")
        instance.packet_size = packet_info.get("size")
        
        # Extract application information
        instance.application = (
            metadata.get("application") or 
            dpi_result.get("estimated_application") or
            protocol_info.get("detected_application")
        )
        instance.media_type = metadata.get("media_type")
        instance.stream_id = metadata.get("stream_id")
        
        # Extract QoS metrics if available
        qos_info = dpi_result.get("qos_metrics", {})
        instance.latency = qos_info.get("latency")
        instance.jitter = qos_info.get("jitter")
        instance.packet_loss = qos_info.get("packet_loss")
        
        return instance
    
    @classmethod
    def from_packet(cls, packet: Packet) -> 'TrafficMetadata':
        """
        Create a TrafficMetadata object from a Packet object.
        
        Args:
            packet: Packet object from packet capture
            
        Returns:
            TrafficMetadata object
        """
        protocol = packet.get_protocol()
        
        instance = cls(
            protocol=protocol,
            src_ip=packet.src_ip,
            dst_ip=packet.dst_ip,
            src_port=packet.src_port,
            dst_port=packet.dst_port,
            packet_size=packet.get_size(),
            timestamp=packet.timestamp,
            raw_metadata=packet.metadata.copy()
        )
        
        # Extract additional information from packet metadata
        if packet.metadata:
            instance.application = packet.metadata.get("application")
            instance.media_type = packet.metadata.get("media_type")
            instance.encrypted = packet.metadata.get("encrypted", False)
            instance.stream_id = packet.metadata.get("stream_id")
        
        return instance
    
    def merge_with_dpi_result(self, dpi_result: Dict[str, Any]) -> None:
        """
        Merge DPI analysis results into existing metadata.
        
        Args:
            dpi_result: DPI Engine analysis result
        """
        protocol_info = dpi_result.get("protocol_info", {})
        metadata = dpi_result.get("metadata", {})
        
        # Update protocol if DPI provides more specific information
        if protocol_info.get("application_protocol"):
            self.protocol = protocol_info["application_protocol"]
        
        # Update codec and media information
        self.codec = metadata.get("codec") or self.codec
        self.media_type = metadata.get("media_type") or self.media_type
        self.encrypted = dpi_result.get("encrypted", self.encrypted)
        
        # Update application information
        detected_app = (
            metadata.get("application") or 
            dpi_result.get("estimated_application") or
            protocol_info.get("detected_application")
        )
        if detected_app:
            self.application = detected_app
        
        # Merge QoS metrics
        qos_info = dpi_result.get("qos_metrics", {})
        if qos_info:
            self.latency = qos_info.get("latency") or self.latency
            self.jitter = qos_info.get("jitter") or self.jitter
            self.packet_loss = qos_info.get("packet_loss") or self.packet_loss
        
        # Merge raw metadata
        self.raw_metadata.update(dpi_result)
    
    def update_from_classification(self, traffic_class: str, priority: int) -> None:
        """
        Update metadata with classification results.
        
        Args:
            traffic_class: Assigned traffic class
            priority: Priority level (0=highest, 4=lowest)
        """
        self.traffic_class = traffic_class
        self.priorityTag = priority
        
        # Add classification timestamp
        self.raw_metadata["classification_timestamp"] = time.time()
        self.raw_metadata["classification_method"] = "rule_based"
    
    def get_flow_key(self) -> str:
        """
        Generate a unique flow identifier for this traffic.
        
        Returns:
            String representing the flow key
        """
        # Sort IPs and ports to ensure consistent flow identification
        # regardless of direction
        if self.src_ip and self.dst_ip:
            ip1, ip2 = sorted([self.src_ip, self.dst_ip])
            port1, port2 = sorted([self.src_port or 0, self.dst_port or 0])
            return f"{ip1}:{port1}-{ip2}:{port2}-{self.protocol}"
        
        return f"unknown-{self.protocol}-{self.timestamp}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to dictionary format.
        
        Returns:
            Dictionary representation of metadata
        """
        return {
            "protocol": self.protocol,
            "codec": self.codec,
            "estimated_bandwidth": self.estimatedBandwidth,
            "priority": self.priorityTag,
            "application": self.application,
            "media_type": self.media_type,
            "stream_id": self.stream_id,
            "encrypted": self.encrypted,
            "traffic_class": self.traffic_class,
            "src_ip": self.src_ip,
            "dst_ip": self.dst_ip,
            "src_port": self.src_port,
            "dst_port": self.dst_port,
            "packet_size": self.packet_size,
            "latency": self.latency,
            "jitter": self.jitter,
            "packet_loss": self.packet_loss,
            "timestamp": self.timestamp,
            "flow_duration": self.flow_duration,
            "flow_key": self.get_flow_key(),
            "raw_metadata": self.raw_metadata
        }
    
    def is_real_time_traffic(self) -> bool:
        """
        Determine if this traffic requires real-time handling.
        
        Returns:
            True if traffic is real-time sensitive
        """
        real_time_classes = {
            "Video Call", "Audio Call", "Gaming", "VoIP", 
            "Live Streaming", "Interactive"
        }
        
        real_time_applications = {
            "Zoom", "Teams", "Skype", "WebRTC", "Discord",
            "Twitch", "YouTube Live"
        }
        
        return (
            self.traffic_class in real_time_classes or
            self.application in real_time_applications or
            self.priorityTag <= 1  # High priority traffic
        )
    
    def estimate_quality_requirements(self) -> Dict[str, Any]:
        """
        Estimate quality requirements based on traffic characteristics.
        
        Returns:
            Dictionary with quality requirements
        """
        requirements = {
            "max_latency_ms": 1000,
            "max_jitter_ms": 100,
            "max_packet_loss_percent": 5.0,
            "min_bandwidth_mbps": 0.1
        }
        
        # Adjust based on traffic class
        if self.traffic_class == "Video Call":
            requirements.update({
                "max_latency_ms": 150,
                "max_jitter_ms": 30,
                "max_packet_loss_percent": 1.0,
                "min_bandwidth_mbps": 2.0
            })
        elif self.traffic_class == "Audio Call":
            requirements.update({
                "max_latency_ms": 100,
                "max_jitter_ms": 20,
                "max_packet_loss_percent": 0.5,
                "min_bandwidth_mbps": 0.1
            })
        elif self.traffic_class == "Gaming":
            requirements.update({
                "max_latency_ms": 50,
                "max_jitter_ms": 10,
                "max_packet_loss_percent": 0.1,
                "min_bandwidth_mbps": 1.0
            })
        elif self.traffic_class in ["HD Streaming", "4K Streaming"]:
            requirements.update({
                "max_latency_ms": 5000,
                "max_jitter_ms": 1000,
                "max_packet_loss_percent": 2.0,
                "min_bandwidth_mbps": 5.0 if "HD" in self.traffic_class else 20.0
            })
        
        return requirements