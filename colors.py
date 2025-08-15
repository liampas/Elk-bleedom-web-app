#!/usr/bin/env python3
from bluepy.btle import Peripheral
import sys

with open("devices.txt") as f:
    MACS = [line.strip() for line in f if line.strip()]

#Characteristic UUID for color control
COLOR_CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

#naming of the modes:
#effects:
# S = strobe flash
# F = fade
# #CF = # colors cross fade
# CF = cross fade (2 colors)
# #J = # colors jump
#
#colors:
# r = red
# g = green
# b = blue
# y = yellow
# c = cyan
# m = magenta
# w = white

# Predefined packets
COLOR_PACKETS = {
    "rgb": "7e00038a03000000ef",
    "3j":  "7e00038703000000ef",
    "7j":  "7e00038803000000ef",
    "3cf": "7e00038903000000ef",
    "7cf": "7e00038a03000000ef",
    "rf":  "7e00038b03000000ef",
    "gf":  "7e00038c03000000ef",
    "bf":  "7e00038d03000000ef",
    "yf":  "7e00038e03000000ef",
    "cf":  "7e00038f03000000ef",
    "mf":  "7e00039003000000ef",
    "wf":  "7e00039103000000ef",
    "rgcf":"7e00039203000000ef",
    "rbcf":"7e00039303000000ef",
    "gbcf":"7e00039403000000ef",
    "7s":  "7e00039503000000ef",
    "rs":  "7e00039603000000ef",
    "gs":  "7e00039703000000ef",
    "bs":  "7e00039803000000ef",
    "ys":  "7e00039903000000ef",
    "cs":  "7e00039a03000000ef",
    "ms":  "7e00039b03000000ef",
    "ws":  "7e00039c03000000ef",

    "red":   "7e000503ff000000ef",
    "green": "7e00050300ff0000ef",
    "blue":  "7e0005030000ff00ef",
    "yellow":  "7e000503ffff0000ef",
    "orange":  "7e000503ffa50000ef",
    "purple":  "7e000503ff00ff00ef",
    "white": "7e000503ffffff00ef",
    "off":   "7e00050300000000ef",
    
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

