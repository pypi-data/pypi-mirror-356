#!/usr/bin/env python3
"""
Test script to verify Bluetooth functionality on Raspberry Pi
"""

import sys
import subprocess
import asyncio

def test_bluetooth_service():
    """Test if Bluetooth service is running"""
    try:
        result = subprocess.run(['systemctl', 'is-active', 'bluetooth'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip() == 'active':
            print("✓ Bluetooth service is running")
            return True
        else:
            print("✗ Bluetooth service is not running")
            return False
    except Exception as e:
        print(f"✗ Error checking Bluetooth service: {e}")
        return False

def test_hci_device():
    """Test if HCI device is available"""
    try:
        result = subprocess.run(['hciconfig'], capture_output=True, text=True)
        if result.returncode == 0 and 'hci0' in result.stdout:
            print("✓ HCI device (hci0) is available")
            return True
        else:
            print("✗ No HCI device found")
            print("Try: sudo hciconfig hci0 up")
            return False
    except Exception as e:
        print(f"✗ Error checking HCI device: {e}")
        return False

async def test_bleak_import():
    """Test if bleak library can be imported and used"""
    try:
        from bleak import BleakScanner
        print("✓ Bleak library imported successfully")
        
        # Try to create a scanner
        scanner = BleakScanner()
        print("✓ BleakScanner created successfully")
        return True
    except ImportError:
        print("✗ Bleak library not found")
        print("Install with: pip install bleak")
        return False
    except Exception as e:
        print(f"✗ Error with bleak: {e}")
        return False

async def test_ble_scan():
    """Test basic BLE scanning"""
    try:
        from bleak import BleakScanner
        
        print("Testing BLE scan (5 seconds)...")
        devices = await BleakScanner.discover(timeout=5.0)
        print(f"✓ Found {len(devices)} BLE devices")
        
        for device in devices[:3]:  # Show first 3 devices
            print(f"  - {device.name or 'Unknown'} ({device.address}) RSSI: {device.rssi}")
            
        return True
    except Exception as e:
        print(f"✗ Error during BLE scan: {e}")
        return False

async def main():
    """Run all tests"""
    print("Raspberry Pi Bluetooth/BLE Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Bluetooth service
    if test_bluetooth_service():
        tests_passed += 1
    
    # Test 2: HCI device
    if test_hci_device():
        tests_passed += 1
    
    # Test 3: Bleak import
    if await test_bleak_import():
        tests_passed += 1
    
    # Test 4: BLE scan
    if await test_ble_scan():
        tests_passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! Your system is ready for AirTag detection.")
    else:
        print("✗ Some tests failed. Please address the issues above.")
        print("\nCommon solutions:")
        print("- Run with sudo for Bluetooth access")
        print("- Install bleak: pip install bleak")
        print("- Enable Bluetooth: sudo systemctl start bluetooth")
        print("- Bring up HCI device: sudo hciconfig hci0 up")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test failed with error: {e}")
