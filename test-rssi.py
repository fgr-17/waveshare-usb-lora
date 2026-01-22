#!/usr/bin/env python3
import serial
import time

DEVICE = '/dev/ttyACM0'
BAUD = 115200

def send_cmd(ser, cmd, delay=0.5):
    ser.reset_input_buffer()
    print(f">> {cmd}")
    ser.write(f"{cmd}\r\n".encode())
    time.sleep(delay)
    response = ser.read(ser.in_waiting or 100).decode('utf-8', errors='ignore').strip()
    print(f"<< {response}\n")
    return response

def main():
    ser = serial.Serial(DEVICE, BAUD, timeout=1)
    ser.reset_input_buffer()
    time.sleep(0.5)
    
    # Enter command mode
    print("--- Entering Command Mode ---")
    ser.write(b'+++\r\n')
    time.sleep(1.5)
    ser.read(ser.in_waiting or 100)
    
    # Enable RSSI output
    send_cmd(ser, 'AT+RSSI=1')
    
    # Verify settings
    send_cmd(ser, 'AT+RSSI?')
    send_cmd(ser, 'AT+TXCH?')
    send_cmd(ser, 'AT+RXCH?')
    
    # Exit command mode
    send_cmd(ser, 'AT+EXIT')
    
    print("=== Listening for RF activity ===")
    print("Start T114 transmitting now...")
    print("Press Ctrl+C to exit\n")
    
    try:
        while True:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting)
                # Show both hex and ASCII
                print(f"[RX] hex: {data.hex()} | ascii: {data.decode('utf-8', errors='replace')}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()

if __name__ == '__main__':
    main()