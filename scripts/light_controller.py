"""Core Elgato Key Light API client."""

import requests
import json
import logging
from typing import Dict, Optional, Tuple
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LightController:
    """Control Elgato Key Lights via REST API."""

    def __init__(self, light_ip: str, port: int = 9123):
        """
        Initialize the light controller.

        Args:
            light_ip: IP address of the Elgato Key Light
            port: API port (default 9123)
        """
        self.light_ip = light_ip
        self.port = port
        self.base_url = f"http://{light_ip}:{port}"
        self.timeout = 5

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Dict:
        """
        Make HTTP request to the light.

        Args:
            method: HTTP method (GET, PUT, POST)
            endpoint: API endpoint (e.g., '/elgato/lights')
            data: Optional request body

        Returns:
            Response JSON as dict

        Raises:
            requests.RequestException: If request fails
        """
        url = urljoin(self.base_url, endpoint)
        try:
            if method == "GET":
                response = requests.get(url, timeout=self.timeout)
            elif method == "PUT":
                response = requests.put(
                    url, json=data, timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            logger.error(
                f"Failed to connect to {self.light_ip}:{self.port} - {e}"
            )
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout for {self.light_ip}:{self.port}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e.response.status_code}")
            raise

    def get_status(self) -> Dict:
        """
        Get the current status of the light.

        Returns:
            Dict with light status including on/off, brightness, color temp, etc.
        """
        response = self._make_request("GET", "/elgato/lights")
        return response.get("lights", [{}])[0] if response.get("lights") else {}

    def set_power(self, on: bool) -> bool:
        """
        Turn light on or off.

        Args:
            on: True to turn on, False to turn off

        Returns:
            True if successful
        """
        self._make_request(
            "PUT",
            "/elgato/lights",
            {"lights": [{"on": 1 if on else 0}]}
        )
        return True

    def turn_on(self) -> bool:
        """Turn the light on."""
        return self.set_power(True)

    def turn_off(self) -> bool:
        """Turn the light off."""
        return self.set_power(False)

    def toggle(self) -> bool:
        """
        Toggle light on/off.

        Returns:
            True if successful
        """
        status = self.get_status()
        current_state = status.get("on", 0)
        return self.set_power(current_state == 0)

    def set_brightness(self, brightness: int) -> bool:
        """
        Set light brightness.

        Args:
            brightness: Brightness level 0-100

        Returns:
            True if successful

        Raises:
            ValueError: If brightness is not 0-100
        """
        if not 0 <= brightness <= 100:
            raise ValueError("Brightness must be between 0 and 100")

        self._make_request(
            "PUT",
            "/elgato/lights",
            {"lights": [{"brightness": brightness}]}
        )
        return True

    def set_color_temperature(self, kelvin: int) -> bool:
        """
        Set color temperature.

        Args:
            kelvin: Color temperature in Kelvin (2700-7000K)

        Returns:
            True if successful

        Raises:
            ValueError: If kelvin is outside valid range
        """
        if not 2700 <= kelvin <= 7000:
            raise ValueError("Color temperature must be between 2700K and 7000K")

        self._make_request(
            "PUT",
            "/elgato/lights",
            {"lights": [{"temperature": kelvin}]}
        )
        return True

    def set_color(self, red: int, green: int, blue: int) -> bool:
        """
        Set light color using RGB values.

        Args:
            red: Red value 0-255
            green: Green value 0-255
            blue: Blue value 0-255

        Returns:
            True if successful

        Raises:
            ValueError: If any RGB value is outside 0-255
        """
        for value, name in [(red, "red"), (green, "green"), (blue, "blue")]:
            if not 0 <= value <= 255:
                raise ValueError(f"{name} must be between 0 and 255")

        hue = self._rgb_to_hue(red, green, blue)
        self._make_request(
            "PUT",
            "/elgato/lights",
            {"lights": [{"hue": hue}]}
        )
        return True

    @staticmethod
    def _rgb_to_hue(red: int, green: int, blue: int) -> int:
        """
        Convert RGB to Hue value (0-360 mapped to 0-360 range used by API).

        Args:
            red: Red value 0-255
            green: Green value 0-255
            blue: Blue value 0-255

        Returns:
            Hue value 0-360
        """
        r = red / 255.0
        g = green / 255.0
        b = blue / 255.0

        max_val = max(r, g, b)
        min_val = min(r, g, b)
        delta = max_val - min_val

        if delta == 0:
            hue = 0
        elif max_val == r:
            hue = 60 * (((g - b) / delta) % 6)
        elif max_val == g:
            hue = 60 * (((b - r) / delta) + 2)
        else:
            hue = 60 * (((r - g) / delta) + 4)

        return int(hue) % 360

    def get_info(self) -> Dict:
        """
        Get light information (name, model, firmware, etc.).

        Returns:
            Dict with light information
        """
        return self._make_request("GET", "/elgato/accessory-info")
