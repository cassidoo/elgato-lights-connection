#!/usr/bin/env python3
"""Toggle Elgato Key Light on/off."""

import sys
import argparse
from scripts.light_controller import LightController


def main():
    parser = argparse.ArgumentParser(
        description="Toggle Elgato Key Light on/off"
    )
    parser.add_argument("ip", help="IP address of the light")
    parser.add_argument(
        "--port", type=int, default=9123, help="API port (default: 9123)"
    )

    args = parser.parse_args()

    try:
        controller = LightController(args.ip, args.port)
        controller.toggle()
        status = controller.get_status()
        state = "ON" if status.get("on") else "OFF"
        print(f"Light toggled to {state}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
