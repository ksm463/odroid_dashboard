import requests

def send_telegram(message):
    token = '6760963910:AAGp7hAMztb_nESlDSNPhQlUX1fajqKCCqE'
    chat_id = '43517934'
    send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    
    response = requests.get(send_text)
    return response.json()