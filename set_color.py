#!/usr/bin/env python3
"""Set Elgato Key Light RGB color."""

import sys
import argparse
from scripts.light_controller import LightController


def main():
    parser = argparse.ArgumentParser(
        description="Set Elgato Key Light color (RGB 0-255)"
    )
    parser.add_argument("ip", help="IP address of the light")
    parser.add_argument("red", type=int, help="Red value (0-255)")
    parser.add_argument("green", type=int, help="Green value (0-255)")
    parser.add_argument("blue", type=int, help="Blue value (0-255)")
    parser.add_argument(
        "--port", type=int, default=9123, help="API port (default: 9123)"
    )

    args = parser.parse_args()

    try:
        controller = LightController(args.ip, args.port)
        controller.set_color(args.red, args.green, args.blue)
        print(f"Color set to RGB({args.red}, {args.green}, {args.blue})")
        return 0
    except ValueError as e:
        print(f"Invalid value: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
