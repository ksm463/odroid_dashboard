import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import sqlite3
from utils import config_mng


ini_dict = config_mng.get_config_dict()
MAX_LENGTH = int(ini_dict['DASH']['max_length'])  
DASH_INTERVAL = int(ini_dict['DASH']['dash_interval'])
temperature_values = deque(maxlen=MAX_LENGTH)
humidity_values = deque(maxlen=MAX_LENGTH)
timestamps = deque(maxlen=MAX_LENGTH)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=DASH_INTERVAL, 
        n_intervals=0
    )
])


# 최근 온도 습도 데이터를 DB에서 읽어오는 함수
def read_last_temperature_humidity():
    try:
        conn = sqlite3.connect("temp_humid.db")
        c = conn.cursor()
        
        # 마지막 온도와 습도 데이터 가져오기
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

# 온도 습도 업데이트 함수
def update_temperature_humidity():
    temperature, humidity, timestamp = read_last_temperature_humidity()
    if temperature is not None and humidity is not None and timestamp is not None:
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
                                   yaxis=dict(title='Temperature (°C)'))
    
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
                                yaxis=dict(title='Humidity (%)'))
    
    return {'data': humidity_data, 'layout': humidity_layout}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8085)