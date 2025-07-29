"""
Dynamic traffic adjustment based on network conditions.
"""
from typing import Dict, Any, List, Optional
import time

from traffic_classifier.traffic_metadata import TrafficMetadata

class DynamicAdjuster:
    """
    Dynamically adjusts traffic classifications based on network conditions.
    """
    
    def __init__(self):
        """Initialize dynamic adjuster."""
        self.current_load = 0.0  # Current network load (0-100%)
        self.last_update = time.time()
        self.congestion_threshold = 80.0  # Load percentage that triggers adjustments
        self.severe_congestion_threshold = 90.0
        
        # Traffic classes and their adjusted versions during congestion
        self.adjustments = {
            "4K Streaming": "HD Streaming",
            "HD Streaming": "SD Streaming",
            "Video Call": "Audio Call",
            "Gaming": "Gaming (Low Quality)",
            "Web Browsing": "Web Browsing (Low Quality)",
            "File Download": "Background Download"
        }
        
        # Priority adjustments during congestion
        self.priority_boosts = {
            "Video Call": -1,  # Reduce priority number (higher priority)
            "Audio Call": -1,
            "Web Browsing": 0,  # No change
            "Gaming": -1,
            "SD Streaming": 1   # Increase priority number (lower priority)
        }
    
    def update_network_load(self, load: float) -> None:
        """
        Update current network load.
        
        Args:
            load: Current load percentage (0-100)
        """
        self.current_load = load
        self.last_update = time.time()
    
    def is_congested(self) -> bool:
        """
        Check if network is congested.
        
        Returns:
            True if network is congested, False otherwise
        """
        return self.current_load >= self.congestion_threshold
    
    def is_severely_congested(self) -> bool:
        """
        Check if network is severely congested.
        
        Returns:
            True if network is severely congested, False otherwise
        """
        return self.current_load >= self.severe_congestion_threshold
    
    def downgrade_quality(self, traffic_class: str) -> str:
        """
        Get downgraded traffic class for congestion.
        
        Args:
            traffic_class: Original traffic class
            
        Returns:
            Adjusted traffic class
        """
        return self.adjustments.get(traffic_class, traffic_class)
    
    def adjust_priority(self, traffic_class: str, current_priority: int) -> int:
        """
        Adjust priority based on congestion.
        
        Args:
            traffic_class: Traffic class
            current_priority: Current priority level
            
        Returns:
            Adjusted priority level
        """
        if not self.is_congested():
            return current_priority
            
        adjustment = self.priority_boosts.get(traffic_class, 0)
        
        # Apply more aggressive adjustment for severe congestion
        if self.is_severely_congested() and adjustment <= 0:
            adjustment -= 1
            
        # Ensure priority stays in valid range (0-4)
        new_priority = current_priority + adjustment
        return max(0, min(4, new_priority))
    
    def adjust_traffic(self, metadata: TrafficMetadata) -> TrafficMetadata:
        """
        Adjust traffic classification based on current network conditions.
        
        Args:
            metadata: Traffic metadata to adjust
            
        Returns:
            Adjusted metadata
        """
        if not metadata.traffic_class:
            return metadata
            
        # If network is congested, adjust traffic class
        if self.is_congested():
            # Downgrade traffic class
            original_class = metadata.traffic_class
            new_class = self.downgrade_quality(original_class)
            
            if new_class != original_class:
                metadata.traffic_class = new_class
                
                # Add original class to metadata for reference
                metadata.raw_metadata["original_class"] = original_class
            
            # Adjust priority
            metadata.priorityTag = self.adjust_priority(
                metadata.traffic_class, metadata.priorityTag
            )
            
            # Add congestion flag to metadata
            metadata.raw_metadata["congestion_adjusted"] = True
            metadata.raw_metadata["congestion_level"] = self.current_load
        
        return metadata
