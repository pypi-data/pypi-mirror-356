# -*- coding: utf-8 -*-

import logging
import subprocess
import re
from typing import Optional, Dict, List
import typer

from my_cli_utilities_common.http_helpers import make_sync_request
from my_cli_utilities_common.config import BaseConfig, LoggingUtils
from .display_managers import DeviceDisplayManager, HostDisplayManager
from .device_filters import DeviceFilter, HostFilter

# Initialize logger and disable noise
logger = LoggingUtils.setup_logger('device_spy_cli')
logging.getLogger("httpx").setLevel(logging.WARNING)

# Create main app
app = typer.Typer(
    name="ds",
    help="📱 Device Spy CLI - Device Management Tools",
    add_completion=False,
    rich_markup_mode="rich"
)


class Config(BaseConfig):
    """Configuration constants for Device Spy CLI."""
    BASE_URL = "https://device-spy-mthor.int.rclabenv.com"
    HOSTS_ENDPOINT = f"{BASE_URL}/api/v1/hosts"
    ALL_DEVICES_ENDPOINT = f"{BASE_URL}/api/v1/hosts/get_all_devices"
    DEVICE_ASSETS_ENDPOINT = f"{BASE_URL}/api/v1/device_assets/"


class DataManager:
    """Centralized data management with caching."""
    
    def __init__(self):
        self._devices_cache = None
        self._hosts_cache = None
    
    def get_devices(self, force_refresh: bool = False) -> Optional[List[Dict]]:
        """Get all devices data with caching."""
        if self._devices_cache is None or force_refresh:
            response_data = make_sync_request(Config.ALL_DEVICES_ENDPOINT)
            self._devices_cache = response_data.get("data", []) if response_data else None
        return self._devices_cache

    def get_hosts(self, force_refresh: bool = False) -> Optional[List[Dict]]:
        """Get all hosts data with caching."""
        if self._hosts_cache is None or force_refresh:
            response_data = make_sync_request(Config.HOSTS_ENDPOINT)
            self._hosts_cache = response_data.get("data", []) if response_data else None
        return self._hosts_cache


