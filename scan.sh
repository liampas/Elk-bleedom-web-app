#!/usr/bin/env bash

{ echo 'scan on'; sleep 5; echo 'scan off'; echo 'quit'; } | bluetoothctl | \
grep -oE '([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}' | \
sort -u | grep BE:27: > devices.txt
