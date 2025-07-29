"""
Enhanced Integration between DPI Engine, Traffic Classifier, and Packet Capture.
"""
import time
import threading
import queue
from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict, deque
import logging

from packet_capture_module.core.packet import Packet
from dpi_module.main import DPIEngine
from traffic_classifier.traffic_classifier import TrafficClassifier
from traffic_classifier.traffic_metadata import TrafficMetadata

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enhanced_integration")

class FlowTracker:
    """
    Track network flows for better classification accuracy.
    """
    def __init__(self, flow_timeout: int = 300):
        self.flows: Dict[str, Dict[str, Any]] = {}
        self.flow_timeout = flow_timeout
        self.lock = threading.RLock()
    
    def update_flow(self, metadata: TrafficMetadata) -> Dict[str, Any]:
        """
        Update flow information and return flow statistics.
        
        Args:
            metadata: Traffic metadata
            
        Returns:
            Flow statistics
        """
        with self.lock:
            flow_key = metadata.get_flow_key()
            current_time = time.time()
            
            if flow_key not in self.flows:
                self.flows[flow_key] = {
                    "first_seen": current_time,
                    "last_seen": current_time,
                    "packet_count": 0,
                    "byte_count": 0,
                    "classifications": [],
                    "metadata_history": deque(maxlen=100)
                }
            
            flow = self.flows[flow_key]
            flow["last_seen"] = current_time
            flow["packet_count"] += 1
            flow["byte_count"] += metadata.packet_size or 0
            
            if metadata.traffic_class:
                flow["classifications"].append(metadata.traffic_class)
            
            flow["metadata_history"].append(metadata.to_dict())
            
            # Calculate flow duration
            metadata.flow_duration = current_time - flow["first_seen"]
            
            # Clean up old flows
            self._cleanup_old_flows(current_time)
            
            return flow
    
    def _cleanup_old_flows(self, current_time: float) -> None:
        """Clean up flows that have timed out."""
        flows_to_remove = []
        
        for flow_key, flow in self.flows.items():
            if current_time - flow["last_seen"] > self.flow_timeout:
                flows_to_remove.append(flow_key)
        
        for flow_key in flows_to_remove:
            del self.flows[flow_key]
    
    def get_flow_statistics(self) -> Dict[str, Any]:
        """Get overall flow statistics."""
        with self.lock:
            return {
                "active_flows": len(self.flows),
                "total_packets": sum(f["packet_count"] for f in self.flows.values()),
                "total_bytes": sum(f["byte_count"] for f in self.flows.values())
            }

