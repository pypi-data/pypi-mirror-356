"""
Classification rules for traffic classifier.
"""
from typing import Dict, Any, List, Callable, Optional
import re

from traffic_classifier.traffic_metadata import TrafficMetadata

class ClassificationRule:
    """
    Rule for classifying traffic based on metadata.
    """
    def __init__(self, 
                 name: str,
                 condition: str,
                 action: str,
                 priority: int = 3,
                 bandwidth_estimate: Optional[float] = None):
        """
        Initialize a classification rule.
        
        Args:
            name: Rule name
            condition: Condition expression 
            action: Action to take (typically traffic class assignment)
            priority: Priority level (0=highest, 4=lowest)
            bandwidth_estimate: Estimated bandwidth in Mbps (if known)
        """
        self.name = name
        self.condition = condition
        self.action = action
        self.priority = priority
        self.bandwidth_estimate = bandwidth_estimate
    
    def evaluate(self, metadata: TrafficMetadata) -> bool:
        """
        Evaluate if the rule applies to the given metadata.
        
        Args:
            metadata: Traffic metadata to evaluate
            
        Returns:
            True if rule condition matches, False otherwise
        """
        # Simple condition evaluation
        if "==" in self.condition:
            field, value = self.condition.split("==", 1)
            field = field.strip()
            value = value.strip().strip('"\'')
            
            # Check metadata fields
            if field == "protocol":
                return metadata.protocol == value
            elif field == "codec":
                return metadata.codec == value
            elif field == "application":
                return metadata.application == value
            elif field == "media_type":
                return metadata.media_type == value
            elif field == "encrypted":
                return metadata.encrypted == (value.lower() == "true")
            
            # Check raw metadata
            return metadata.raw_metadata.get(field) == value
            
        elif "contains" in self.condition:
            field, value = self.condition.split("contains", 1)
            field = field.strip()
            value = value.strip().strip('"\'')
            
            if field == "protocol":
                return value in (metadata.protocol or "")
            elif field == "codec":
                return value in (metadata.codec or "")
            elif field == "application":
                return value in (metadata.application or "")
            
            # Check raw metadata for string contains
            field_value = metadata.raw_metadata.get(field)
            if isinstance(field_value, str):
                return value in field_value
            
            return False
        
        # Advanced condition evaluation logic could be added here
        return False
    
    def apply(self, metadata: TrafficMetadata) -> None:
        """
        Apply this rule's action to metadata.
        
        Args:
            metadata: Traffic metadata to update
        """
        # Set traffic class from action
        traffic_class = self.action.strip()
        metadata.update_from_classification(traffic_class, self.priority)
        
        # Apply bandwidth estimate if available
        if self.bandwidth_estimate is not None:
            metadata.estimatedBandwidth = self.bandwidth_estimate
    
    @staticmethod
    def from_dict(rule_dict: Dict[str, Any]) -> 'ClassificationRule':
        """
        Create rule from dictionary configuration.
        
        Args:
            rule_dict: Rule configuration dictionary
            
        Returns:
            ClassificationRule instance
        """
        return ClassificationRule(
            name=rule_dict["name"],
            condition=rule_dict["condition"],
            action=rule_dict["action"],
            priority=rule_dict.get("priority", 3),
            bandwidth_estimate=rule_dict.get("bandwidth_estimate")
        )
