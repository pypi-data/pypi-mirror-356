"""
Modern packet buffer implementation with priority queues, memory management, and enhanced features.
"""
import time
from typing import Dict, List, Optional, Union, Tuple, Deque
from collections import deque, defaultdict
from dataclasses import dataclass
from heapq import heappush, heappop
import threading

from packet_capture_module.core.packet import Packet
from utils.config_handler import get_config
from utils.logging_utils import setup_logger

logger = setup_logger("packet_buffer")

@dataclass
class BufferStats:
    added_packets: int = 0
    retrieved_packets: int = 0
    dropped_packets: int = 0
    peak_usage: int = 0
    last_cleanup: float = time.time()

class PacketBuffer:
    """
    High-performance packet buffer with:
    - Priority-based queuing
    - Memory management
    - Thread safety
    - Advanced statistics
    - Dynamic priority adjustment
    """

    def __init__(self, buffer_size: int = None, config_path: str = "config/config.yaml"):
        # Load centralized configuration
        self.config = get_config(config_path)
        buffer_config = self.config.get_buffer_config()
        
        # Configuration
        self.max_size = buffer_size or buffer_config.size_mb * 1024 * 1024
        self.cleanup_threshold = buffer_config.auto_delete_threshold / 100  # Convert to fraction
        self.checkpoint_interval = buffer_config.checkpoint_interval_sec
        
        # Priority system
        self.priority_queues: Dict[int, Deque[Packet]] = defaultdict(deque)
        self._init_priority_queues(buffer_config.priority_queues)
        
        # Tracking and synchronization
        self.total_packets = 0
        self.packet_sizes: Dict[int, int] = defaultdict(int)  # Priority -> total size
        self.stats = BufferStats()
        self.lock = threading.RLock()
        self.cleanup_lock = threading.Lock()
        
        logger.info(f"Initialized PacketBuffer with max_size={self.max_size} bytes, "
                   f"cleanup_threshold={self.cleanup_threshold}, "
                   f"priority_queues={len(buffer_config.priority_queues)}")

    def _init_priority_queues(self, priority_config: Dict) -> None:
        """Initialize priority queues from configuration"""
        if not priority_config:
            self.priority_queues[0] = deque(maxlen=self.max_size)
            return
            
        for priority_str, criteria in priority_config.items():
            try:
                priority = int(priority_str)
                self.priority_queues[priority] = deque(maxlen=self.max_size)
            except (ValueError, TypeError):
                logger.warning(f"Invalid priority level: {priority_str}")

    def add_packet(self, packet: Packet, priority: Optional[int] = None) -> bool:
        """
        Add packet to buffer with optional priority.
        Returns True if packet was successfully added.
        """
        with self.lock:
            # Determine priority
            priority = self._determine_priority(packet) if priority is None else priority
            priority = self._validate_priority(priority)
            
            # Check capacity management
            if self._needs_cleanup():
                self._cleanup_old_packets()
            
            # Add packet
            try:
                self.priority_queues[priority].append(packet)
                self.total_packets += 1
                self.packet_sizes[priority] += 1
                
                # Update stats
                self.stats.added_packets += 1
                self.stats.peak_usage = max(self.stats.peak_usage, self.total_packets)
                return True
            except Exception as e:
                logger.error(f"Failed to add packet: {e}", exc_info=True)
                self.stats.dropped_packets += 1
                return False

    def get_next_packet(self) -> Optional[Packet]:
        """Get next packet from highest priority non-empty queue."""
        with self.lock:
            for priority in sorted(self.priority_queues.keys()):
                queue = self.priority_queues[priority]
                if queue:
                    packet = queue.popleft()
                    self.total_packets -= 1
                    self.packet_sizes[priority] -= 1
                    self.stats.retrieved_packets += 1
                    return packet
            return None

    def get_packets(self, count: int = 1, priority: Optional[int] = None) -> List[Packet]:
        """
        Get multiple packets, optionally filtered by priority.
        """
        with self.lock:
            packets = []
            if priority is not None:
                queue = self.priority_queues.get(priority, deque())
                packets.extend(self._get_from_queue(queue, count))
            else:
                remaining = count
                for priority in sorted(self.priority_queues.keys()):
                    queue = self.priority_queues[priority]
                    packets.extend(self._get_from_queue(queue, remaining))
                    remaining = count - len(packets)
                    if remaining <= 0:
                        break
            return packets

    def _get_from_queue(self, queue: Deque[Packet], count: int) -> List[Packet]:
        """Helper to get packets from a single queue"""
        packets = []
        for _ in range(min(count, len(queue))):
            try:
                packet = queue.popleft()
                self.total_packets -= 1
                self.stats.retrieved_packets += 1
                packets.append(packet)
            except IndexError:
                break
        return packets

    def _determine_priority(self, packet: Packet) -> int:
        """Determine packet priority based on metadata and content"""
        # Check explicit priority in metadata
        if 'priority' in packet.metadata:
            return self._validate_priority(packet.metadata['priority'])
            
        # Check traffic class
        traffic_class = packet.metadata.get('traffic_class')
        if traffic_class:
            buffer_config = self.config.get_buffer_config()
            for priority, criteria in buffer_config.priority_queues.items():
                if str(criteria).lower() == traffic_class.lower():
                    return self._validate_priority(int(priority))
        
        # Protocol/port based detection
        protocol = packet.get_protocol().upper()
        dst_port = packet.dst_port
        
        buffer_config = self.config.get_buffer_config()
        for priority, criteria in buffer_config.priority_queues.items():
            criteria_str = str(criteria).upper()
            
            # Protocol match
            if protocol in criteria_str:
                return self._validate_priority(int(priority))
                
            # Port range match
            if "PORT" in criteria_str:
                port_part = criteria_str.split("PORT")[-1].strip()
                if self._match_port_range(dst_port, port_part):
                    return self._validate_priority(int(priority))
        
        return self._validate_priority(0)  # Default to lowest

    def _match_port_range(self, port: int, spec: str) -> bool:
        """Check if port matches a range specification"""
        try:
            if '-' in spec:
                start, end = map(int, spec.split('-'))
                return start <= port <= end
            return port == int(spec)
        except (ValueError, AttributeError):
            return False

    def _validate_priority(self, priority: int) -> int:
        """Ensure priority exists, fallback to nearest available"""
        if priority in self.priority_queues:
            return priority
        available = sorted(self.priority_queues.keys())
        if not available:
            raise RuntimeError("No priority queues configured")
        return min(available, key=lambda x: abs(x - priority))

    def _needs_cleanup(self) -> bool:
        """Check if buffer needs cleanup"""
        return (self.total_packets / self.max_size) >= self.cleanup_threshold

    def _cleanup_old_packets(self) -> int:
        """
        Cleanup old packets based on age and priority.
        Returns number of packets removed.
        """
        with self.cleanup_lock:
            target = int(self.max_size * 0.2)  # Target 20% reduction
            removed = 0
            current_time = time.time()
            
            # Clean from lowest priority first
            for priority in sorted(self.priority_queues.keys(), reverse=True):
                queue = self.priority_queues[priority]
                new_queue = deque()
                
                for packet in queue:
                    packet_age = current_time - packet.timestamp
                    if packet_age > self.checkpoint_interval and removed < target:
                        removed += 1
                        self.stats.dropped_packets += 1
                    else:
                        new_queue.append(packet)
                
                self.priority_queues[priority] = new_queue
                
                if removed >= target:
                    break
            
            self.total_packets -= removed
            self.stats.last_cleanup = current_time
            logger.info(f"Cleaned {removed} old packets")
            return removed

    def get_stats(self) -> Dict[str, Union[int, float]]:
        """Get comprehensive buffer statistics"""
        with self.lock:
            return {
                "total_packets": self.total_packets,
                "usage_percentage": (self.total_packets / self.max_size) * 100,
                "by_priority": dict(self.packet_sizes),
                **self.stats.__dict__,
                "queues": len(self.priority_queues)
            }

    def clear(self) -> None:
        """Clear all packets from buffer"""
        with self.lock:
            for queue in self.priority_queues.values():
                queue.clear()
            self.total_packets = 0
            self.packet_sizes.clear()
            logger.info("Buffer completely cleared")

    def reload_config(self) -> None:
        """Reload configuration and update buffer settings"""
        self.config.reload_config()
        buffer_config = self.config.get_buffer_config()
        
        with self.lock:
            # Update configuration
            self.cleanup_threshold = buffer_config.auto_delete_threshold / 100
            self.checkpoint_interval = buffer_config.checkpoint_interval_sec
            
            # Reinitialize priority queues
            self.priority_queues.clear()
            self._init_priority_queues(buffer_config.priority_queues)
            
        logger.info("Buffer configuration reloaded")

    def __len__(self) -> int:
        """Current number of packets in buffer"""
        return self.total_packets

    def __contains__(self, packet: Packet) -> bool:
        """Check if packet is in buffer"""
        with self.lock:
            for queue in self.priority_queues.values():
                if packet in queue:
                    return True
        return False