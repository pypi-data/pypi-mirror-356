import socket
import subprocess
import netifaces
import platform
import re
from typing import List, Dict, Union
import os

class NetworkCommands:
    # IP/MAC/Network Interfaces
    @staticmethod
    def get_ip() -> Dict[str, str]:
        """Get all interface IPs"""
        return {
            iface: netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
            for iface in netifaces.interfaces()
            if netifaces.AF_INET in netifaces.ifaddresses(iface)
        }

    @staticmethod
    def get_mac() -> Dict[str, str]:
        """Get all interface MAC addresses"""
        return {
            iface: netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
            for iface in netifaces.interfaces()
            if netifaces.AF_LINK in netifaces.ifaddresses(iface)
        }

    @staticmethod
    def list_interfaces() -> List[str]:
        """List all network interfaces"""
        return netifaces.interfaces()

    # Port Operations
    @staticmethod
    def port_check(port: int) -> bool:
        """Check if port is occupied"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    @staticmethod
    def scan_ports(start: int = 1, end: int = 1024) -> Dict[int, bool]:
        """Scan ports in range"""
        return {port: NetworkCommands.port_check(port) 
                for port in range(start, end + 1)}

    # Connectivity
    @staticmethod
    def ping(host: str, count: int = 4) -> bool:
        """Ping a host"""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        return subprocess.call(
            ['ping', param, str(count), host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0

    @staticmethod
    def traceroute(host: str) -> List[str]:
        """Perform traceroute"""
        param = '-d' if platform.system().lower() == 'windows' else ''
        result = subprocess.run(
            ['tracert' if 'windows' in platform.system().lower() else 'traceroute', param, host],
            capture_output=True,
            text=True
        )
        return result.stdout.splitlines()

    # WiFi Operations (Windows/Linux/macOS)
    @staticmethod
    def list_wifi() -> List[Dict[str, Union[str, float]]]:
        """List available WiFi networks"""
        if platform.system() == 'Windows':
            return NetworkCommands._scan_wifi_windows()
        elif platform.system() == 'Linux':
            return NetworkCommands._scan_wifi_linux()
        elif platform.system() == 'Darwin':
            return NetworkCommands._scan_wifi_mac()
        return []

    @staticmethod
    def _scan_wifi_windows() -> List[Dict[str, Union[str, float]]]:
        """Windows WiFi scanning"""
        try:
            result = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'networks'],
                text=True
            )
            wifis = []
            for line in result.split('\n'):
                if 'SSID' in line:
                    ssid = line.split(':')[1].strip()
                    wifis.append({'ssid': ssid, 'signal': -1.0})
            return wifis
        except:
            return []

    @staticmethod
    def _scan_wifi_linux() -> List[Dict[str, Union[str, float]]]:
        """Linux WiFi scanning"""
        try:
            scan_result = subprocess.check_output(
                ['nmcli', '-t', '-f', 'SSID,SIGNAL', 'device', 'wifi', 'list'],
                text=True
            )
            return [
                {'ssid': parts[0], 'signal': float(parts[1])} 
                for parts in [line.split(':') 
                for line in scan_result.splitlines() if line]
            ]
        except:
            return []

    # Network Info
    @staticmethod
    def public_ip() -> str:
        """Get public IP (without external API)"""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

    @staticmethod
    def dns_lookup(hostname: str) -> str:
        """DNS resolution"""
        return socket.gethostbyname(hostname)

    @staticmethod
    def arp_table() -> Dict[str, str]:
        """Get ARP table"""
        if platform.system() == 'Windows':
            result = subprocess.check_output(['arp', '-a'], text=True)
            return {
                match.group(1): match.group(2)
                for match in re.finditer(
                    r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f-]+)',
                    result,
                    re.IGNORECASE
                )
            }
        else:
            with open('/proc/net/arp') as f:
                return {
                    parts[0]: parts[3]
                    for parts in [line.split() 
                    for line in f.readlines()[1:] if line]
                }