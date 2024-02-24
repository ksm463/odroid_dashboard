import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import datetime
import sqlite3

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
        # 데이터베이스 파일에 연결
        conn = sqlite3.connect("temp_humid.db")
        c = conn.cursor()
        
        # 가장 최근의 온도와 습도 데이터를 가져오는 쿼리 실행
        c.execute("SELECT temperature, humidity, timestamp FROM sensordata ORDER BY timestamp DESC LIMIT 1")
        row = c.fetchone()
        
        if row:
            temperature, humidity, timestamp = row
            return temperature, humidity, timestamp
        else:
            return None, None, None
    except Exception as e:
        print(f"Error reading from database: {e}")
        return None, None, None
    finally:
        conn.close()

def update_temperature_humidity():
    temperature, humidity, timestamp = read_last_temperature_humidity()
    if temperature is not None and humidity is not None and timestamp is not None:
        # 반환된 타임스탬프를 사용
        timestamps.append(timestamp)
        temperature_values.append(temperature)
        humidity_values.append(humidity)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='temperature-graph'),
    ]),
    html.Div([
        dcc.Graph(id='humidity-graph'),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=10000,  # milliseconds
        n_intervals=0
    )
])

# 온도 데이터를 위한 콜백
@app.callback(Output('temperature-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_temperature_graph(n):
    # 온도와 습도 데이터 업데이트
    update_temperature_humidity()
    
    # 온도 그래프 데이터 생성
    temperature_data = [
        go.Scatter(
            x=list(timestamps), 
            y=list(temperature_values), 
            name='Temperature', 
            mode='lines+markers',
            line=dict(color='orange')
            )
    ]
    
    # 온도 그래프 레이아웃 설정
    temperature_layout = go.Layout(title="Real-time Temperature Data",
                                   xaxis=dict(title='Time'),
                                   yaxis=dict(title='Temperature (°C)'))
    
    return {'data': temperature_data, 'layout': temperature_layout}

# 습도 데이터를 위한 콜백
@app.callback(Output('humidity-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_humidity_graph(n):
    # 이 함수 내에서는 데이터 업데이트를 호출하지 않습니다. 온도 업데이트 함수에서 이미 호출되었기 때문입니다.
    
    # 습도 그래프 데이터 생성
    humidity_data = [
        go.Scatter(x=list(timestamps), 
                   y=list(humidity_values), 
                   name='Humidity', 
                   mode='lines+markers', 
                   line=dict(color='blue')
                   )
    ]
    
    # 습도 그래프 레이아웃 설정
    humidity_layout = go.Layout(title="Real-time Humidity Data",
                                xaxis=dict(title='Time'),
                                yaxis=dict(title='Humidity (%)'))
    
    return {'data': humidity_data, 'layout': humidity_layout}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8085)