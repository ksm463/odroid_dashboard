import requests

def send_telegram(sensor_state, sensor_data):
    message = None
    if sensor_state == "very_high_temp":
        message = f"경고: 온도가 {sensor_data.temperature}°C로 매우 높습니다."
    elif sensor_state == "high_temp":
        message = f"경고: 온도가 {sensor_data.temperature}°C로 비정상 범위에 진입했습니다."
    elif sensor_state == "low_humidity":
        message = f"주의: 습도가 {sensor_data.humidity}%로 낮습니다."
    elif sensor_state == "high_humidity":
        message = f"주의: 습도가 {sensor_data.humidity}%로 높습니다."
    
    token = 'token_id'
    chat_id = 'chat_id'
    send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    
    response = requests.get(send_text)
    return response.json()
