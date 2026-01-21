"""
Network Presence Detection Module
Handles detecting device presence on the local network
"""
import subprocess
import platform
from datetime import datetime
from typing import Dict, Optional
from apscheduler.schedulers.background import BackgroundScheduler

class PresenceDetector:
    """Manages network presence detection."""

    def __init__(self, device_ip: str, scan_interval: int = 60, scan_method: str = 'ping'):
        """
        Initialize the presence detector.

        Args:
            device_ip: IP address of the device to detect
            scan_interval: How often to scan (in seconds)
            scan_method: Method to use for detection ('ping' or 'arp-scan')
        """
        self.device_ip = device_ip
        self.scan_interval = scan_interval
        self.scan_method = scan_method
        self.scheduler = BackgroundScheduler()
        self.last_status = None
        self.last_check = None
        self.is_running = False

    def ping_device(self) -> bool:
        """
        Ping the device to check if it's online.

        Returns:
            True if device responds, False otherwise
        """
        # Determine ping parameters based on OS
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        # Use -W for timeout on Linux/Mac, -w on Windows
        timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'

        try:
            # Ping with 1 packet and 1 second timeout
            command = ['ping', param, '1', timeout_param, '1', self.device_ip]
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, Exception):
            return False

    def check_presence(self) -> bool:
        """
        Check if the device is present on the network.

        Returns:
            True if device is present, False otherwise
        """
        if self.scan_method == 'ping':
            is_present = self.ping_device()
        else:
            # Default to ping if method is unknown
            is_present = self.ping_device()

        self.last_status = is_present
        self.last_check = datetime.now()

        return is_present

    def get_status(self) -> Dict[str, any]:
        """
        Get the current presence status.

        Returns:
            Dictionary containing:
            {
                'present': bool,
                'device_ip': str,
                'last_check': ISO timestamp,
                'scan_method': str,
                'scan_interval': int
            }
        """
        # If never checked, check now
        if self.last_status is None:
            self.check_presence()

        return {
            'present': self.last_status,
            'device_ip': self.device_ip,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'scan_method': self.scan_method,
            'scan_interval': self.scan_interval
        }

    def start_monitoring(self):
        """Start background monitoring of device presence."""
        if self.is_running:
            return

        # Do an immediate check
        self.check_presence()

        # Schedule periodic checks
        self.scheduler.add_job(
            self.check_presence,
            'interval',
            seconds=self.scan_interval,
            id='presence_check'
        )
        self.scheduler.start()
        self.is_running = True

    def stop_monitoring(self):
        """Stop background monitoring."""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False

    def update_config(self, device_ip: Optional[str] = None,
                      scan_interval: Optional[int] = None,
                      scan_method: Optional[str] = None):
        """
        Update detector configuration.

        Args:
            device_ip: New device IP
            scan_interval: New scan interval
            scan_method: New scan method
        """
        restart_needed = False

        if device_ip and device_ip != self.device_ip:
            self.device_ip = device_ip
            restart_needed = True

        if scan_interval and scan_interval != self.scan_interval:
            self.scan_interval = scan_interval
            restart_needed = True

        if scan_method and scan_method != self.scan_method:
            self.scan_method = scan_method
            restart_needed = True

        # Restart monitoring if running and config changed
        if restart_needed and self.is_running:
            self.stop_monitoring()
            self.start_monitoring()
