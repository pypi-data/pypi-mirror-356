"""
Traffic Classification Module main implementation.
"""
import os
import time
import json
import threading
import queue
from typing import Dict, List, Any, Optional, Callable
import logging

from traffic_classifier.traffic_metadata import TrafficMetadata
from traffic_classifier.classification_rule import ClassificationRule
from traffic_classifier.bandwidth_estimator import BandwidthEstimator
from traffic_classifier.dynamic_adjuster import DynamicAdjuster

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("traffic_classifier")

class TrafficClassifier:
    """
    Main Traffic Classification Module.
    
    Classifies traffic based on metadata from DPI Engine.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize Traffic Classifier.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.bandwidth_estimator = BandwidthEstimator(
            self.config.get("historical_data_path")
        )
        
        self.dynamic_adjuster = DynamicAdjuster()
        
        # Load classification rules
        self.rules: List[ClassificationRule] = []
        self._load_rules(self.config.get("rules_path"))
        
        # Statistics and state
        self.stats = {
            "traffic_processed": 0,
            "classified_traffic": 0,
            "unclassified_traffic": 0,
            "last_update": time.time(),
            "traffic_by_class": {},
            "traffic_by_priority": {}
        }
        
        # Processing queue and thread
        self.processing_queue = queue.Queue()
        self.processing_thread = None
        self.should_stop = False
        
        # Result callbacks
        self.result_callbacks = []
        
        logger.info("Traffic Classifier initialized with %d rules", len(self.rules))
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        # Default configuration
        default_config = {
            "rules_path": "config/classification_rules.json",
            "historical_data_path": "data/bandwidth_history.json",
            "processing_interval": 0.1,
            "batch_size": 10
        }
        
        # Try to load from file
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Update default config with loaded values
                    default_config.update(loaded_config)
            except Exception as e:
                logger.error("Error loading config: %s", e)
        
        return default_config
    
    def _load_rules(self, rules_path: Optional[str]) -> None:
        """
        Load classification rules from file.
        
        Args:
            rules_path: Path to rules file
        """
        # Default rules if no file is provided
        default_rules = [
            {
                "name": "Video Call Rule",
                "condition": "protocol == 'RTP'",
                "action": "Video Call",
                "priority": 0,  # Highest priority
                "bandwidth_estimate": 2.5
            },
            {
                "name": "HTTPS Streaming Rule",
                "condition": "application contains 'Netflix'",
                "action": "HD Streaming",
                "priority": 2,
                "bandwidth_estimate": 5.0
            },
            {
                "name": "HTTP Web Rule",
                "condition": "protocol == 'HTTP'",
                "action": "Web Browsing",
                "priority": 3,
                "bandwidth_estimate": 1.0
            },
            {
                "name": "Audio Call Rule",
                "condition": "codec contains 'OPUS'",
                "action": "Audio Call",
                "priority": 1,
                "bandwidth_estimate": 0.1
            }
        ]
        
        # Try to load from file
        loaded_rules = []
        if rules_path and os.path.exists(rules_path):
            try:
                with open(rules_path, 'r') as f:
                    loaded_rules = json.load(f)
            except Exception as e:
                logger.error("Error loading rules: %s", e)
        
        # Use loaded or default rules
        rules_to_use = loaded_rules if loaded_rules else default_rules
        
        # Convert to ClassificationRule objects
        self.rules = [ClassificationRule.from_dict(rule) for rule in rules_to_use]
        
        logger.info("Loaded %d classification rules", len(self.rules))
    
    def classify_traffic(self, metadata: TrafficMetadata) -> TrafficMetadata:
        """
        Classify traffic based on its metadata.
        
        Args:
            metadata: Traffic metadata to classify
            
        Returns:
            Classified metadata
        """
        # Apply rules to classify traffic
        matched_rule = None
        
        for rule in self.rules:
            if rule.evaluate(metadata):
                matched_rule = rule
                rule.apply(metadata)
                break
        
        # If no rule matched, use default classification
        if not matched_rule:
            # Use protocol-based default classification
            protocol = metadata.protocol.upper()
            
            if "RTP" in protocol:
                metadata.update_from_classification("Video Call", 1)
            elif "HTTP" in protocol:
                metadata.update_from_classification("Web Browsing", 3)
            elif "RTSP" in protocol:
                metadata.update_from_classification("HD Streaming", 2)
            else:
                metadata.update_from_classification("General Traffic", 3)
            
            self.stats["unclassified_traffic"] += 1
        else:
            self.stats["classified_traffic"] += 1
        
        # Track statistics
        traffic_class = metadata.traffic_class
        priority = metadata.priorityTag
        
        if traffic_class:
            if traffic_class in self.stats["traffic_by_class"]:
                self.stats["traffic_by_class"][traffic_class] += 1
            else:
                self.stats["traffic_by_class"][traffic_class] = 1
        
        if priority is not None:
            if priority in self.stats["traffic_by_priority"]:
                self.stats["traffic_by_priority"][priority] += 1
            else:
                self.stats["traffic_by_priority"][priority] = 1
        
        return metadata
    
    def process_metadata(self, metadata: TrafficMetadata) -> TrafficMetadata:
        """
        Process traffic metadata through the complete classification pipeline.
        
        Args:
            metadata: Traffic metadata to process
            
        Returns:
            Processed metadata
        """
        # Step 1: Apply classification rules
        self.classify_traffic(metadata)
        
        # Step 2: Estimate bandwidth
        self.bandwidth_estimator.estimate_bandwidth(metadata)
        
        # Step 3: Apply dynamic adjustments
        self.dynamic_adjuster.adjust_traffic(metadata)
        
        # Update statistics
        self.stats["traffic_processed"] += 1
        self.stats["last_update"] = time.time()
        
        return metadata
    
    def process_dpi_result(self, dpi_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process DPI Engine result and return classified traffic.
        
        Args:
            dpi_result: DPI Engine analysis result
            
        Returns:
            Dictionary with classification results
        """
        # Convert DPI result to traffic metadata
        metadata = TrafficMetadata.from_dpi_result(dpi_result)
        
        # Process the metadata
        classified_metadata = self.process_metadata(metadata)
        
        # Prepare result
        result = {
            "original_dpi_result": dpi_result,
            "traffic_class": classified_metadata.traffic_class,
            "priority": classified_metadata.priorityTag,
            "estimated_bandwidth": classified_metadata.estimatedBandwidth,
            "timestamp": time.time(),
            "congestion_adjusted": classified_metadata.raw_metadata.get(
                "congestion_adjusted", False
            )
        }
        
        return result
    
    def start_processing(self) -> bool:
        """
        Start background processing thread.
        
        Returns:
            True if processing started successfully
        """
        if self.processing_thread and self.processing_thread.is_alive():
            logger.warning("Processing already running")
            return False
        
        self.should_stop = False
        self.processing_thread = threading.Thread(
            target=self._processing_loop,
            daemon=True
        )
        self.processing_thread.start()
        logger.info("Started background processing thread")
        return True
    
    def stop_processing(self) -> bool:
        """
        Stop background processing.
        
        Returns:
            True if processing stopped successfully
        """
        if not self.processing_thread or not self.processing_thread.is_alive():
            logger.warning("Processing not running")
            return False
        
        self.should_stop = True
        self.processing_thread.join(timeout=5.0)
        
        if self.processing_thread.is_alive():
            logger.warning("Failed to stop processing thread gracefully")
            return False
        
        logger.info("Stopped background processing thread")
        return True
    
    def _processing_loop(self) -> None:
        """Background processing loop for DPI results."""
        batch_size = self.config.get("batch_size", 10)
        processing_interval = self.config.get("processing_interval", 0.1)
        
        while not self.should_stop:
            # Process batch of items from queue
            processed = 0
            for _ in range(batch_size):
                try:
                    # Get item with timeout
                    item = self.processing_queue.get(block=True, timeout=0.1)
                    
                    # Process item
                    result = self.process_dpi_result(item)
                    
                    # Notify callbacks
                    for callback in self.result_callbacks:
                        try:
                            callback(result)
                        except Exception as e:
                            logger.error("Error in result callback: %s", e)
                    
                    # Mark item as done
                    self.processing_queue.task_done()
                    processed += 1
                    
                except queue.Empty:
                    # Queue is empty, break batch processing
                    break
                except Exception as e:
                    logger.error("Error processing item: %s", e)
            
            # If no items processed, sleep to avoid busy wait
            if processed == 0:
                time.sleep(processing_interval)
    
    def queue_dpi_result(self, dpi_result: Dict[str, Any]) -> None:
        """
        Queue a DPI result for processing.
        
        Args:
            dpi_result: DPI Engine analysis result
        """
        try:
            self.processing_queue.put(dpi_result, block=False)
        except queue.Full:
            logger.warning("Processing queue full, dropping DPI result")
    
    def register_result_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a callback function for classification results.
        
        Args:
            callback: Function to call with each result
        """
        self.result_callbacks.append(callback)
    
    def update_network_load(self, load_percentage: float) -> None:
        """
        Update network load for dynamic adjustments.
        
        Args:
            load_percentage: Current network load (0-100%)
        """
        self.dynamic_adjuster.update_network_load(load_percentage)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get module statistics.
        
        Returns:
            Statistics dictionary
        """
        stats = self.stats.copy()
        
        # Add bandwidth stats
        stats["bandwidth_by_class"] = self.bandwidth_estimator.get_avg_bandwidth_by_class()
        
        # Add congestion stats
        stats["network_congested"] = self.dynamic_adjuster.is_congested()
        stats["congestion_level"] = self.dynamic_adjuster.current_load
        
        # Queue stats
        stats["queue_size"] = self.processing_queue.qsize()
        
        return stats
