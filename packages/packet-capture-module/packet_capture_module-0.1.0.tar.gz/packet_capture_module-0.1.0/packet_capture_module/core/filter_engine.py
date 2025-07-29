"""
Modern Filter Engine with BPF and manual filtering support.
Enhanced with better type safety, performance optimizations, and extended filtering capabilities.
"""
from typing import List, Tuple, Optional, Pattern, Callable, Any
import re
from scapy.arch.common import compile_filter
from scapy.all import Ether, IP, IPv6, TCP, UDP, ICMP
from dataclasses import dataclass
from utils.config_handler import get_config
from utils.logging_utils import setup_logger
from packet_capture_module.core.packet import Packet

logger = setup_logger("filter_engine")

@dataclass
class FilterRule:
    """Container for filter rule with compiled versions"""
    original: str
    compiled: Optional[Callable[[Any], bool]] = None
    manual_matcher: Optional[Callable[[Packet], bool]] = None

class FilterEngine:
    def __init__(self, config_path: str = "config/config.yaml"):
        self._rules: List[FilterRule] = []
        self._port_range_pattern: Pattern = re.compile(r'^(\d+)-(\d+)$')
        
        # Load centralized configuration
        self.config = get_config(config_path)
        filter_config = self.config.get_filter_config()
        
        # Initialize with filter rules from config
        if filter_config.enable:
            self.update_filters(filter_config.rules)
        else:
            logger.info("Filtering is disabled in configuration")

    def update_filters(self, rules: List[str]) -> bool:
        """Update active filters with validation and compilation"""
        new_rules = []
        success = True
        
        for rule in rules:
            try:
                validated_rule = self._validate_and_compile(rule)
                if validated_rule:
                    new_rules.append(validated_rule)
                else:
                    success = False
            except Exception as e:
                logger.error(f"Error processing rule '{rule}': {e}", exc_info=True)
                success = False
        
        if success:
            self._rules = new_rules
            logger.info(f"Updated filters: {len(self._rules)} active rules")
        return success

    def _validate_and_compile(self, rule: str) -> Optional[FilterRule]:
        """Validate and compile a single filter rule"""
        rule = rule.strip()
        if not rule:
            return None

        # First try to compile as BPF
        try:
            bpf_func = compile_filter(rule)
            return FilterRule(original=rule, compiled=bpf_func)
        except Exception:
            pass  # Not a BPF rule, try manual matching

        # Handle manual filter types
        manual_matcher = self._create_manual_matcher(rule)
        if manual_matcher:
            return FilterRule(original=rule, manual_matcher=manual_matcher)

        logger.error(f"Invalid rule syntax: {rule}")
        return None

    def _create_manual_matcher(self, rule: str) -> Optional[Callable[[Packet], bool]]:
        """Create manual filter matching function"""
        rule_lower = rule.lower()
        
        # Port matching
        if rule_lower.startswith("port "):
            port_spec = rule[5:].strip()
            return self._create_port_matcher(port_spec)
        
        # Host matching
        elif rule_lower.startswith(("src host ", "dst host ")):
            direction, _, ip = rule.partition("host ")
            direction = direction.strip().lower()
            ip = ip.strip()
            return lambda p: self._match_host(p, direction, ip)
        
        # Protocol matching
        elif rule_lower in {"tcp", "udp", "icmp", "ip", "ip6"}:
            return lambda p: p.get_protocol().lower() == rule_lower
        
        return None

    def _create_port_matcher(self, port_spec: str) -> Callable[[Packet], bool]:
        """Create function to match port ranges"""
        if '-' in port_spec:
            try:
                start, end = map(int, port_spec.split('-'))
                return lambda p: (
                    (p.dst_port and start <= p.dst_port <= end) or
                    (p.src_port and start <= p.src_port <= end)
                )
            except ValueError:
                logger.warning(f"Invalid port range: {port_spec}")
                return lambda p: False
        
        try:
            port = int(port_spec)
            return lambda p: p.dst_port == port or p.src_port == port
        except ValueError:
            logger.warning(f"Invalid port: {port_spec}")
            return lambda p: False

    def _match_host(self, packet: Packet, direction: str, ip: str) -> bool:
        """Match host IP with direction (src/dst)"""
        if direction == "src":
            return packet.src_ip == ip
        return packet.dst_ip == ip

    def apply_filter(self, packet: Packet) -> bool:
        """
        Apply all filters to the packet.
        Returns True if packet matches any filter rule (OR logic).
        """
        # Check if filtering is enabled
        if not self.config.get_filter_config().enable:
            return True  # Allow all packets when filtering is disabled
            
        if not self._rules:
            return True  # No filters = allow all

        try:
            for rule in self._rules:
                # Check BPF compiled rules
                if rule.compiled:
                    try:
                        # For BPF rules, we need to check if the packet matches the BPF filter
                        # Since we can't easily apply BPF to our Packet object, we'll use manual matching
                        # for common BPF patterns
                        if self._match_bpf_rule(rule.original, packet):
                            return True
                    except Exception as e:
                        logger.debug(f"BPF rule '{rule.original}' failed: {e}")
                
                # Check manual matcher rules
                if rule.manual_matcher and rule.manual_matcher(packet):
                    return True
                    
            return False
        except Exception as e:
            logger.error(f"Filter error on packet: {e}", exc_info=True)
            return False

    def _match_bpf_rule(self, rule: str, packet: Packet) -> bool:
        """Match common BPF patterns manually"""
        rule_lower = rule.lower()
        
        # Handle "ip multicast" rule
        if rule_lower == "ip multicast":
            return packet.is_multicast()
        
        # Handle "udp portrange X-Y" rule
        if "udp portrange" in rule_lower:
            # Extract port range from rule
            port_range_match = re.search(r'portrange (\d+)-(\d+)', rule_lower)
            if port_range_match:
                start_port = int(port_range_match.group(1))
                end_port = int(port_range_match.group(2))
                return (packet.get_protocol().upper() == "UDP" and 
                       ((packet.dst_port and start_port <= packet.dst_port <= end_port) or
                        (packet.src_port and start_port <= packet.src_port <= end_port)))
        
        # Handle "tcp" rule
        if rule_lower == "tcp":
            return packet.get_protocol().upper() == "TCP"
        
        # Handle "udp" rule
        if rule_lower == "udp":
            return packet.get_protocol().upper() == "UDP"
        
        # Handle "icmp" rule
        if rule_lower == "icmp":
            return packet.get_protocol().upper() == "ICMP"
        
        # Handle "ip" rule
        if rule_lower == "ip":
            return packet.get_protocol().upper() in ["TCP", "UDP", "ICMP"]
        
        # If we can't handle the BPF rule, allow the packet (fail open)
        logger.debug(f"Unhandled BPF rule: {rule}, allowing packet")
        return True

    def get_active_filters(self) -> List[str]:
        """Get list of active filter rules"""
        return [rule.original for rule in self._rules]

    def reload_config(self) -> None:
        """Reload configuration and update filters"""
        self.config.reload_config()
        filter_config = self.config.get_filter_config()
        
        if filter_config.enable:
            self.update_filters(filter_config.rules)
        else:
            self._rules = []
            logger.info("Filtering disabled after config reload")

    def __str__(self) -> str:
        return f"FilterEngine(rules={self.get_active_filters()})"

    def __len__(self) -> int:
        return len(self._rules)