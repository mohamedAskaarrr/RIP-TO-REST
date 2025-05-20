import ipaddress
import logging
from typing import Optional, Union

def is_valid_ip(ip: str) -> bool:
    """Validate if a string is a valid IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def setup_logging(level: str = 'INFO') -> None:
    """Configure logging for the application"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def format_metric(metric: Union[int, str]) -> Optional[int]:
    """Format and validate RIP metric"""
    try:
        metric_int = int(metric)
        if 0 <= metric_int <= 16:
            return metric_int
        return None
    except (ValueError, TypeError):
        return None