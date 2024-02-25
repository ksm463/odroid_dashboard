import requests

def send_telegram(message):
    token = 'bot_token'
    chat_id = 'chat_id'
    send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    
    response = requests.get(send_text)
    return response.json()
