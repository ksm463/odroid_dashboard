import time
from loguru import logger
import adafruit_dht
import board

# loguru를 사용하여 로그 파일 설정
logger.add("temperature_humidity.log", rotation="10 MB")

dhtDevice = adafruit_dht.DHT22(board.D13)

while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        # 로그 메시지 포맷팅 및 파일에 기록
        logger.info(f"Temp={temperature:0.1f}*C Humidity={humidity:0.1f}%")
        
        # 콘솔에도 출력 (선택사항)
        print(f"Temp={temperature:0.1f}*C Humidity={humidity:0.1f}%")
        
    except Exception as e:
        # 센서 읽기 실패시 에러 로깅
        logger.warning(f"failed to read sensor: {e}")

    # 10초 간격으로 데이터 측정
    time.sleep(10)