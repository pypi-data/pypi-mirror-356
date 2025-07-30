#!/usr/bin/env python3
"""
HomeKit Controller Module for AirTag Detector
Controls HomeKit devices via Home Assistant or direct HomeKit
"""

import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Optional

try:
    import requests
except ImportError:
    requests = None

# Try to import HomeKit library (optional)
try:
    from aiohomekit import Controller, Pairing
    HOMEKIT_AVAILABLE = True
except ImportError:
    HOMEKIT_AVAILABLE = False

logger = logging.getLogger(__name__)


class HomeKitController:
    """Controls HomeKit devices via Home Assistant or direct HomeKit"""
    
    def __init__(self, config=None):
        self.plug_state = None  # Track current plug state
        self.pairing = None
        self.controller = None
        
        # Load configuration
        if config:
            self.home_assistant_url = getattr(config, 'HOME_ASSISTANT_URL', '')
            self.home_assistant_token = getattr(config, 'HOME_ASSISTANT_TOKEN', '')
            self.home_assistant_entity_id = getattr(config, 'HOME_ASSISTANT_ENTITY_ID', 'switch.smart_plug')
            self.homekit_pairing_file = getattr(config, 'HOMEKIT_PAIRING_DATA_FILE', '/tmp/homekit_pairing.json')
            self.debug_homekit = getattr(config, 'DEBUG_HOMEKIT', True)
        else:
            # Default config
            self.home_assistant_url = ''
            self.home_assistant_token = ''
            self.home_assistant_entity_id = 'switch.smart_plug'
            self.homekit_pairing_file = '/tmp/homekit_pairing.json'
            self.debug_homekit = True
            
        self.use_home_assistant = bool(self.home_assistant_token and self.home_assistant_url)
        
        if self.debug_homekit:
            logger.info(f"HomeKit controller initialized. Using Home Assistant: {self.use_home_assistant}")
    
    async def initialize(self):
        """Initialize HomeKit connection"""
        if self.use_home_assistant:
            await self._test_home_assistant_connection()
        elif HOMEKIT_AVAILABLE:
            await self._initialize_homekit_direct()
        else:
            logger.warning("No HomeKit control method available")
            
    async def _test_home_assistant_connection(self):
        """Test Home Assistant connection"""
        if not requests:
            logger.error("requests library not available for Home Assistant integration")
            return
            
        try:
            headers = {
                "Authorization": f"Bearer {self.home_assistant_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{self.home_assistant_url}/api/", headers=headers, timeout=5)
            if response.status_code == 200:
                logger.info("✓ Home Assistant connection successful")
                
                # Get current state
                state_response = requests.get(
                    f"{self.home_assistant_url}/api/states/{self.home_assistant_entity_id}",
                    headers=headers,
                    timeout=5
                )
                if state_response.status_code == 200:
                    state_data = state_response.json()
                    self.plug_state = state_data.get('state')
                    logger.info(f"Current plug state: {self.plug_state}")
                else:
                    logger.warning(f"Could not get current plug state: {state_response.status_code}")
            else:
                logger.error(f"Home Assistant connection failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Error testing Home Assistant connection: {e}")
    
    async def _initialize_homekit_direct(self):
        """Initialize direct HomeKit connection"""
        try:
            self.controller = Controller()
            
            # Try to load existing pairing
            if os.path.exists(self.homekit_pairing_file):
                with open(self.homekit_pairing_file, 'r') as f:
                    pairing_data = json.load(f)
                    # Restore pairing (implementation depends on aiohomekit version)
                    logger.info("Loaded existing HomeKit pairing")
            else:
                logger.warning("No existing HomeKit pairing found. Manual pairing required.")
                logger.info("Run the setup script to pair with HomeKit")
                
        except Exception as e:
            logger.error(f"Error initializing direct HomeKit: {e}")
    
    async def turn_off_plug(self):
        """Turn off the smart plug"""
        if self.plug_state == 'off':
            logger.debug("Plug already off")
            return True
            
        try:
            if self.use_home_assistant:
                success = await self._home_assistant_control('turn_off')
            else:
                success = await self._homekit_direct_control(False)
                
            if success:
                self.plug_state = 'off'
                logger.info("🔌 Smart plug turned OFF (AirTag detected)")
            return success
        except Exception as e:
            logger.error(f"Error turning off plug: {e}")
            return False
    
    async def turn_on_plug(self):
        """Turn on the smart plug"""
        if self.plug_state == 'on':
            logger.debug("Plug already on")
            return True
            
        try:
            if self.use_home_assistant:
                success = await self._home_assistant_control('turn_on')
            else:
                success = await self._homekit_direct_control(True)
                
            if success:
                self.plug_state = 'on'
                logger.info("🔌 Smart plug turned ON (AirTag no longer detected)")
            return success
        except Exception as e:
            logger.error(f"Error turning on plug: {e}")
            return False
    
    async def _home_assistant_control(self, action):
        """Control device via Home Assistant"""
        if not requests:
            logger.error("requests library not available")
            return False
            
        try:
            headers = {
                "Authorization": f"Bearer {self.home_assistant_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "entity_id": self.home_assistant_entity_id
            }
            
            response = requests.post(
                f"{self.home_assistant_url}/api/services/switch/{action}",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.debug(f"Home Assistant {action} successful")
                return True
            else:
                logger.error(f"Home Assistant {action} failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error controlling via Home Assistant: {e}")
            return False
    
    async def _homekit_direct_control(self, turn_on: bool):
        """Control device via direct HomeKit"""
        try:
            if not self.pairing:
                logger.error("No HomeKit pairing available")
                return False
                
            # Implementation depends on specific HomeKit setup
            # This is a placeholder - actual implementation varies by device
            logger.warning("Direct HomeKit control not fully implemented")
            return False
            
        except Exception as e:
            logger.error(f"Error with direct HomeKit control: {e}")
            return False
