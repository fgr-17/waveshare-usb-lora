#!/usr/bin/env python3
import serial
import time

DEVICE = '/dev/ttyACM0'
BAUD = 115200

def send_cmd(ser, cmd, delay=0.5):
    """Send AT command and print response"""
    ser.reset_input_buffer()
    print(f">> {cmd}")
    ser.write(f"{cmd}\r\n".encode())
    time.sleep(delay)
    response = ser.read(ser.in_waiting or 100).decode('utf-8', errors='ignore').strip()
    if response:
        print(f"<< {response}")
    else:
        print("<< (no response)")
    print()
    return response

def main():
    print(f"=== Configuring USB LoRa for T114 Communication ===")
    print(f"Device: {DEVICE}")
    print(f"Baud: {BAUD}\n")
    
    ser = serial.Serial(DEVICE, BAUD, timeout=1)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    time.sleep(0.5)
    
    # Enter AT command mode
    print("--- Entering Command Mode ---")
    ser.write(b'+++\r\n')
    time.sleep(1.5)
    response = ser.read(ser.in_waiting or 100).decode('utf-8', errors='ignore')
    print(f"Mode response: {response}\n")
    
    # Verify communication
    print("--- Verify Communication ---")
    send_cmd(ser, 'AT')
    send_cmd(ser, 'AT+VER')
    
    # Query current settings
    print("--- Current Settings ---")
    send_cmd(ser, 'AT+SF?')
    send_cmd(ser, 'AT+BW?')
    send_cmd(ser, 'AT+CR?')
    send_cmd(ser, 'AT+PWR?')
    send_cmd(ser, 'AT+TXCH?')
    send_cmd(ser, 'AT+RXCH?')
    send_cmd(ser, 'AT+NETID?')
    send_cmd(ser, 'AT+ADDR?')
    send_cmd(ser, 'AT+MODE?')
    send_cmd(ser, 'AT+RSSI?')
    
    # Configure to match T114 settings:
    # frequency=868MHz, BW=125kHz, SF=7, CR=4/5
    print("--- Configuring Parameters ---")
    
    # SF=7
    send_cmd(ser, 'AT+SF=7')
    
    # BW=125kHz (7)
    send_cmd(ser, 'AT+BW=0')
    
    # CR=4/5 (1)
    send_cmd(ser, 'AT+CR=1')
    
    # Power=14dBm
    send_cmd(ser, 'AT+PWR=14')
    
    # Channel (check what channel = 868MHz for your module)
    send_cmd(ser, 'AT+TXCH=18')
    send_cmd(ser, 'AT+RXCH=18')
    
    # Network ID
    send_cmd(ser, 'AT+NETID=0')
    
    # Address (0 = broadcast)
    send_cmd(ser, 'AT+ADDR=0')
    
    # Verify new settings
    print("--- Verify New Settings ---")
    send_cmd(ser, 'AT+SF?')
    send_cmd(ser, 'AT+BW?')
    send_cmd(ser, 'AT+CR?')
    send_cmd(ser, 'AT+PWR?')
    
    # Exit command mode to enter transparent/receive mode
    print("--- Exiting Command Mode ---")
    send_cmd(ser, 'AT+EXIT')
    
    print("=== Configuration Complete ===")
    print("Module is now in transparent mode, waiting for packets...")
    print("Press Ctrl+C to exit\n")
    
    # # Listen for incoming packets
    try:
        while True:
           if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            try:
                # Decode to string
                text = data.decode('utf-8', errors='replace')
                
                # Last 2 chars are RSSI hex value (when RSSI enabled)
                if len(text) >= 2:
                    payload = text[:-2]
                    rssi_hex = text[-2:]
                    try:
                        rssi_val = int(rssi_hex, 16)
                        rssi_dbm = -rssi_val  # Convert to negative dBm
                        print(f"[RX] {payload.strip()}  (RSSI: {rssi_dbm} dBm)")
                    except ValueError:
                        # Not valid hex, just print raw
                        print(f"[RX] {text}")
                else:
                    print(f"[RX] {text}")
            except:
                print(f"[RX] raw: {data.hex()}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()
    
    
    # count = 0
    # try:
    #     while True:
    #         count += 1
    #         message = f"Hello T114 #{count}"
    #         print(f"[TX] {message}")
    #         ser.write(message.encode())
    #         time.sleep(3)
    # except KeyboardInterrupt:
    #     print("\nStopped.")
    # finally:
    #     ser.close()


if __name__ == '__main__':
    main()