from pyatcrobo2.parts import IRPhotoReflector, DCMotor, Servomotor
from pystubit.board import button_a, display

import time

# ir = IRPhotoReflector("P0")
# ir2 = IRPhotoReflector('P1')
m1 = DCMotor("M1")
m2 = DCMotor("M2")

## 設置 Servo Motor
ls = Servomotor("P13") ## 越大越內
ms = Servomotor("P15") ## 0向天,100向地
rs = Servomotor("P16") ## 越細越內

speed = 100
m1.power(speed)
m2.power(speed)

threshold = 1800
# def run():
#     if 
# m1.cw() ## cw: 順時針, ccw: 逆時針
# m2.cw()

def default(): ## 打開
    ls.set_angle(40)
    ms.set_angle(100)
    rs.set_angle(140)
    time.sleep(3)

def grab(): ## 抓
    ls.set_angle(105)
    rs.set_angle(75)
    time.sleep(1)
    ms.set_angle(0)

default()

display.show("S", delay=0)
while True: ## 無限循環
    while not button_a.is_pressed(): ## 檢測按鈕A有沒有被按下
        pass ## 按鈕A沒有被按下將會跳過返回循環中

    display.clear() ## 當按鈕A被按下將會破壞循環, 同時執行 display.clear()
    grab()
    time.sleep(5)
    default()


m1.brake()
m2.brake()
