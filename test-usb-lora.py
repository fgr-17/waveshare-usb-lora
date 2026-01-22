#! /usr/bin/env python3

# Quick test
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(0.5)

# Enter AT mode
ser.write(b'+++\r\n')
time.sleep(1)
print('Response:', ser.read(100).decode('utf-8', errors='ignore'))

# Send AT
ser.write(b'AT\r\n')
time.sleep(0.3)
print('AT Response:', ser.read(100).decode('utf-8', errors='ignore'))

ser.close()
