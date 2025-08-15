#!/usr/bin/env python3
from bluepy.btle import Peripheral
import sys
#import numpy as np


with open("devices.txt") as f:
    MACS = [line.strip() for line in f if line.strip()]




#Characteristic UUID for color control
COLOR_CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

# Predefined packets
COLOR_PACKETS = {
    "rgb":  "7e00038903000000ef",
    "rgb2":  "7e00038a03000000ef",
    "green": "7e00050300ff0000ef",
    "blue":  "7e0005030000ff00ef",
    "white": "7e000503ffffff00ef",
    "off":   "7e00050300000000ef",
    "red":   "7e000503ff000000ef"
}
def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <color>")
        print(f"Available colors: {', '.join(list(COLOR_PACKETS.keys()) + ['hex'])}")
        return

    color_name = sys.argv[1].lower()

    if color_name == "hex":
        if len(sys.argv) != 3:
            print(f"Usage: {sys.argv[0]} hex <RRGGBB>")
            return
        hex_color = sys.argv[2].lower()
        if len(hex_color) != 6:
            print("Hex color must be 6 digits (RRGGBB).")
            return
        # convert hex RRGGBB into bytes
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        packet = bytes([0x7E, 0x00, 0x05, 0x03, r, g, b, 0x00, 0xEF])
    else:
        if color_name not in COLOR_PACKETS:
            print(f"Available colors: {', '.join(list(COLOR_PACKETS.keys()) + ['hex'])}")
            return
        packet = bytes.fromhex(COLOR_PACKETS[color_name])

    for mac in MACS:
        try:
            print(f"Connecting to {mac}…")
            p = Peripheral(mac)
            print("Connected!")

            print(f"Getting characteristic {COLOR_CHAR_UUID}…")
            char = p.getCharacteristics(uuid=COLOR_CHAR_UUID)[0]

            print(f"Writing {color_name} color packet…")
            char.write(packet, withResponse=False)
            print(f"{mac} updated successfully!")

            p.disconnect()
            print(f"{mac} disconnected.\n")
        except Exception as e:
            print(f"Failed to update {mac}: {e}\n")

if __name__ == "__main__":
    main()

