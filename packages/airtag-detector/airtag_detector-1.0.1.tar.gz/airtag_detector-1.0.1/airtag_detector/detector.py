#!/usr/bin/env python3
"""
Apple AirTag Detector Module
Main detection logic for Apple AirTags using Bluetooth LE
"""

import asyncio
import logging
import time
import os
from datetime import datetime
from typing import Set, Dict, Optional
import signal
import sys

try:
    from bleak import BleakScanner, BleakError
    from bleak.backends.device import BLEDevice
    from bleak.backends.scanner import AdvertisementData
except ImportError:
    BleakScanner = None
    BleakError = None
    BLEDevice = None
    AdvertisementData = None

from .homekit_controller import HomeKitController

logger = logging.getLogger(__name__)


class AirTagDetector:
    """Detects Apple AirTags using Bluetooth LE scanning"""
    
    # Apple's company identifier and AirTag-related service UUIDs
    APPLE_COMPANY_ID = 0x004C
    AIRTAG_SERVICE_UUIDS = [
        "FD44",  # Apple's Nearby Interaction service
        "FEAA",  # Eddystone (sometimes used by Find My network)
    ]
    
    def __init__(self, config=None, proximity_threshold=-70, scan_interval=2.0, auto_turn_on_delay=30):
        self.detected_devices: Dict[str, Dict] = {}
        self.scanner: Optional[BleakScanner] = None
        self.running = False
        self.scan_interval = scan_interval
        self.proximity_threshold = proximity_threshold
        self.auto_turn_on_delay = auto_turn_on_delay
        
        # HomeKit integration
        self.homekit_controller = HomeKitController(config)
        self.plug_off_time = None
        self.detection_active = False
        
        # Check if bleak is available
        if not BleakScanner:
            raise ImportError("bleak library not found. Install with: pip install bleak")
        
    async def detection_callback(self, device: BLEDevice, advertisement_data: AdvertisementData):
        """Callback function called when a BLE device is detected"""
        
        # Check if this could be an Apple device
        if not self._is_potential_airtag(device, advertisement_data):
            return
            
        # Check if device is within proximity range
        if device.rssi and device.rssi > self.proximity_threshold:
            device_info = {
                'name': device.name or 'Unknown',
                'address': device.address,
                'rssi': device.rssi,
                'last_seen': datetime.now(),
                'advertisement_data': {
                    'manufacturer_data': advertisement_data.manufacturer_data,
                    'service_uuids': advertisement_data.service_uuids,
                    'local_name': advertisement_data.local_name,
                }
            }
            
            # Log detection
            is_new_detection = device.address not in self.detected_devices
            if is_new_detection:
                logger.info(f"NEW AIRTAG DETECTED: {device_info['name']} ({device.address}) "
                           f"RSSI: {device.rssi} dBm")
                self._log_device_details(device_info)
                
                # Turn off plug on first detection
                if not self.detection_active:
                    await self._handle_airtag_detected()
            else:
                # Update existing device info
                logger.debug(f"AIRTAG STILL IN RANGE: {device_info['name']} ({device.address}) "
                           f"RSSI: {device.rssi} dBm")
                
            self.detected_devices[device.address] = device_info
            
    def _is_potential_airtag(self, device: BLEDevice, advertisement_data: AdvertisementData) -> bool:
        """Check if a device could potentially be an AirTag"""
        
        # Check for Apple company identifier in manufacturer data
        if advertisement_data.manufacturer_data:
            if self.APPLE_COMPANY_ID in advertisement_data.manufacturer_data:
                logger.debug(f"Found Apple device: {device.address}")
                return True
                
        # Check for relevant service UUIDs
        if advertisement_data.service_uuids:
            for uuid in advertisement_data.service_uuids:
                if uuid.upper() in self.AIRTAG_SERVICE_UUIDS:
                    logger.debug(f"Found device with relevant service UUID: {device.address}")
                    return True
                    
        # Check device name patterns
        if device.name:
            # AirTags might appear with various names or no name
            name_lower = device.name.lower()
            if any(keyword in name_lower for keyword in ['airtag', 'findmy', 'apple']):
                logger.debug(f"Found device with suspicious name: {device.name}")
                return True
                
        return False
        
    async def _handle_airtag_detected(self):
        """Handle when AirTag is first detected"""
        self.detection_active = True
        self.plug_off_time = datetime.now()
        await self.homekit_controller.turn_off_plug()
        
    async def _handle_no_airtags(self):
        """Handle when no AirTags are detected"""
        if self.detection_active:
            # Check if enough time has passed since last detection
            if self.plug_off_time:
                time_since_off = (datetime.now() - self.plug_off_time).total_seconds()
                if time_since_off >= self.auto_turn_on_delay:
                    self.detection_active = False
                    self.plug_off_time = None
                    await self.homekit_controller.turn_on_plug()
                    logger.info(f"No AirTags detected for {self.auto_turn_on_delay} seconds - turning plug back on")
        
    def _log_device_details(self, device_info: Dict):
        """Log detailed information about detected device"""
        logger.info("Device Details:")
        logger.info(f"  Address: {device_info['address']}")
        logger.info(f"  Name: {device_info['name']}")
        logger.info(f"  RSSI: {device_info['rssi']} dBm")
        logger.info(f"  Manufacturer Data: {device_info['advertisement_data']['manufacturer_data']}")
        logger.info(f"  Service UUIDs: {device_info['advertisement_data']['service_uuids']}")
        
    def _cleanup_old_devices(self):
        """Remove devices that haven't been seen for a while"""
        current_time = datetime.now()
        timeout_seconds = 30  # Remove devices not seen for 30 seconds
        
        devices_to_remove = []
        for address, device_info in self.detected_devices.items():
            time_since_seen = (current_time - device_info['last_seen']).total_seconds()
            if time_since_seen > timeout_seconds:
                devices_to_remove.append(address)
                logger.info(f"AIRTAG LEFT RANGE: {device_info['name']} ({address})")
                
        for address in devices_to_remove:
            del self.detected_devices[address]
            
        # Check if we should turn the plug back on
        if not self.detected_devices:
            asyncio.create_task(self._handle_no_airtags())
            
    async def start_scanning(self):
        """Start continuous BLE scanning"""
        logger.info("Starting AirTag detector with HomeKit integration...")
        logger.info(f"RSSI threshold: {self.proximity_threshold} dBm (approximately 3 feet)")
        
        # Initialize HomeKit controller
        await self.homekit_controller.initialize()
        
        self.running = True
        
        try:
            while self.running:
                try:
                    # Create scanner for this iteration
                    self.scanner = BleakScanner(
                        detection_callback=self.detection_callback,
                        scanning_mode="active"  # Active scanning for more data
                    )
                    
                    logger.debug("Starting BLE scan...")
                    await self.scanner.start()
                    
                    # Scan for the specified interval
                    await asyncio.sleep(self.scan_interval)
                    
                    await self.scanner.stop()
                    
                    # Cleanup old devices
                    self._cleanup_old_devices()
                    
                    # Show current status
                    if self.detected_devices:
                        logger.info(f"Currently tracking {len(self.detected_devices)} AirTag(s)")
                    else:
                        logger.debug("No AirTags detected in range")
                        
                except BleakError as e:
                    logger.error(f"Bluetooth error: {e}")
                    await asyncio.sleep(5)  # Wait before retrying
                    
                except Exception as e:
                    logger.error(f"Unexpected error during scanning: {e}")
                    await asyncio.sleep(5)
                    
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            await self.stop_scanning()
            
    async def stop_scanning(self):
        """Stop BLE scanning"""
        logger.info("Stopping AirTag detector...")
        self.running = False
        
        if self.scanner:
            try:
                await self.scanner.stop()
            except Exception as e:
                logger.error(f"Error stopping scanner: {e}")
                
        logger.info("AirTag detector stopped")


def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)


async def main():
    """Main function for console script entry point"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/tmp/airtag_detector.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Try to import config
    config = None
    try:
        from . import config as cfg
        config = cfg
    except ImportError:
        logger.warning("No configuration found. Using defaults.")
    
    detector = AirTagDetector(config)
    
    logger.info("Apple AirTag Detector v1.0")
    logger.info("Press Ctrl+C to stop")
    
    # Check if running as root (recommended for Bluetooth access)
    if os.geteuid() != 0:
        logger.warning("Not running as root. You may need sudo for Bluetooth access.")
    
    try:
        await detector.start_scanning()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Failed to start: {e}")
        sys.exit(1)