class EnhancedDPITrafficClassifierIntegration:
    """
    Enhanced integration with improved flow tracking and performance monitoring.
    """
    
    def __init__(self, 
                 dpi_engine: Optional[DPIEngine] = None,
                 traffic_classifier: Optional[TrafficClassifier] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize enhanced integration.
        
        Args:
            dpi_engine: DPI Engine instance
            traffic_classifier: Traffic Classifier instance
            config: Configuration dictionary
        """
        self.config = config or {}
        
        # Initialize components
        self.dpi_engine = dpi_engine or DPIEngine()
        self.traffic_classifier = traffic_classifier or TrafficClassifier()
        self.flow_tracker = FlowTracker(
            flow_timeout=self.config.get("flow_timeout", 300)
        )
        
        # Processing queues
        self.packet_queue = queue.Queue(maxsize=self.config.get("packet_queue_size", 1000))
        self.dpi_result_queue = queue.Queue(maxsize=self.config.get("dpi_queue_size", 500))
        
        # Processing threads
        self.packet_processor_thread = None
        self.dpi_processor_thread = None
        self.should_stop = False
        
        # Callbacks
        self.result_callbacks = []
        self.performance_callbacks = []
        
        # Performance monitoring
        self.performance_stats = {
            "packets_received": 0,
            "packets_processed": 0,
            "dpi_analyses_completed": 0,
            "classifications_completed": 0,
            "processing_errors": 0,
            "queue_overflows": 0,
            "average_processing_time": 0.0,
            "start_time": time.time()
        }
        
        # Connect components
        self._setup_component_connections()
        
        logger.info("Enhanced DPI-Traffic Classifier integration initialized")
    
    def _setup_component_connections(self) -> None:
        """Setup connections between components."""
        # Connect DPI Engine callback
        self.dpi_engine.register_result_callback(self._handle_dpi_result)
        
        # Connect Traffic Classifier callback
        self.traffic_classifier.register_result_callback(self._handle_classification_result)
    
    def process_packet(self, packet: Packet) -> None:
        """
        Process a packet through the complete pipeline.
        
        Args:
            packet: Packet to process
        """
        self.performance_stats["packets_received"] += 1
        
        try:
            # Add to processing queue
            self.packet_queue.put(packet, block=False)
        except queue.Full:
            self.performance_stats["queue_overflows"] += 1
            logger.warning("Packet queue full, dropping packet")
    
    def _process_packets(self) -> None:
        """Background thread for processing packets."""
        logger.info("Starting packet processing thread")
        
        while not self.should_stop:
            try:
                # Get packet from queue
                packet = self.packet_queue.get(timeout=1.0)
                
                start_time = time.time()
                
                # Create initial metadata from packet
                metadata = TrafficMetadata.from_packet(packet)
                
                # Update flow tracking
                flow_stats = self.flow_tracker.update_flow(metadata)
                
                # Send packet to DPI engine
                self.dpi_engine.process_packet(packet)
                
                # Update performance stats
                processing_time = time.time() - start_time
                self._update_processing_time(processing_time)
                
                self.performance_stats["packets_processed"] += 1
                self.packet_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing packet: {e}", exc_info=True)
                self.performance_stats["processing_errors"] += 1
    
    def _handle_dpi_result(self, dpi_result: Dict[str, Any]) -> None:
        """
        Handle DPI analysis result.
        
        Args:
            dpi_result: DPI analysis result
        """
        self.performance_stats["dpi_analyses_completed"] += 1
        
        try:
            # Add to DPI result queue
            self.dpi_result_queue.put(dpi_result, block=False)
        except queue.Full:
            logger.warning("DPI result queue full, dropping result")
    
    def _process_dpi_results(self) -> None:
        """Background thread for processing DPI results."""
        logger.info("Starting DPI result processing thread")
        
        while not self.should_stop:
            try:
                # Get DPI result from queue
                dpi_result = self.dpi_result_queue.get(timeout=1.0)
                
                # Create metadata from DPI result
                metadata = TrafficMetadata.from_dpi_result(dpi_result)
                
                # Update flow tracking
                self.flow_tracker.update_flow(metadata)
                
                # Process through traffic classifier
                classified_metadata = self.traffic_classifier.process_metadata(metadata)
                
                # Create final result
                final_result = self._create_final_result(classified_metadata, dpi_result)
                
                # Notify callbacks
                for callback in self.result_callbacks:
                    try:
                        callback(final_result)
                    except Exception as e:
                        logger.error(f"Error in result callback: {e}", exc_info=True)
                
                self.performance_stats["classifications_completed"] += 1
                self.dpi_result_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing DPI result: {e}", exc_info=True)
                self.performance_stats["processing_errors"] += 1
    
    def _handle_classification_result(self, result: Dict[str, Any]) -> None:
        """
        Handle classification result from traffic classifier.
        
        Args:
            result: Classification result
        """
        # This is called by the traffic classifier's internal processing
        # We handle the final result in _process_dpi_results
        pass
    
    def _create_final_result(self, metadata: TrafficMetadata, dpi_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create final integrated result.
        
        Args:
            metadata: Classified traffic metadata
            dpi_result: Original DPI result
            
        Returns:
            Final integrated result
        """
        return {
            "timestamp": time.time(),
            "flow_key": metadata.get_flow_key(),
            "network_info": {
                "src_ip": metadata.src_ip,
                "dst_ip": metadata.dst_ip,
                "src_port": metadata.src_port,
                "dst_port": metadata.dst_port,
                "protocol": metadata.protocol,
                "packet_size": metadata.packet_size
            },
            "classification": {
                "traffic_class": metadata.traffic_class,
                "priority": metadata.priorityTag,
                "application": metadata.application,
                "confidence": dpi_result.get("confidence", 0.0)
            },
            "technical_details": {
                "codec": metadata.codec,
                "media_type": metadata.media_type,
                "encrypted": metadata.encrypted,
                "estimated_bandwidth": metadata.estimatedBandwidth
            },
            "quality_metrics": {
                "latency": metadata.latency,
                "jitter": metadata.jitter,
                "packet_loss": metadata.packet_loss,
                "requirements": metadata.estimate_quality_requirements()
            },
            "flow_info": {
                "duration": metadata.flow_duration,
                "is_real_time": metadata.is_real_time_traffic()
            },
            "dpi_analysis": {
                "protocol_info": dpi_result.get("protocol_info", {}),
                "pattern_matches": dpi_result.get("pattern_matches", []),
                "anomalies": dpi_result.get("anomalies", [])
            },
            "raw_data": {
                "dpi_result": dpi_result,
                "metadata": metadata.to_dict()
            }
        }
    
    def _update_processing_time(self, processing_time: float) -> None:
        """Update average processing time."""
        current_avg = self.performance_stats["average_processing_time"]
        packet_count = self.performance_stats["packets_processed"]
        
        if packet_count == 0:
            self.performance_stats["average_processing_time"] = processing_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.performance_stats["average_processing_time"] = (
                alpha * processing_time + (1 - alpha) * current_avg
            )
    
    def start_processing(self) -> bool:
        """
        Start all processing threads.
        
        Returns:
            True if started successfully
        """
        if (self.packet_processor_thread and self.packet_processor_thread.is_alive() or
            self.dpi_processor_thread and self.dpi_processor_thread.is_alive()):
            logger.warning("Processing already running")
            return False
        
        self.should_stop = False
        
        # Start Traffic Classifier processing
        self.traffic_classifier.start_processing()
        
        # Start packet processing thread
        self.packet_processor_thread = threading.Thread(
            target=self._process_packets,
            daemon=True
        )
        self.packet_processor_thread.start()
        
        # Start DPI result processing thread
        self.dpi_processor_thread = threading.Thread(
            target=self._process_dpi_results,
            daemon=True
        )
        self.dpi_processor_thread.start()
        
        logger.info("Started enhanced integration processing")
        return True
    
    def stop_processing(self) -> bool:
        """
        Stop all processing threads.
        
        Returns:
            True if stopped successfully
        """
        logger.info("Stopping enhanced integration processing")
        
        self.should_stop = True
        
        # Stop Traffic Classifier
        self.traffic_classifier.stop_processing()
        
        # Wait for threads to finish
        threads_to_join = [
            self.packet_processor_thread,
            self.dpi_processor_thread
        ]
        
        for thread in threads_to_join:
            if thread and thread.is_alive():
                thread.join(timeout=5.0)
                if thread.is_alive():
                    logger.warning(f"Thread {thread.name} did not stop gracefully")
        
        logger.info("Stopped enhanced integration processing")
        return True
    
    def register_result_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a callback for final classification results.
        
        Args:
            callback: Callback function
        """
        self.result_callbacks.append(callback)
    
    def register_performance_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a callback for performance metrics.
        
        Args:
            callback: Callback function
        """
        self.performance_callbacks.append(callback)
    
    def update_network_load(self, load_percentage: float) -> None:
        """
        Update network load for dynamic adjustments.
        
        Args:
            load_percentage: Current network load (0-100%)
        """
        self.traffic_classifier.update_network_load(load_percentage)
    
    def get_comprehensive_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics.
        
        Returns:
            Comprehensive statistics
        """
        stats = self.performance_stats.copy()
        
        # Add component statistics
        stats["traffic_classifier"] = self.traffic_classifier.get_statistics()
        stats["dpi_engine"] = self.dpi_engine.get_stats()
        stats["flow_tracker"] = self.flow_tracker.get_flow_statistics()
        
        # Add queue statistics
        stats["queue_status"] = {
            "packet_queue_size": self.packet_queue.qsize(),
            "dpi_result_queue_size": self.dpi_result_queue.qsize()
        }
        
        # Calculate rates
        elapsed_time = time.time() - stats["start_time"]
        if elapsed_time > 0:
            stats["packets_per_second"] = stats["packets_processed"] / elapsed_time
            stats["classifications_per_second"] = stats["classifications_completed"] / elapsed_time
        
        # Calculate efficiency metrics
        if stats["packets_received"] > 0:
            stats["processing_efficiency"] = stats["packets_processed"] / stats["packets_received"]
            stats["error_rate"] = stats["processing_errors"] / stats["packets_received"]
        
        return stats