# -*- coding: utf-8 -*-

import json
import logging
from typing import Optional, Dict, List, Any
import typer
from my_cli_utilities_common.http_helpers import make_sync_request
from my_cli_utilities_common.pagination import paginated_display
from my_cli_utilities_common.config import BaseConfig, LoggingUtils

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

# Configuration constants
class Config(BaseConfig):
    BASE_URL = "https://device-spy-mthor.int.rclabenv.com"
    HOSTS_ENDPOINT = f"{BASE_URL}/api/v1/hosts"
    ALL_DEVICES_ENDPOINT = f"{BASE_URL}/api/v1/hosts/get_all_devices"
    LABELS_ENDPOINT = f"{BASE_URL}/api/v1/labels/"
    DEVICE_ASSETS_ENDPOINT = f"{BASE_URL}/api/v1/device_assets/"


class DeviceDataManager:
    """Handles device data retrieval and caching."""
    
    def __init__(self):
        self._devices_cache = None
        self._hosts_cache = None
    
    def get_devices_data(self, force_refresh: bool = False) -> Optional[List[Dict]]:
        """Get all devices data from API with caching."""
        if self._devices_cache is None or force_refresh:
            response_data = make_sync_request(Config.ALL_DEVICES_ENDPOINT)
            self._devices_cache = response_data.get("data", []) if response_data else None
        return self._devices_cache

    def get_hosts_data(self, force_refresh: bool = False) -> Optional[List[Dict]]:
        """Get all hosts data from API with caching."""
        if self._hosts_cache is None or force_refresh:
            response_data = make_sync_request(Config.HOSTS_ENDPOINT)
            self._hosts_cache = response_data.get("data", []) if response_data else None
        return self._hosts_cache

    def find_device_by_udid(self, udid: str) -> Optional[Dict]:
        """Find a specific device by UDID."""
        devices = self.get_devices_data()
        if not devices:
            return None
        
        for device in devices:
            if device.get("udid") == udid:
                return device
        return None

    def get_available_devices(self, platform: str) -> List[Dict]:
        """Get available devices for a specific platform."""
        devices = self.get_devices_data()
        if not devices:
            return []
        
        return [
            device for device in devices
            if (not device.get("is_locked") and 
                not device.get("is_simulator") and 
                device.get("platform") == platform)
        ]


class DeviceDisplayManager:
    """Handles device information display."""
    
    @staticmethod
    def display_device_info(device: Dict) -> None:
        """Display device information in a user-friendly format."""
        typer.echo(f"\n📱 Device Information")
        typer.echo("=" * Config.DISPLAY_WIDTH)
        
        # Extract key information
        udid = device.get("udid", "N/A")
        platform = device.get("platform", "N/A")
        model = device.get("model", "N/A")
        os_version = device.get("platform_version", "N/A")
        hostname = device.get("hostname", "N/A")
        host_ip = device.get("host_ip", "N/A")
        location = device.get("location", "N/A")
        is_locked = device.get("is_locked", False)
        ip_port = device.get("ip_port", "N/A")
        
        typer.echo(f"📋 UDID:           {udid}")
        typer.echo(f"🔧 Platform:       {platform}")
        typer.echo(f"📟 Model:          {model}")
        typer.echo(f"🎯 OS Version:     {os_version}")
        typer.echo(f"🖥️  Host:           {hostname}")
        if host_ip != "N/A":
            typer.echo(f"🌐 Host IP:        {host_ip}")
        if location != "N/A":
            typer.echo(f"📍 Location:       {location}")
        if ip_port != "N/A":
            typer.echo(f"🌐 IP:Port:        {ip_port}")
        
        status = "🔒 Locked" if is_locked else "✅ Available"
        typer.echo(f"🔐 Status:         {status}")
        typer.echo("=" * Config.DISPLAY_WIDTH)

    @staticmethod
    def display_device_list(devices: List[Dict], title: str) -> None:
        """Display a list of devices with pagination."""
        def display_device(device: Dict, index: int) -> None:
            udid = device.get("udid", "N/A")
            model = device.get("model", "N/A")
            os_version = device.get("platform_version", "N/A")
            hostname = device.get("hostname", "N/A")
            
            typer.echo(f"\n{index}. {model} ({os_version})")
            typer.echo(f"   UDID: {udid}")
            typer.echo(f"   Host: {hostname}")
        
        paginated_display(devices, display_device, title, Config.PAGE_SIZE, Config.DISPLAY_WIDTH)
        
        typer.echo("\n" + "=" * Config.DISPLAY_WIDTH)
        typer.echo(f"💡 Use 'ds udid <udid>' to get detailed information")
        typer.echo("=" * Config.DISPLAY_WIDTH)

    @staticmethod
    def display_host_results(hosts: List[Dict], query: str) -> None:
        """Display host search results."""
        typer.echo(f"\n🔍 Host Search Results for: '{query}'")
        typer.echo("=" * Config.DISPLAY_WIDTH)
        
        for i, host in enumerate(hosts, 1):
            hostname = host.get("hostname", "N/A")
            alias = host.get("alias", "N/A")
            typer.echo(f"{i}. {alias} ({hostname})")
        
        typer.echo("=" * Config.DISPLAY_WIDTH)