class DeviceEnhancer:
    """Enhances device data with additional information."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def enhance_device_info(self, device: Dict) -> Dict:
        """Enhance device with additional data."""
        enhanced = device.copy()
        
        # Add host alias
        hostname = device.get("hostname")
        if hostname:
            hosts = self.data_manager.get_hosts()
            host = HostFilter.find_exact_match(hosts or [], hostname)
            if host and host.get("alias"):
                enhanced["hostname"] = host["alias"]
                enhanced["host_ip"] = hostname
        
        # Add IP:Port for Android
        if device.get("platform") == "android" and device.get("adb_port"):
            enhanced["ip_port"] = f"{hostname}:{device['adb_port']}"
        
        return enhanced


class ConnectionManager:
    """Handles SSH and ADB connections."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def connect_ssh(self, query: str) -> None:
        """Connect via SSH."""
        typer.echo(f"\n🔍 Looking up host...")
        typer.echo(f"   Query: '{query}'")
        
        hosts = self.data_manager.get_hosts()
        host_ip = HostFilter.get_single_host_ip(hosts or [], query)
        
        if host_ip == "not_found":
            typer.echo(f"   ❌ No host found matching '{query}'")
            raise typer.Exit(1)
        elif not self._is_valid_ip(host_ip):
            typer.echo(f"   ❌ Invalid host IP: {host_ip}")
            raise typer.Exit(1)
        
        typer.echo(f"   ✅ Found host IP: {host_ip}")
        typer.echo(f"\n🔗 Connecting via SSH...")
        
        try:
            cmd = ["sshpass", "-p", "123123", "ssh", "-o", "StrictHostKeyChecking=no", 
                   "-o", "ServerAliveInterval=300", f"rcadmin@{host_ip}"]
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            typer.echo(f"   ❌ SSH connection failed: {e}")
            raise typer.Exit(1)
        except FileNotFoundError:
            typer.echo(f"   ❌ sshpass not found. Install: brew install sshpass")
            raise typer.Exit(1)
    
    def connect_adb(self, udid: str) -> None:
        """Connect via ADB."""
        typer.echo(f"\n🔍 Looking up Android device...")
        typer.echo(f"   UDID: {udid}")
        
        devices = self.data_manager.get_devices()
        device = DeviceFilter.find_by_udid(devices or [], udid)
        
        if not device:
            typer.echo(f"   ❌ Device {udid} not found")
            raise typer.Exit(1)
        
        if device.get("is_locked"):
            typer.echo(f"   🔒 Device {udid} is locked")
            raise typer.Exit(1)
        
        if device.get("platform") != "android" or not device.get("adb_port"):
            typer.echo(f"   ❌ Device is not Android or has no ADB port")
            raise typer.Exit(1)
        
        ip_port = f"{device['hostname']}:{device['adb_port']}"
        typer.echo(f"   ✅ Found Android device")
        typer.echo(f"   🌐 Connection: {ip_port}")
        typer.echo(f"\n🔗 Connecting via ADB...")
        
        try:
            cmd = ["adb", "-s", udid, "connect", ip_port]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                typer.echo(f"   ✅ ADB connection successful")
                if result.stdout.strip():
                    typer.echo(f"   📄 Output: {result.stdout.strip()}")
            else:
                typer.echo(f"   ❌ ADB connection failed")
                if result.stderr.strip():
                    typer.echo(f"   📄 Error: {result.stderr.strip()}")
                raise typer.Exit(1)
        except FileNotFoundError:
            typer.echo(f"   ❌ adb not found. Install Android SDK Platform Tools")
            raise typer.Exit(1)
    
    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Validate IP address format."""
        pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(pattern, ip))


# Global instances
data_manager = DataManager()
device_enhancer = DeviceEnhancer(data_manager)
connection_manager = ConnectionManager(data_manager)


# CLI Commands
@app.command("udid")
def get_device_info(udid: str = typer.Argument(..., help="Device UDID to lookup")):
    """📱 Display detailed information for a specific device"""
    typer.echo(f"\n🔍 Looking up device information...")
    typer.echo(f"   UDID: {udid}")
    
    devices = data_manager.get_devices()
    device = DeviceFilter.find_by_udid(devices or [], udid)
    
    if not device:
        typer.echo(f"   ❌ Device with UDID '{udid}' not found")
        raise typer.Exit(1)
    
    typer.echo(f"   ✅ Device found")
    enhanced_device = device_enhancer.enhance_device_info(device)
    DeviceDisplayManager.display_device_info(enhanced_device)


@app.command("devices")
def list_available_devices(platform: str = typer.Argument(..., help="Platform: android or ios")):
    """📋 List available devices for a platform"""
    typer.echo(f"\n🔍 Finding available devices...")
    typer.echo(f"   Platform: {platform}")
    
    devices = data_manager.get_devices()
    available_devices = DeviceFilter.get_available_devices(devices or [], platform)
    
    typer.echo(f"   ✅ Found {len(available_devices)} available {platform} devices")
    
    if available_devices:
        title = f"📱 Available {platform.capitalize()} Devices"
        DeviceDisplayManager.display_device_list(available_devices, title)
    else:
        typer.echo(f"\n   ℹ️  No available {platform} devices found")


@app.command("host")
def find_host_info(
    query: str = typer.Argument(..., help="Host query string (hostname or alias)"),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed host information")
):
    """🖥️  Find host information by query"""
    typer.echo(f"\n🔍 Searching for hosts...")
    typer.echo(f"   Query: '{query}'")
    
    hosts = data_manager.get_hosts()
    found_hosts = HostFilter.by_query(hosts or [], query)
    
    if not found_hosts:
        typer.echo(f"   ❌ No hosts found matching '{query}'")
        raise typer.Exit(1)
    
    typer.echo(f"   ✅ Found {len(found_hosts)} matching host(s)")
    
    if detailed and len(found_hosts) == 1:
        host = found_hosts[0]
        hostname = host.get("hostname", "")
        devices = data_manager.get_devices()
        host_devices = DeviceFilter.by_host(devices or [], hostname)
        HostDisplayManager.display_detailed_host_info(host, host_devices)
    elif detailed and len(found_hosts) > 1:
        typer.echo(f"   ⚠️  Multiple hosts found. Please be more specific for detailed view:")
        HostDisplayManager.display_host_results(found_hosts, query)
    else:
        HostDisplayManager.display_host_results(found_hosts, query)
        if len(found_hosts) == 1:
            typer.echo(f"\n💡 Use 'ds host {query} --detailed' for comprehensive host information")


@app.command("ssh")
def ssh_connect(query: str = typer.Argument(..., help="Host query string to connect via SSH")):
    """🔗 Connect to a host via SSH"""
    connection_manager.connect_ssh(query)


@app.command("connect")
def adb_connect(udid: str = typer.Argument(..., help="Android device UDID to connect via ADB")):
    """🤖 Connect to Android device via ADB"""
    connection_manager.connect_adb(udid)


@app.command("android-ip")
def get_android_connection(udid: str = typer.Argument(..., help="Android device UDID")):
    """🤖 Get Android device IP:Port for ADB connection"""
    devices = data_manager.get_devices()
    device = DeviceFilter.find_by_udid(devices or [], udid)
    
    if not device:
        typer.echo("not_found")
        return "not_found"
    
    if device.get("is_locked"):
        typer.echo("locked")
        return "locked"
    elif device.get("platform") == "android" and device.get("adb_port"):
        ip_port = f"{device.get('hostname')}:{device.get('adb_port')}"
        typer.echo(ip_port)
        return ip_port
    else:
        typer.echo("not_android")
        return "not_android"


@app.command("host-ip")
def get_host_ip_for_script(query: str = typer.Argument(..., help="Host query string")):
    """🌐 Get host IP address for script usage"""
    hosts = data_manager.get_hosts()
    result = HostFilter.get_single_host_ip(hosts or [], query)
    typer.echo(result)
    return result


# Legacy compatibility class
class DeviceSpyCli:
    """Legacy class for backward compatibility with .startup.sh"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_android_ip_port(self, udid: str) -> str:
        """Legacy method for getting Android IP:Port."""
        devices = self.data_manager.get_devices()
        device = DeviceFilter.find_by_udid(devices or [], udid)
        
        if not device:
            return "not_found"
        if device.get("is_locked"):
            return "locked"
        elif device.get("platform") == "android" and device.get("adb_port"):
            return f"{device.get('hostname')}:{device.get('adb_port')}"
        else:
            return "not_android"
    
    def get_host_ip_for_script(self, query_string: str) -> str:
        """Legacy method for getting host IP."""
        hosts = self.data_manager.get_hosts()
        return HostFilter.get_single_host_ip(hosts or [], query_string)


def main_ds_function():
    """Main entry point for Device Spy CLI"""
    app()


if __name__ == "__main__":
    main_ds_function()
