import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import datetime

# 고정 길이를 갖는 deque를 사용하여 최근 데이터를 저장
MAX_LENGTH = 20  # 저장할 데이터 포인트의 최대 개수
temperature_values = deque(maxlen=MAX_LENGTH)
humidity_values = deque(maxlen=MAX_LENGTH)
timestamps = deque(maxlen=MAX_LENGTH)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=10000,  # milliseconds
        n_intervals=0
    )
])

def read_last_temperature_humidity():
    try:
        with open("temperature_humidity.log", "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "Temp=" in line and "Humidity=" in line:
                    # Temp=와 Humidity=를 기준으로 데이터 추출
                    temp_str = line.split("Temp=")[1].split("*")[0]  # 온도 값 추출
                    humidity_str = line.split("Humidity=")[1].split("%")[0]  # 습도 값 추출
                    temperature = float(temp_str)
                    humidity = float(humidity_str)
                    return temperature, humidity
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None, None

def update_temperature_humidity():
    temperature, humidity = read_last_temperature_humidity()
    if temperature is not None and humidity is not None:
        # 현재 시간을 타임스탬프 리스트에 추가
        now = datetime.datetime.now()
        timestamps.append(now.strftime("%H:%M:%S"))
        # 새로운 온도와 습도 값을 각각의 리스트에 추가
        temperature_values.append(temperature)
        humidity_values.append(humidity)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # 온도와 습도 데이터 업데이트
    update_temperature_humidity()

    # 그래프 데이터 생성
    data = [
        go.Scatter(x=list(timestamps), y=list(temperature_values), name='Temperature', mode='lines+markers'),
        go.Scatter(x=list(timestamps), y=list(humidity_values), name='Humidity', mode='lines+markers')
    ]

    # 그래프 레이아웃 설정
    layout = go.Layout(title="Real-time Temperature and Humidity Data",
                       xaxis=dict(title='Time'),
                       yaxis=dict(title='Value'))

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)