import re
from typing import Dict, Union

def parse_natural_language(text: str) -> Dict[str, Union[str, int]]:
    """Extract parameters from voice commands"""
    # Port detection: "scan ports 1 to 100" → {'start': 1, 'end': 100}
    port_scan = re.search(r'scan ports (\d+) to (\d+)', text)
    if port_scan:
        return {'command': 'scan_ports', 'start': int(port_scan.group(1)), 'end': int(port_scan.group(2))}
    
    # Host detection: "ping google.com" → {'host': 'google.com'}
    host_match = re.search(r'(ping|trace) (.+)', text)
    if host_match:
        return {'command': host_match.group(1), 'host': host_match.group(2)}
    
    # Default to direct command mapping
    return {'command': text.strip()}