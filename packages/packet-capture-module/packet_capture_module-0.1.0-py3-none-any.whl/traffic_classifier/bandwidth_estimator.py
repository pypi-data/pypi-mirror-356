"""
Bandwidth estimation for traffic classification.
"""
from typing import Dict, List, Any, Optional
import time
import json
import os
from collections import defaultdict

from traffic_classifier.traffic_metadata import TrafficMetadata

class BandwidthEstimator:
    """
    Estimates bandwidth usage based on traffic metadata and historical data.
    """
    
    def __init__(self, historical_data_path: Optional[str] = None):
        """
        Initialize bandwidth estimator.
        
        Args:
            historical_data_path: Path to historical data file
        """
        # Historical data by traffic class
        self.historical_data: Dict[str, List[float]] = defaultdict(list)
        self.total_estimates: Dict[str, int] = defaultdict(int)
        self.total_bandwidth: Dict[str, float] = defaultdict(float)
        
        # Bandwidth by codec type (Mbps)
        self.codec_bandwidth = {
            "H.264": 5.0,     # Standard HD video
            "H.265": 3.0,     # More efficient HD video
            "VP8": 4.0,       # WebRTC video
            "VP9": 2.5,       # More efficient WebRTC video
            "AV1": 2.0,       # Next-gen video codec
            "MPEG-4": 4.0,    # Standard video
            "OPUS": 0.064,    # High quality audio
            "AAC": 0.128,     # Standard audio
            "PCMU": 0.064,    # VoIP audio
            "PCMA": 0.064,    # VoIP audio
            "G.722": 0.064,   # HD VoIP audio
            "AMR": 0.012      # Mobile audio
        }
        
        # Traffic class bandwidth (Mbps)
        self.class_bandwidth = {
            "Video Call": 2.5,
            "Audio Call": 0.1,
            "HD Streaming": 5.0,
            "4K Streaming": 20.0,
            "Web Browsing": 1.0,
            "File Download": 10.0,
            "Social Media": 1.5,
            "Email": 0.5,
            "Gaming": 3.0,
            "IoT": 0.1
        }
        
        # Load historical data if provided
        if historical_data_path and os.path.exists(historical_data_path):
            self._load_historical_data(historical_data_path)
    
    def _load_historical_data(self, file_path: str) -> None:
        """
        Load historical bandwidth data from file.
        
        Args:
            file_path: Path to historical data JSON file
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                for traffic_class, values in data.items():
                    if isinstance(values, list):
                        self.historical_data[traffic_class] = values
                    elif isinstance(values, dict) and "avg_bandwidth" in values:
                        # Alternative format with average bandwidth
                        self.historical_data[traffic_class] = [values["avg_bandwidth"]] * 10
        except Exception as e:
            print(f"Error loading historical data: {e}")
    
    def save_historical_data(self, file_path: str) -> None:
        """
        Save current historical data to file.
        
        Args:
            file_path: Path to save historical data
        """
        try:
            # Calculate averages for each traffic class
            averages = {}
            for traffic_class, values in self.historical_data.items():
                if values:
                    averages[traffic_class] = {
                        "avg_bandwidth": sum(values) / len(values),
                        "samples": len(values),
                        "last_updated": time.time()
                    }
            
            # Save to file
            with open(file_path, 'w') as f:
                json.dump(averages, f, indent=2)
        except Exception as e:
            print(f"Error saving historical data: {e}")
    
    def predict_usage(self, traffic_class: str) -> float:
        """
        Predict bandwidth usage for a traffic class.
        
        Args:
            traffic_class: Traffic class to predict
            
        Returns:
            Predicted bandwidth in Mbps
        """
        # Check historical data first
        if traffic_class in self.historical_data and self.historical_data[traffic_class]:
            # Return average of historical data
            return sum(self.historical_data[traffic_class]) / len(self.historical_data[traffic_class])
        
        # Fallback to default class bandwidth
        if traffic_class in self.class_bandwidth:
            return self.class_bandwidth[traffic_class]
        
        # Default fallback
        return 1.0  # 1 Mbps default
    
    def estimate_bandwidth(self, metadata: TrafficMetadata) -> float:
        """
        Estimate bandwidth for traffic based on its metadata.
        
        Args:
            metadata: Traffic metadata
            
        Returns:
            Estimated bandwidth in Mbps
        """
        estimated_bandwidth = 0.0
        
        # If we already have a traffic class, use historical data
        if metadata.traffic_class:
            estimated_bandwidth = self.predict_usage(metadata.traffic_class)
        
        # If we have a codec, use codec-based estimation
        elif metadata.codec and metadata.codec in self.codec_bandwidth:
            estimated_bandwidth = self.codec_bandwidth[metadata.codec]
            
            # Adjust for media type
            if metadata.media_type == "video":
                # Higher resolution needs more bandwidth
                if "4K" in (metadata.raw_metadata.get("resolution") or ""):
                    estimated_bandwidth *= 4
                elif "HD" in (metadata.raw_metadata.get("resolution") or ""):
                    estimated_bandwidth *= 1.5
            
        # Fallback to protocol-based estimation
        elif metadata.protocol:
            if "RTP" in metadata.protocol:
                estimated_bandwidth = 2.0  # Assume video call
            elif "HTTP" in metadata.protocol:
                estimated_bandwidth = 1.0  # Assume web browsing
            elif "RTSP" in metadata.protocol:
                estimated_bandwidth = 5.0  # Assume video streaming
        
        # Update metadata with estimate
        metadata.estimatedBandwidth = estimated_bandwidth
        
        # Store this estimate for future predictions
        if metadata.traffic_class:
            self.historical_data[metadata.traffic_class].append(estimated_bandwidth)
            # Keep last 100 estimates per class
            self.historical_data[metadata.traffic_class] = self.historical_data[metadata.traffic_class][-100:]
            
            # Update totals
            self.total_estimates[metadata.traffic_class] += 1
            self.total_bandwidth[metadata.traffic_class] += estimated_bandwidth
        
        return estimated_bandwidth
    
    def get_avg_bandwidth_by_class(self) -> Dict[str, float]:
        """
        Get average bandwidth by traffic class.
        
        Returns:
            Dictionary mapping traffic classes to average bandwidth
        """
        result = {}
        
        for traffic_class, values in self.historical_data.items():
            if values:
                result[traffic_class] = sum(values) / len(values)
        
        return result