class DeviceEnhancementManager:
    """Handles device data enhancement with additional information."""
    
    def __init__(self, data_manager: DeviceDataManager):
        self.data_manager = data_manager
    
    def get_device_location_from_assets(self, udid: str) -> Optional[str]:
        """Fetch device location from assets by UDID."""
        response_data = make_sync_request(Config.DEVICE_ASSETS_ENDPOINT)
        if response_data:
            device_assets = response_data.get("data", [])
            for device_asset in device_assets:
                if device_asset.get("udid") == udid:
                    return device_asset.get("location")
        return None

    def get_host_alias(self, host_ip: str) -> Optional[str]:
        """Fetch host alias by IP address."""
        hosts = self.data_manager.get_hosts_data()
        if hosts:
            for host in hosts:
                if host.get("hostname") == host_ip:
                    return host.get("alias")
        return None

    def enhance_device_info(self, device: Dict) -> Dict:
        """Enhance device information with additional data."""
        enhanced_device = device.copy()
        udid = device.get("udid")
        original_hostname = device.get("hostname")

        # Get host alias and preserve original IP
        if original_hostname:
            host_alias = self.get_host_alias(original_hostname)
            if host_alias:
                enhanced_device["hostname"] = host_alias
                enhanced_device["host_ip"] = original_hostname

        # Add IP:Port for Android devices
        if device.get("platform") == "android":
            adb_port = device.get("adb_port")
            if adb_port and original_hostname:
                enhanced_device["ip_port"] = f"{original_hostname}:{adb_port}"

        # Get location information
        if udid:
            location = self.get_device_location_from_assets(udid)
            if location:
                enhanced_device["location"] = location

        # Clean up unnecessary fields
        for key in ["is_simulator", "remote_control", "adb_port"]:
            enhanced_device.pop(key, None)

        return enhanced_device


class HostManager:
    """Handles host-related operations."""
    
    def __init__(self, data_manager: DeviceDataManager):
        self.data_manager = data_manager
    
    def find_hosts_by_query(self, query_string: str) -> List[Dict]:
        """Find hosts based on a query string."""
        hosts = self.data_manager.get_hosts_data()
        if not hosts:
            return []
        
        query_lower = query_string.lower()
        found_hosts = []
        
        for host in hosts:
            hostname = host.get("hostname", "").lower()
            alias = host.get("alias", "").lower()
            
            if query_lower in hostname or query_lower in alias:
                found_hosts.append(host)
        
        return found_hosts

    def get_single_host_ip(self, query_string: str) -> str:
        """Get single host IP for script usage."""
        found_hosts = self.find_hosts_by_query(query_string)
        
        if not found_hosts:
            return "not_found"
        elif len(found_hosts) == 1:
            return found_hosts[0].get("hostname", "error")
        else:
            # Multiple results, try exact match
            for host in found_hosts:
                if (host.get("hostname", "").lower() == query_string.lower() or 
                    host.get("alias", "").lower() == query_string.lower()):
                    return host.get("hostname", "error")
            # No exact match, return first result
            return found_hosts[0].get("hostname", "error")


# Global managers
data_manager = DeviceDataManager()
display_manager = DeviceDisplayManager()
enhancement_manager = DeviceEnhancementManager(data_manager)
host_manager = HostManager(data_manager)


# Command definitions
@app.command("udid")
def get_device_info(udid: str = typer.Argument(..., help="Device UDID to lookup")):
    """📱 Display detailed information for a specific device"""
    typer.echo(f"\n🔍 Looking up device information...")
    typer.echo(f"   UDID: {udid}")
    
    device = data_manager.find_device_by_udid(udid)
    if not device:
        typer.echo(f"   ❌ Device with UDID '{udid}' not found")
        raise typer.Exit(1)
    
    typer.echo(f"   ✅ Device found")
    enhanced_device = enhancement_manager.enhance_device_info(device)
    display_manager.display_device_info(enhanced_device)


@app.command("devices")
def list_available_devices(platform: str = typer.Argument(..., help="Platform: android or ios")):
    """📋 List available devices for a platform"""
    typer.echo(f"\n🔍 Finding available devices...")
    typer.echo(f"   Platform: {platform}")
    
    available_devices = data_manager.get_available_devices(platform)
    typer.echo(f"   ✅ Found {len(available_devices)} available {platform} devices")
    
    if available_devices:
        title = f"📱 Available {platform.capitalize()} Devices"
        display_manager.display_device_list(available_devices, title)
    else:
        typer.echo(f"\n   ℹ️  No available {platform} devices found")


@app.command("host")
def find_host_info(query: str = typer.Argument(..., help="Host query string (hostname or alias)")):
    """🖥️  Find host information by query"""
    typer.echo(f"\n🔍 Searching for hosts...")
    typer.echo(f"   Query: '{query}'")
    
    found_hosts = host_manager.find_hosts_by_query(query)
    
    if not found_hosts:
        typer.echo(f"   ❌ No hosts found matching '{query}'")
        raise typer.Exit(1)
    
    typer.echo(f"   ✅ Found {len(found_hosts)} matching host(s)")
    display_manager.display_host_results(found_hosts, query)


@app.command("android-ip")
def get_android_connection(udid: str = typer.Argument(..., help="Android device UDID")):
    """🤖 Get Android device IP:Port for ADB connection"""
    device = data_manager.find_device_by_udid(udid)
    
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
    result = host_manager.get_single_host_ip(query)
    typer.echo(result)
    return result


# Legacy method support for backward compatibility
class DeviceSpyCli:
    """Legacy class for backward compatibility."""
    
    def __init__(self):
        self.data_manager = data_manager
        self.display_manager = display_manager
        self.enhancement_manager = enhancement_manager
        self.host_manager = host_manager
    
    def get_android_ip_port(self, udid: str) -> str:
        """Legacy method: Get Android device IP:Port for ADB connection."""
        return get_android_connection.callback(udid)
    
    def get_host_ip_for_script(self, query_string: str) -> str:
        """Legacy method: Get host IP for script usage."""
        return get_host_ip_for_script.callback(query_string)


def main_ds_function():
    """Main entry point for Device Spy CLI"""
    app()


if __name__ == "__main__":
    main_ds_function()
