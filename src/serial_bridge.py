import os
import re
import sys
import time
import serial
from dotenv import load_dotenv

# Load local .env file
load_dotenv()

# ================= Configuration =================
# Do not provide default values; force specification via .env or environment variables.
SERIAL_PORT = os.getenv("SERIAL_PORT", "")
BAUD_RATE = int(os.getenv("BAUD_RATE", "9600"))
# =================================================

def read_sensor_once():
    """Read temperature and humidity data from Arduino exactly once and return it."""
    if not SERIAL_PORT:
        print('{"error": "SERIAL_PORT is not configured in .env file"}', file=sys.stderr)
        return None, None

    try:
        # Set timeout to 2 seconds to wait until data is received.
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Wait for Arduino to reset after opening serial connection.
        
        temp_pat = re.compile(r"Temperature:\s*([\d.]+)")
        hum_pat = re.compile(r"Humidity:\s*([\d.]+)")

        # Read up to 10 lines to find the first valid temperature/humidity packet.
        for _ in range(10):
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            
            t_match = temp_pat.search(line)
            h_match = hum_pat.search(line)
            
            if t_match and h_match:
                temp = t_match.group(1)
                hum = h_match.group(1)
                ser.close()
                return temp, hum
                
        ser.close()
        return None, None
    except Exception as e:
        print(f'{{"error": "{str(e)}"}}', file=sys.stderr)
        return None, None

def main():
    # Handle the one-shot retrieval option (--once)
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        if not SERIAL_PORT:
            print('{"error": "SERIAL_PORT environment variable is missing. Set it in .env file."}', file=sys.stderr)
            sys.exit(1)

        temp, hum = read_sensor_once()
        if temp and hum:
            # Print in standard JSON format for easy agent parsing.
            print(f'{{"temperature": {temp}, "humidity": {hum}}}')
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("Usage: uv run src/serial_bridge.py --once", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
