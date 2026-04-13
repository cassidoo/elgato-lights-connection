#!/usr/bin/env python3
"""Interactive setup wizard for Elgato Key Lights."""

import sys
import json
import os
from pathlib import Path
from scripts.light_controller import LightController

# Available scripts for batch file generation (script_name, description)
AVAILABLE_SCRIPTS = [
    ("toggle_light", "Toggle light on/off"),
    ("turn_on_light", "Turn light on"),
    ("turn_off_light", "Turn light off"),
    ("set_brightness", "Set brightness (requires brightness argument 0-100)"),
    ("set_color_temp", "Set color temperature (requires kelvin argument 2700-7000)"),
    ("set_color", "Set RGB color (requires R G B arguments 0-255 each)"),
]


def generate_batch_files(light_name, ip_address, port, selected_scripts):
    """Generate Windows batch wrapper files for selected scripts.
    
    Args:
        light_name: Friendly name of the light
        ip_address: IP address of the light
        port: API port of the light
        selected_scripts: List of script names to generate batch files for
    
    Returns:
        List of paths to generated batch files
    """
    batch_dir = Path("batch")
    batch_dir.mkdir(exist_ok=True)
    
    # Get the absolute path to the project directory
    project_path = Path(__file__).parent.absolute()
    
    # Sanitize light name for file naming
    safe_light_name = light_name.lower().replace(' ', '_').replace('-', '_')
    
    generated_files = []
    
    for script_name in selected_scripts:
        batch_file = batch_dir / f"{safe_light_name}_{script_name}.bat"
        
        # Determine the command based on script type
        if script_name == "set_brightness":
            # Brightness needs a parameter - use 75% as default example
            command = f'python "{project_path}\\{script_name}.py" {ip_address} 75'
        elif script_name == "set_color_temp":
            # Color temp needs a parameter - use 4000K as default example
            command = f'python "{project_path}\\{script_name}.py" {ip_address} 4000'
        elif script_name == "set_color":
            # Color needs RGB parameters - use white (255 255 255) as default example
            command = f'python "{project_path}\\{script_name}.py" {ip_address} 255 255 255'
        else:
            # Simple scripts that just need IP address
            command = f'python "{project_path}\\{script_name}.py" {ip_address}'
        
        # Add port if not default
        if port != 9123:
            command += f' --port {port}'
        
        # Create batch file content
        batch_content = f"""@echo off
REM Batch wrapper for {script_name}.py
REM Light: {light_name}
REM IP: {ip_address}
REM Port: {port}

{command}
"""
        
        with open(batch_file, 'w') as f:
            f.write(batch_content)
        
        generated_files.append(batch_file)
        
        # Create VBScript wrapper that runs the batch file silently
        vbs_file = batch_dir / f"{safe_light_name}_{script_name}.vbs"
        abs_batch_path = batch_file.resolve()
        vbs_content = f'CreateObject("WScript.Shell").Run Chr(34) & "{abs_batch_path}" & Chr(34), 0, False\n'
        
        with open(vbs_file, 'w') as f:
            f.write(vbs_content)
        
        generated_files.append(vbs_file)
    
    return generated_files


def prompt_batch_file_generation(light_name, ip_address, port):
    """Prompt user to select which batch files to generate.
    
    Returns:
        List of script names selected by user, or empty list if declined
    """
    print()
    generate_batch = input(
        "Would you like to generate Windows batch wrapper files for this light? (y/n): "
    ).strip().lower()
    
    if generate_batch != 'y':
        return []
    
    print()
    print("Available scripts for batch file generation:")
    print()
    
    # Display available scripts with numbering
    for i, (script_name, description) in enumerate(AVAILABLE_SCRIPTS, 1):
        print(f"  {i}. {script_name:20} - {description}")
    
    print()
    selected = input(
        "Enter script numbers to generate (comma-separated, e.g., '1,2,3'): "
    ).strip()
    
    if not selected:
        return []
    
    selected_scripts = []
    try:
        indices = [int(x.strip()) for x in selected.split(',')]
        for idx in indices:
            if 1 <= idx <= len(AVAILABLE_SCRIPTS):
                selected_scripts.append(AVAILABLE_SCRIPTS[idx - 1][0])
            else:
                print(f"Warning: Invalid selection {idx}, skipping")
    except ValueError:
        print("Invalid input format. Skipping batch file generation.")
        return []
    
    return selected_scripts


def main():
    print("=" * 60)
    print("Elgato Key Light Setup Wizard")
    print("=" * 60)
    print()

    ip_address = input("Enter the IP address of your Elgato Key Light: ").strip()
    if not ip_address:
        print("Error: IP address is required", file=sys.stderr)
        return 1

    port = input("Enter the API port (default 9123): ").strip()
    port = int(port) if port else 9123

    print("\nTesting connection...")
    try:
        controller = LightController(ip_address, port)
        info = controller.get_info()
        status = controller.get_status()
        print(f"✓ Successfully connected!")
        print(f"  Product Name: {info.get('displayName', 'Unknown')}")
        print(f"  Firmware: {info.get('firmwareVersion', 'Unknown')}")
        print(f"  Current State: {'ON' if status.get('on') else 'OFF'}")
    except Exception as e:
        print(f"✗ Failed to connect: {e}", file=sys.stderr)
        print("Please verify the IP address and network connection", file=sys.stderr)
        return 1

    print()
    light_name = input(
        "Enter a friendly name for this light (e.g., 'Desk Light'): "
    ).strip()
    if not light_name:
        light_name = "Elgato Light"

    light_desc = input(
        "Enter a description for this light (optional): "
    ).strip()

    light_config = {
        "name": light_name,
        "ip_address": ip_address,
        "port": port,
        "description": light_desc
    }

    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)

    config_file = config_dir / f"{light_name.lower().replace(' ', '_')}.json"

    print()
    print(f"Configuration to be saved:")
    print(json.dumps(light_config, indent=2))
    print()

    confirm = input(f"Save to {config_file}? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Setup cancelled")
        return 0

    with open(config_file, 'w') as f:
        json.dump(light_config, f, indent=2)

    print(f"✓ Configuration saved to {config_file}")
    print()

    # Prompt for batch file generation (Windows only)
    selected_scripts = prompt_batch_file_generation(light_name, ip_address, port)
    
    if selected_scripts:
        print()
        print("Generating batch files...")
        generated_files = generate_batch_files(light_name, ip_address, port, selected_scripts)
        bat_files = [f for f in generated_files if f.suffix == '.bat']
        vbs_files = [f for f in generated_files if f.suffix == '.vbs']
        print(f"✓ Generated {len(bat_files)} .bat file(s) and {len(vbs_files)} .vbs file(s) in 'batch/' directory:")
        for generated_file in generated_files:
            print(f"  - {generated_file}")
        print()
        print("Next steps:")
        print("1. Review the generated .bat and .vbs files in the 'batch/' folder")
        print("2. Update any default parameters in the batch files as needed:")
        print("   - set_brightness.bat: Change '75' to desired brightness (0-100)")
        print("   - set_color_temp.bat: Change '4000' to desired temperature (2700-7000K)")
        print("   - set_color.bat: Change '255 255 255' to desired RGB values (0-255 each)")
        print("3. In Logi Options+, bind the .vbs files to MX Console buttons")
        print("   (Use .vbs files instead of .bat files to run silently without a console window)")
    else:
        print("Next steps:")
        print("1. Create batch file wrappers manually (see README.md for examples)")
        print("2. Test scripts manually with: python toggle_light.py {ip_address}")
        print("3. Bind scripts to MX Console buttons in Logitech Options")

    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
