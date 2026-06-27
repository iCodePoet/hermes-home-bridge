import os
import re
import sys
import time
import serial
from dotenv import load_dotenv

# 로컬 .env 파일 로드
load_dotenv()

# ================= Configuration =================
# 기본값을 제공하지 않고, .env 혹은 환경변수로 명시하도록 유도합니다.
SERIAL_PORT = os.getenv("SERIAL_PORT", "")
BAUD_RATE = int(os.getenv("BAUD_RATE", "9600"))
# =================================================

def read_sensor_once():
    """아두이노로부터 딱 한 번만 온습도 데이터를 읽어서 반환하고 종료합니다."""
    if not SERIAL_PORT:
        print('{"error": "SERIAL_PORT is not configured in .env file"}', file=sys.stderr)
        return None, None

    try:
        # 타임아웃을 2초로 넉넉히 설정하여 값을 찾을 때까지 대기
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # 아두이노 리셋 대기
        
        temp_pat = re.compile(r"Temperature:\s*([\d.]+)")
        hum_pat = re.compile(r"Humidity:\s*([\d.]+)")

        # 최대 10라인을 읽으며 온습도가 매칭되는 최초 패킷을 찾습니다.
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
    # 1회성 가져오기 옵션 (--once) 처리
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        if not SERIAL_PORT:
            print('{"error": "SERIAL_PORT environment variable is missing. Set it in .env file."}', file=sys.stderr)
            sys.exit(1)

        temp, hum = read_sensor_once()
        if temp and hum:
            # 에이전트가 쉽게 파싱할 수 있도록 표준 JSON 포맷으로 출력
            print(f'{{"temperature": {temp}, "humidity": {hum}}}')
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("Usage: uv run src/bridge.py --once", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
