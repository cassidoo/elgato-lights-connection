#!/usr/bin/env python3
"""Interactive setup wizard for Elgato Key Lights."""

import sys
import json
import os
from pathlib import Path
from scripts.light_controller import LightController


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
    print("Next steps:")
    print(f"1. Test the light with: python toggle_light.py {ip_address}")
    print(f"2. Bind scripts to MX Console buttons (see README.md)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
