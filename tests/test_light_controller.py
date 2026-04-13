"""Unit tests for Elgato Key Light controller."""

import unittest
from unittest.mock import patch, MagicMock
from scripts.light_controller import LightController


class TestLightController(unittest.TestCase):
    """Test cases for LightController."""

    def setUp(self):
        """Set up test fixtures."""
        self.controller = LightController("192.168.1.100", 9123)

    @patch('scripts.light_controller.requests.get')
    def test_get_status(self, mock_get):
        """Test getting light status."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "lights": [
                {
                    "on": 1,
                    "brightness": 50,
                    "temperature": 4000
                }
            ]
        }
        mock_get.return_value = mock_response

        status = self.controller.get_status()
        self.assertEqual(status["on"], 1)
        self.assertEqual(status["brightness"], 50)
        self.assertEqual(status["temperature"], 4000)

    @patch('scripts.light_controller.requests.put')
    def test_turn_on(self, mock_put):
        """Test turning light on."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_put.return_value = mock_response

        result = self.controller.turn_on()
        self.assertTrue(result)
        mock_put.assert_called_once()

    @patch('scripts.light_controller.requests.put')
    def test_turn_off(self, mock_put):
        """Test turning light off."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_put.return_value = mock_response

        result = self.controller.turn_off()
        self.assertTrue(result)
        mock_put.assert_called_once()

    def test_set_brightness_valid(self):
        """Test setting brightness with valid value."""
        with patch('scripts.light_controller.requests.put') as mock_put:
            mock_response = MagicMock()
            mock_response.json.return_value = {}
            mock_put.return_value = mock_response

            result = self.controller.set_brightness(75)
            self.assertTrue(result)

    def test_set_brightness_invalid_low(self):
        """Test setting brightness below 0."""
        with self.assertRaises(ValueError):
            self.controller.set_brightness(-1)

    def test_set_brightness_invalid_high(self):
        """Test setting brightness above 100."""
        with self.assertRaises(ValueError):
            self.controller.set_brightness(101)

    def test_set_color_temperature_valid(self):
        """Test setting color temperature with valid value."""
        with patch('scripts.light_controller.requests.put') as mock_put:
            mock_response = MagicMock()
            mock_response.json.return_value = {}
            mock_put.return_value = mock_response

            result = self.controller.set_color_temperature(4000)
            self.assertTrue(result)

    def test_set_color_temperature_invalid_low(self):
        """Test setting color temperature below 2700K."""
        with self.assertRaises(ValueError):
            self.controller.set_color_temperature(2600)

    def test_set_color_temperature_invalid_high(self):
        """Test setting color temperature above 7000K."""
        with self.assertRaises(ValueError):
            self.controller.set_color_temperature(7100)

    def test_rgb_to_hue_conversion(self):
        """Test RGB to Hue conversion."""
        hue = LightController._rgb_to_hue(255, 0, 0)
        self.assertEqual(hue, 0)

        hue = LightController._rgb_to_hue(0, 255, 0)
        self.assertEqual(hue, 120)

        hue = LightController._rgb_to_hue(0, 0, 255)
        self.assertEqual(hue, 240)

        hue = LightController._rgb_to_hue(255, 255, 255)
        self.assertEqual(hue, 0)

    def test_set_color_valid(self):
        """Test setting color with valid RGB values."""
        with patch('scripts.light_controller.requests.put') as mock_put:
            mock_response = MagicMock()
            mock_response.json.return_value = {}
            mock_put.return_value = mock_response

            result = self.controller.set_color(255, 128, 0)
            self.assertTrue(result)

    def test_set_color_invalid_red(self):
        """Test setting color with invalid red value."""
        with self.assertRaises(ValueError):
            self.controller.set_color(256, 0, 0)

    def test_set_color_invalid_green(self):
        """Test setting color with invalid green value."""
        with self.assertRaises(ValueError):
            self.controller.set_color(0, -1, 0)

    def test_set_color_invalid_blue(self):
        """Test setting color with invalid blue value."""
        with self.assertRaises(ValueError):
            self.controller.set_color(0, 0, 300)

    @patch('scripts.light_controller.requests.get')
    def test_connection_error(self, mock_get):
        """Test handling of connection errors."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.controller.get_status()

    @patch('scripts.light_controller.requests.get')
    def test_timeout_error(self, mock_get):
        """Test handling of timeout errors."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        with self.assertRaises(requests.exceptions.Timeout):
            self.controller.get_status()


if __name__ == "__main__":
    unittest.main()
