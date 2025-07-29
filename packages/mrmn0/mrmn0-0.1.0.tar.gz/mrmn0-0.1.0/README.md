# README.md

# Arduino Controller

아두이노와 PC 간의 시리얼 통신을 쉽게 제어할 수 있는 Python 라이브러리입니다.

## 설치 방법
```bash
pip install lha_arducon

## 사용예시
from lha_arducon import  ArduinoController

arduino = ArduinoController()
arduino.connect_serial()
arduino.control_led(5, 'on')