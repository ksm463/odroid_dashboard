import adafruit_dht
import board
from loguru import logger

class DHTSensor:
    def __init__(self, pin=board.D13):
        self.dht_device = adafruit_dht.DHT22(pin)

    async def get_temperature_humidity(self):
        attempts = 0
        while attempts < 5:  # 최대 5번까지 재시도
            try:
                temperature = self.dht_device.temperature
                humidity = self.dht_device.humidity
                if temperature is not None and humidity is not None:
                    logger.info(f"Temp={temperature:0.1f}*C Humidity={humidity:0.1f}%")
                    return temperature, humidity
                else:
                    raise ValueError("Sensor returned None values")
            except Exception as e:
                logger.debug(f"Failed to read sensor, attempt {attempts + 1}: {e}")
                attempts += 1
        logger.warning("Failed to read from sensor after multiple attempts")
        return None, None