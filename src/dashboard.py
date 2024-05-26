import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import requests
from utils import ConfigManager


ini_path = "/home/odroid/workspace/odroid_dashboard/src/config.ini"
config = ConfigManager(ini_path)
ini_dict = config.get_config_dict()

API_URL = ini_dict['DASH']['API_URL']
MAX_LENGTH = int(ini_dict['DASH']['MAX_LENGTH'])  
DASH_INTERVAL = int(ini_dict['DASH']['DASH_INTERVAL'])
DB_PATH = ini_dict['DB']['DB_PATH']
DB_NAME = ini_dict['DB']['DB_NAME']

temperature_values = deque(maxlen=MAX_LENGTH)
humidity_values = deque(maxlen=MAX_LENGTH)
timestamps = deque(maxlen=MAX_LENGTH)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='temperature-graph'),
    ]),
    html.Div([
        dcc.Graph(id='humidity-graph'),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=DASH_INTERVAL,  # milliseconds
        n_intervals=0
    )
])

def fetch_sensor_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return []

def update_temperature_humidity():
    data = fetch_sensor_data()
    if data:
        # 데이터를 타임스탬프 기준으로 오름차순 정렬
        data_sorted = sorted(data, key=lambda x: x['timestamp'])

        # 새로운 타임스탬프, 온도, 습도 데이터 추출
        new_timestamps = [entry['timestamp'] for entry in data_sorted]
        new_temperatures = [entry['temperature'] for entry in data_sorted]
        new_humidities = [entry['humidity'] for entry in data_sorted]

        # 이전 데이터와 중복되지 않도록 추가
        last_timestamp = timestamps[-1] if timestamps else None
        for ts, temp, hum in zip(new_timestamps, new_temperatures, new_humidities):
            if last_timestamp is None or ts > last_timestamp:
                timestamps.append(ts)
                temperature_values.append(temp)
                humidity_values.append(hum)

# 온도 데이터 콜백
@app.callback(Output('temperature-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_temperature_graph(n):
    # 온도와 습도 데이터 업데이트
    update_temperature_humidity()
    
    # 온도 데이터
    temperature_data = [
        go.Scatter(
            x=list(timestamps), 
            y=list(temperature_values), 
            name='Temperature', 
            mode='lines+markers',
            line=dict(color='orange')
            )
    ]
    
    # 온도 레이블
    temperature_layout = go.Layout(title="Real-time Temperature Data",
                                   xaxis=dict(title='Time'),
                                   yaxis=dict(title='Temperature (°C)'),
                                   showlegend=True,
                                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return {'data': temperature_data, 'layout': temperature_layout}

# 습도 데이터 콜백
@app.callback(Output('humidity-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_humidity_graph(n):
    # 습도 업데이트는 온도에서 이미 했으므로 따로 진행 안함
    
    # 습도 데이터
    humidity_data = [
        go.Scatter(x=list(timestamps), 
                   y=list(humidity_values), 
                   name='Humidity', 
                   mode='lines+markers', 
                   line=dict(color='blue')
                   )
    ]
    
    # 습도 레이블
    humidity_layout = go.Layout(title="Real-time Humidity Data",
                                xaxis=dict(title='Time'),
                                yaxis=dict(title='Humidity (%)'),
                                showlegend=True,
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return {'data': humidity_data, 'layout': humidity_layout}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8085)