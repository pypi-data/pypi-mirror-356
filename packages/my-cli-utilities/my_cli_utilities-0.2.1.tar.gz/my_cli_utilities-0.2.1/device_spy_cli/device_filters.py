# -*- coding: utf-8 -*-

from typing import List, Dict, Optional


class DeviceFilter:
    """Utility class for filtering devices based on various criteria."""
    
    @staticmethod
    def by_platform(devices: List[Dict], platform: str) -> List[Dict]:
        """Filter devices by platform."""
        if not devices:
            return []
        return [device for device in devices if device.get("platform") == platform]
    
    @staticmethod
    def by_availability(devices: List[Dict], available_only: bool = True) -> List[Dict]:
        """Filter devices by availability status."""
        if not devices:
            return []
        if available_only:
            return [device for device in devices if not device.get("is_locked", False)]
        return [device for device in devices if device.get("is_locked", False)]
    
    @staticmethod
    def by_host(devices: List[Dict], hostname: str) -> List[Dict]:
        """Filter devices by hostname."""
        if not devices:
            return []
        return [device for device in devices if device.get("hostname") == hostname]
    
    @staticmethod
    def exclude_simulators(devices: List[Dict]) -> List[Dict]:
        """Exclude simulator devices."""
        if not devices:
            return []
        return [device for device in devices if not device.get("is_simulator", False)]
    
    @staticmethod
    def get_available_devices(devices: List[Dict], platform: str) -> List[Dict]:
        """Get available devices for a specific platform (non-locked, non-simulator)."""
        if not devices:
            return []
        
        filtered = DeviceFilter.by_platform(devices, platform)
        filtered = DeviceFilter.exclude_simulators(filtered)
        filtered = DeviceFilter.by_availability(filtered, available_only=True)
        
        return filtered
    
    @staticmethod
    def find_by_udid(devices: List[Dict], udid: str) -> Optional[Dict]:
        """Find a device by UDID."""
        if not devices:
            return None
        
        for device in devices:
            if device.get("udid") == udid:
                return device
        return None
    
    @staticmethod
    def get_android_with_adb(devices: List[Dict]) -> List[Dict]:
        """Get Android devices that have ADB port configured."""
        android_devices = DeviceFilter.by_platform(devices, "android")
        return [device for device in android_devices if device.get("adb_port")]


class HostFilter:
    """Utility class for filtering hosts based on various criteria."""
    
    @staticmethod
    def by_query(hosts: List[Dict], query: str) -> List[Dict]:
        """Filter hosts by query string (hostname or alias)."""
        if not hosts:
            return []
        
        query_lower = query.lower()
        found_hosts = []
        
        for host in hosts:
            hostname = host.get("hostname", "").lower()
            alias = host.get("alias", "").lower()
            
            if query_lower in hostname or query_lower in alias:
                found_hosts.append(host)
        
        return found_hosts
    
    @staticmethod
    def find_exact_match(hosts: List[Dict], query: str) -> Optional[Dict]:
        """Find exact match for hostname or alias."""
        if not hosts:
            return None
        
        query_lower = query.lower()
        
        for host in hosts:
            hostname = host.get("hostname", "").lower()
            alias = host.get("alias", "").lower()
            
            if hostname == query_lower or alias == query_lower:
                return host
        
        return None
    
    @staticmethod
    def get_single_host_ip(hosts: List[Dict], query: str) -> str:
        """Get single host IP for script usage with intelligent matching."""
        found_hosts = HostFilter.by_query(hosts, query)
        
        if not found_hosts:
            return "not_found"
        elif len(found_hosts) == 1:
            return found_hosts[0].get("hostname", "error")
        else:
            # Multiple results, try exact match first
            exact_match = HostFilter.find_exact_match(found_hosts, query)
            if exact_match:
                return exact_match.get("hostname", "error")
            # No exact match, return first result
            return found_hosts[0].get("hostname", "error") 