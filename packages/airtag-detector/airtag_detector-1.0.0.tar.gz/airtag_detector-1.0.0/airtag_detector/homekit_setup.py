#!/usr/bin/env python3
"""
HomeKit Setup Script for AirTag Detector
This script helps you set up HomeKit integration
"""

import asyncio
import json
import sys
import os

try:
    from aiohomekit import Controller
    HOMEKIT_AVAILABLE = True
except ImportError:
    HOMEKIT_AVAILABLE = False

try:
    import requests
except ImportError:
    print("Error: requests library not found. Please install it with: pip install requests")
    sys.exit(1)

def setup_home_assistant():
    """Setup Home Assistant integration"""
    print("\n=== Home Assistant Setup ===")
    print("This is the recommended method for HomeKit integration.")
    print()
    
    print("1. In Home Assistant, go to your Profile (bottom left)")
    print("2. Scroll down to 'Long-Lived Access Tokens'")
    print("3. Click 'Create Token' and give it a name like 'AirTag Detector'")
    print("4. Copy the token and paste it here")
    print()
    
    url = input("Enter your Home Assistant URL (e.g., http://192.168.1.50:8123): ").strip()
    token = input("Enter your long-lived access token: ").strip()
    entity_id = input("Enter the entity ID of your smart plug (e.g., switch.smart_plug): ").strip()
    
    if not url or not token or not entity_id:
        print("Error: All fields are required")
        return False
    
    # Test the connection
    print("\nTesting connection...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{url}/api/", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✓ Connection successful!")
            
            # Test entity access
            state_response = requests.get(f"{url}/api/states/{entity_id}", headers=headers, timeout=5)
            if state_response.status_code == 200:
                state_data = state_response.json()
                current_state = state_data.get('state', 'unknown')
                print(f"✓ Found device '{entity_id}' with current state: {current_state}")
                
                # Update config file
                update_config_file(url, token, entity_id)
                print("✓ Configuration saved to config.py")
                return True
            else:
                print(f"✗ Entity '{entity_id}' not found or not accessible")
                return False
        else:
            print(f"✗ Connection failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def update_config_file(ha_url, ha_token, entity_id):
    """Update the config file with Home Assistant settings"""
    config_path = "/home/ubuntu/dogpi/config.py"
    
    try:
        # Read current config
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Update values
        content = content.replace('HOME_ASSISTANT_URL = ""', f'HOME_ASSISTANT_URL = "{ha_url}"')
        content = content.replace('HOME_ASSISTANT_TOKEN = ""', f'HOME_ASSISTANT_TOKEN = "{ha_token}"')
        content = content.replace('HOME_ASSISTANT_ENTITY_ID = "switch.smart_plug"', f'HOME_ASSISTANT_ENTITY_ID = "{entity_id}"')
        
        # Write back
        with open(config_path, 'w') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error updating config file: {e}")

async def setup_direct_homekit():
    """Setup direct HomeKit integration (advanced)"""
    print("\n=== Direct HomeKit Setup ===")
    print("This method connects directly to HomeKit devices.")
    print("Note: This is more complex and may require additional setup.")
    print()
    
    if not HOMEKIT_AVAILABLE:
        print("Error: aiohomekit library not installed.")
        print("Install with: pip install aiohomekit")
        return False
    
    print("Direct HomeKit setup is not fully implemented in this version.")
    print("Please use Home Assistant integration instead.")
    return False

def test_current_config():
    """Test the current configuration"""
    print("\n=== Testing Current Configuration ===")
    
    try:
        # Import current config
        sys.path.insert(0, '/home/ubuntu/dogpi')
        from config import HOME_ASSISTANT_URL, HOME_ASSISTANT_TOKEN, HOME_ASSISTANT_ENTITY_ID
        
        if not HOME_ASSISTANT_TOKEN or not HOME_ASSISTANT_URL:
            print("No Home Assistant configuration found.")
            return False
        
        print(f"Testing connection to: {HOME_ASSISTANT_URL}")
        print(f"Entity ID: {HOME_ASSISTANT_ENTITY_ID}")
        
        headers = {
            "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{HOME_ASSISTANT_URL}/api/states/{HOME_ASSISTANT_ENTITY_ID}", 
                              headers=headers, timeout=5)
        
        if response.status_code == 200:
            state_data = response.json()
            current_state = state_data.get('state', 'unknown')
            print(f"✓ Configuration is working! Current device state: {current_state}")
            return True
        else:
            print(f"✗ Configuration test failed: HTTP {response.status_code}")
            return False
            
    except ImportError:
        print("Configuration file not found or invalid.")
        return False
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("HomeKit Setup for AirTag Detector")
    print("=" * 40)
    print()
    print("Choose an option:")
    print("1. Setup Home Assistant integration (recommended)")
    print("2. Setup direct HomeKit integration (advanced)")
    print("3. Test current configuration")
    print("4. Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            if setup_home_assistant():
                print("\n✓ Home Assistant setup complete!")
                print("You can now run the AirTag detector.")
            break
        elif choice == "2":
            asyncio.run(setup_direct_homekit())
            break
        elif choice == "3":
            test_current_config()
            break
        elif choice == "4":
            print("Setup cancelled.")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup cancelled by user.")
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)
