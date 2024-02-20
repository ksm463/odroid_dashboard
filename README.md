# DHT22 센서 기반 온도 및 습도 대시보드 프로젝트

오드로이드의 핀에 연결된 DHT22 센서를 사용하여 온도와 습도 데이터를 측정하고, FastAPI 및 SQLModel을 사용하여 SQLite 데이터베이스에 저장한 후, Dash를 사용하여 실시간 차트로 시각화하는 대시보드를 구현하는 프로젝트입니다.

## 프로젝트 구성 요소

- **DHT22 센서**: 온도와 습도 측정
- **Odroid N2+**: 센서 데이터 수집 장치
- **FastAPI**: 웹 애플리케이션 프레임워크
- **Uvicorn**: ASGI 서버
- **SQLModel**: 데이터베이스 모델링
- **SQLite**: 데이터 저장소
- **Adafruit-circuitpython-dht**: DHT22 센서와의 통신을 위한 라이브러리
- **board**: 하드웨어 핀 제어
- **Loguru**: 로깅
- **Dash**: 웹 대시보드 구현

## 설치 및 실행 방법

1. 필요한 라이브러리 설치:
    ```bash
    pip install fastapi uvicorn sqlmodel sqlite board loguru dash
    pip install dash dash-core-components dash-html-components plotly
    ```
    * adafruit-circuitpython-dht는 설치 과정이 별도로 필요합니다. Odroid 위키를 참고하세요. https://wiki.odroid.com/odroid-n2/application_note/gpio/circuitpython

2. 서버 실행:
    ```bash
    uvicorn main:app --reload
    ```

3. 대시보드 접속:
    http://localhost:8085
   
## 프로젝트 구조

main.py 
FastAPI 애플리케이션

dashboard.py 
Dash 대시보드

temp_humid.db 
SQLite 데이터베이스 파일

## 데이터 수집 및 저장

DHT22 센서에서 측정한 온도와 습도 데이터를 FastAPI를 이용해 수집하며, SQLModel을 사용하여 SQLite 데이터베이스에 저장합니다. 이를 통해 시간에 따른 변화를 추적할 수 있습니다.

## 대시보드 시각화

Dash로 개발한 웹 대시보드가 온도와 습도 데이터를 실시간으로 차트에 표시합니다.

## 스크린샷

![Screenshot at 2024-02-17 14-43-12](https://github.com/ksm463/odroid_dashboard/assets/113885176/a62728e2-f4e8-4439-ab0f-f9968184cacb)

