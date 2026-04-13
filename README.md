# Elgato Key Light MX Creative Console Control

Control your Elgato Key Lights using buttons on the Logitech MX Creative Console. This system provides Python scripts that can be bound to console buttons for quick light control.

## Features

- **Toggle** lights on/off with a single button
- **Control brightness** (0-100%)
- **Adjust color temperature** (2700K-7000K for warm to cool white)
- **Set custom colors** using RGB values
- **Multiple light support** - control different lights with different buttons
- **Easy setup wizard** - interactive configuration for each light

## Requirements

- Python 3.6+
- Elgato Key Light(s) with API enabled (most models support this)
- Network connectivity between your computer and lights
- Logitech MX Creative Console (for button binding)
- Light IP addresses or network names

## Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd elgato-lights-mx-connection
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Find Your Light IP Addresses

You can find your Elgato Key Light IP address using several methods:

**Option A: Via Elgato Control Center (Easiest)**
1. Install the Elgato Control Center app
2. Open it and select your light
3. Go to Settings → Network
4. Note the IP address shown

**Option B: Via Router Admin Panel**
1. Log into your router's admin panel
2. Check the connected devices list
3. Look for "Elgato" or check device hostnames

**Option C: Using Network Discovery**
```bash
# On Windows (using PowerShell)
Get-NetNeighbor | findstr "Elgato"

# On Mac/Linux
arp -a | grep -i elgato
```

**Option D: Scan your network**
```bash
# Using nmap (if installed)
nmap -p 9123 192.168.1.0/24
```

### 4. Set Up Each Light

For each Elgato Key Light you want to control, run the setup wizard:

```bash
python setup_light.py
```

The wizard will:
1. Ask for your light's IP address
2. Verify the connection
3. Let you name the light
4. Add a description
5. Save the configuration

This creates a JSON config file in the `config/` directory.

## Usage

### Manual Script Testing

Before binding to buttons, test the scripts directly:

**Toggle a light:**
```bash
python toggle_light.py 192.168.1.100
```

**Turn on a light:**
```bash
python turn_on_light.py 192.168.1.100
```

**Turn off a light:**
```bash
python turn_off_light.py 192.168.1.100
```

**Set brightness to 75%:**
```bash
python set_brightness.py 192.168.1.100 75
```

**Set color temperature to 4000K (neutral white):**
```bash
python set_color_temp.py 192.168.1.100 4000
```

**Set color to green (0, 255, 0):**
```bash
python set_color.py 192.168.1.100 0 255 0
```

### Script Parameters

All scripts support:
- `--port <PORT>` - Specify non-standard API port (default: 9123)

Example with custom port:
```bash
python toggle_light.py 192.168.1.100 --port 9124
```

## Binding to MX Creative Console

### Setting Up Buttons

1. **Download and Install MX Master 3S/3/2S Software**
   - Download from Logitech's website
   - Install the control application

2. **Launch the Settings Application**
   - Find "Logitech Options" or "Logitech G Hub" in your applications
   - Open it and navigate to the MX Creative Console settings

3. **Configure Button Actions**
   - Select an available button you want to customize
   - Choose "Application/System" or "Custom Application" action
   - Set it to run a command

