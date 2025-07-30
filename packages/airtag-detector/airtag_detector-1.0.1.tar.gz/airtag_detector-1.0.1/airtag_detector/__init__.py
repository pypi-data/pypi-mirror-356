"""
AirTag Detector Package

A Python package for detecting Apple AirTags on Raspberry Pi with HomeKit integration.
"""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "1.0.1"

__author__ = "Nicholas Anderson"
__email__ = "contras-kite9t@icloud.com"
__description__ = "Apple AirTag detector for Raspberry Pi with HomeKit integration"

from .detector import AirTagDetector
from .homekit_controller import HomeKitController

__all__ = ["AirTagDetector", "HomeKitController", "__version__"]
