#!/usr/bin/env python3
"""Set Elgato Key Light color temperature."""

import sys
import argparse
from scripts.light_controller import LightController


def main():
    parser = argparse.ArgumentParser(
        description="Set Elgato Key Light color temperature (2700K-7000K)"
    )
    parser.add_argument("ip", help="IP address of the light")
    parser.add_argument(
        "kelvin", type=int, help="Color temperature in Kelvin (2700-7000)"
    )
    parser.add_argument(
        "--port", type=int, default=9123, help="API port (default: 9123)"
    )

    args = parser.parse_args()

    try:
        controller = LightController(args.ip, args.port)
        controller.set_color_temperature(args.kelvin)
        print(f"Color temperature set to {args.kelvin}K")
        return 0
    except ValueError as e:
        print(f"Invalid value: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