4. **Create a Batch Wrapper (Windows)**
   Since the scripts are Python, you'll need a `.bat` file wrapper:

   Create a file named `toggle_desk_light.bat`:
   ```batch
   @echo off
   python C:\path\to\elgato-lights-mx-connection\toggle_light.py 192.168.1.100
   pause
   ```

   Replace:
   - `C:\path\to\elgato-lights-mx-connection\` with your actual installation path
   - `192.168.1.100` with your light's IP address

   For other actions, create similar batch files for:
   - `turn_on_desk_light.bat`
   - `turn_off_desk_light.bat`
   - `brightness_75.bat` (with `set_brightness.py 192.168.1.100 75`)
   - etc.

5. **Bind Batch Files to Console Buttons**
   - In Logitech Options, point the button to your `.bat` file
   - Test the button to ensure it works
   - Adjust if needed

### Example Button Configuration

| Button | Action | Batch File |
|--------|--------|-----------|
| Button 1 | Toggle Desk Light | `toggle_desk_light.bat` |
| Button 2 | Toggle Background Light | `toggle_bg_light.bat` |
| Button 3 | Set Brightness 100% | `brightness_100.bat` |
| Button 4 | Set Warm (3000K) | `color_warm.bat` |

### macOS/Linux Alternative

Instead of `.bat` files, create shell scripts:

`toggle_desk_light.sh`:
```bash
#!/bin/bash
python /path/to/elgato-lights-mx-connection/toggle_light.py 192.168.1.100
```

Make it executable:
```bash
chmod +x toggle_desk_light.sh
```

Then bind to the button in Logitech Options.

## Configuration Files

Light configurations are stored as JSON in the `config/` directory.

### Example Configuration
```json
{
  "name": "Desk Light",
  "ip_address": "192.168.1.100",
  "port": 9123,
  "description": "Main desk key light for streaming/video"
}
```

### Manual Configuration

If you prefer to create configs manually instead of using the wizard:

1. Copy `config/lights_example.json` to `config/my_light.json`
2. Edit with your light details:
   - `name`: Friendly name (e.g., "Studio Light")
   - `ip_address`: Your light's IP
   - `port`: Usually 9123 (change only if customized)
   - `description`: Optional notes about this light

## Troubleshooting

### Script Fails with "Connection refused"
- **Verify IP address** - Confirm the light's IP hasn't changed
- **Check network** - Ensure light and computer are on the same network
- **Firewall** - Make sure port 9123 isn't blocked
- **Light offline** - Restart the light (power cycle it)

### MX Button Doesn't Trigger Script
- **Test manually first** - Run the `.bat` file directly to confirm it works
- **Verify path** - Double-check the full path in the batch file
- **Run as administrator** - Some button configurations require elevated privileges
- **Restart application** - Restart Logitech Options after changes
- **Error output** - Add `pause` to batch files to see error messages

### Light Responds Slowly or Not At All
- **Network lag** - Check your WiFi connection strength
- **Light firmware** - Update light firmware via Elgato Control Center
- **Port conflict** - Confirm nothing else is using port 9123
- **API disabled** - Some lights can disable the API; check light settings

### "ModuleNotFoundError: No module named 'requests'"
- Install dependencies: `pip install -r requirements.txt`
- Verify correct Python version: `python --version` (should be 3.6+)

## Testing

Run the included unit tests:

```bash
python -m unittest discover tests
```

Or run a specific test:

```bash
python -m unittest tests.test_light_controller.TestLightController.test_get_status
```

## Color Reference

### Common Color Temperatures
- **2700K** - Warm white (incandescent bulb color)
- **3000K** - Soft white (most comfortable for indoors)
- **4000K** - Neutral white (balanced, natural)
- **5000K** - Cool white (bright, office-like)
- **6500K** - Daylight (bright, natural sunlight)
- **7000K** - Cool daylight (very bright, blue-ish)

### Common RGB Colors
| Color | R | G | B | Hue |
|-------|---|---|---|-----|
| Red | 255 | 0 | 0 | 0° |
| Orange | 255 | 165 | 0 | 39° |
| Yellow | 255 | 255 | 0 | 60° |
| Green | 0 | 255 | 0 | 120° |
| Cyan | 0 | 255 | 255 | 180° |
| Blue | 0 | 0 | 255 | 240° |
| Magenta | 255 | 0 | 255 | 300° |
| White | 255 | 255 | 255 | 0° |

## Advanced: Custom Scripts

The `LightController` class can be imported for custom Python scripts:

```python
from scripts.light_controller import LightController

# Create a controller for a light
light = LightController("192.168.1.100")

# Get current status
status = light.get_status()
print(f"Light is {'on' if status['on'] else 'off'}")
print(f"Brightness: {status['brightness']}%")

# Control the light
light.turn_on()
light.set_brightness(80)
light.set_color_temperature(4000)
```

## API Reference

### LightController Methods

**`__init__(light_ip, port=9123)`**
- Initialize connection to a light

**`get_status()`**
- Returns dict with current light state

**`get_info()`**
- Returns dict with light information (name, firmware, model)

**`turn_on()`**
- Turn light on

**`turn_off()`**
- Turn light off

**`toggle()`**
- Toggle between on and off

**`set_brightness(brightness: int)`**
- Set brightness 0-100 (raises ValueError if out of range)

**`set_color_temperature(kelvin: int)`**
- Set color temperature 2700-7000K

**`set_color(red: int, green: int, blue: int)`**
- Set color using RGB (0-255 each)

## Project Structure

```
elgato-lights-mx-connection/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── toggle_light.py                    # Toggle on/off script
├── turn_on_light.py                   # Turn on script
├── turn_off_light.py                  # Turn off script
├── set_brightness.py                  # Set brightness script
├── set_color_temp.py                  # Set color temperature script
├── set_color.py                       # Set RGB color script
├── setup_light.py                     # Interactive light setup wizard
├── config/
│   └── lights_example.json            # Example configuration
├── scripts/
│   ├── __init__.py
│   └── light_controller.py            # Core API client
└── tests/
    ├── __init__.py
    └── test_light_controller.py       # Unit tests
```

## Limitations

- The light must be on the same network as your computer
- The light API may not be available on very old Elgato models
- Some color modes may not be available on all light models
- Windows batch wrapper files need to be in a known location

## Contributing

Contributions are welcome! Feel free to:
- Report issues
- Suggest improvements
- Add support for new light models
- Improve the documentation

## License

This project is provided as-is for controlling Elgato Key Lights.

## Support

For issues:
1. Check the Troubleshooting section above
2. Verify your light IP and network connection
3. Test scripts manually before binding to buttons
4. Check light firmware is up to date

## Resources

- [Elgato Key Light Official Site](https://www.elgato.com/en/gaming/key-light)
- [Logitech MX Creative Console](https://www.logitech.com/en-us/products/mice/mx-creative-console.html)
- [Elgato API Documentation](https://developer.elgato.com/documentation/master-control/about/)
