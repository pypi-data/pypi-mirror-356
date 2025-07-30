#!/usr/bin/env python3
"""
Setup and Installation Module for AirTag Detector
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_system_requirements():
    """Check if system requirements are met"""
    print("Checking system requirements...")
    
    # Check if running on Linux
    if not sys.platform.startswith('linux'):
        print("❌ This package is designed for Linux systems (Raspberry Pi)")
        return False
    
    # Check if Bluetooth is available
    try:
        result = subprocess.run(['which', 'bluetoothctl'], capture_output=True)
        if result.returncode != 0:
            print("❌ Bluetooth tools not found. Install with: sudo apt install bluetooth bluez")
            return False
    except Exception:
        print("❌ Cannot check Bluetooth availability")
        return False
    
    # Check if running as root for system installation
    if os.geteuid() != 0:
        print("⚠️  Not running as root. Some features may require sudo.")
    
    print("✅ System requirements check passed")
    return True

def install_system_dependencies():
    """Install required system dependencies"""
    print("Installing system dependencies...")
    
    if os.geteuid() != 0:
        print("❌ Root access required for system package installation")
        print("Please run: sudo python -m airtag_detector.setup")
        return False
    
    try:
        # Update package list
        subprocess.run(['apt', 'update'], check=True)
        
        # Install required packages
        packages = [
            'python3', 'python3-pip', 'python3-venv',
            'bluetooth', 'bluez', 'libbluetooth-dev'
        ]
        subprocess.run(['apt', 'install', '-y'] + packages, check=True)
        
        # Enable and start Bluetooth service
        subprocess.run(['systemctl', 'enable', 'bluetooth'], check=True)
        subprocess.run(['systemctl', 'start', 'bluetooth'], check=True)
        
        print("✅ System dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing system dependencies: {e}")
        return False

def install_systemd_service():
    """Install systemd service"""
    print("Installing systemd service...")
    
    if os.geteuid() != 0:
        print("❌ Root access required for systemd service installation")
        return False
    
    try:
        # Find the package installation directory
        import airtag_detector
        package_dir = Path(airtag_detector.__file__).parent
        
        # Copy service file
        service_source = package_dir / "templates" / "airtag-detector.service"
        service_dest = Path("/etc/systemd/system/airtag-detector.service")
        
        if service_source.exists():
            shutil.copy2(service_source, service_dest)
            
            # Reload systemd and enable service
            subprocess.run(['systemctl', 'daemon-reload'], check=True)
            subprocess.run(['systemctl', 'enable', 'airtag-detector.service'], check=True)
            
            print("✅ Systemd service installed successfully")
            return True
        else:
            print(f"❌ Service template not found at {service_source}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing systemd service: {e}")
        return False

def create_config_directory():
    """Create configuration directory and copy template"""
    print("Setting up configuration...")
    
    config_dir = Path.home() / ".config" / "airtag-detector"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = config_dir / "config.py"
    
    if not config_file.exists():
        try:
            # Find the package installation directory
            import airtag_detector
            package_dir = Path(airtag_detector.__file__).parent
            
            # Copy config template
            template_source = package_dir / "configs" / "config.py.template"
            if template_source.exists():
                shutil.copy2(template_source, config_file)
                print(f"✅ Configuration template created at {config_file}")
            else:
                # Create basic config if template not found
                basic_config = '''# AirTag Detector Configuration
HOME_ASSISTANT_URL = ""
HOME_ASSISTANT_TOKEN = ""
HOME_ASSISTANT_ENTITY_ID = "switch.smart_plug"
AUTO_TURN_ON_DELAY = 30
DEBUG_HOMEKIT = True
PROXIMITY_RSSI_THRESHOLD = -70
'''
                config_file.write_text(basic_config)
                print(f"✅ Basic configuration created at {config_file}")
                
        except Exception as e:
            print(f"❌ Error creating configuration: {e}")
            return False
    else:
        print(f"✅ Configuration already exists at {config_file}")
    
    return True

def main():
    """Main setup function"""
    print("AirTag Detector Setup")
    print("=" * 40)
    
    # Check system requirements
    if not check_system_requirements():
        sys.exit(1)
    
    # Ask user what to install
    print("\nSetup options:")
    print("1. Full installation (system dependencies + service)")
    print("2. Service only (requires root)")
    print("3. Configuration only")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            success = True
            success &= install_system_dependencies()
            success &= create_config_directory()
            success &= install_systemd_service()
            
            if success:
                print("\n✅ Full installation completed successfully!")
                print("\nNext steps:")
                print("1. Configure HomeKit: airtag-homekit-setup")
                print("2. Test Bluetooth: airtag-test")
                print("3. Start service: sudo systemctl start airtag-detector.service")
            else:
                print("\n❌ Installation completed with errors")
                sys.exit(1)
            break
            
        elif choice == "2":
            success = True
            success &= install_systemd_service()
            
            if success:
                print("\n✅ Service installation completed!")
            else:
                print("\n❌ Service installation failed")
                sys.exit(1)
            break
            
        elif choice == "3":
            if create_config_directory():
                print("\n✅ Configuration setup completed!")
                print("\nNext steps:")
                print("1. Edit configuration: ~/.config/airtag-detector/config.py")
                print("2. Configure HomeKit: airtag-homekit-setup")
            else:
                print("\n❌ Configuration setup failed")
                sys.exit(1)
            break
            
        elif choice == "4":
            print("Setup cancelled.")
            break
            
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
