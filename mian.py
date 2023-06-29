from pyatcrobo2.parts import IRPhotoReflector, DCMotor, Servomotor, UltrasonicSensor
from pystubit.board import button_a, display

import time

## Sensor And Motor Setup
ir = IRPhotoReflector("P0")
ir2 = IRPhotoReflector('P1')

us = UltrasonicSensor("P0")

m1 = DCMotor("M1")
m2 = DCMotor("M2")

ls = Servomotor("P13") ## 越大越內
ms = Servomotor("P15") ## 0向天,100向地
rs = Servomotor("P16") ## 越細越內


speed:int = 100
m1.power(speed)
m2.power(speed)

threshold:int = 1800

def tracing():
    if ir.get_value() > threshold:
        m1.cw()
        m2.brake()
    else:
        m2.cw()
        m1.brake()

def cross_line():
    m1.cw()
    m2.cw()

    while ir.get_value() > threshold:
        pass
    while ir.get_value() < threshold:
        pass

def default(ls_angle:int = 105, ms_angle:int = 100, rs_angle:int = 75): ## 打開
    ls.set_angle(ls_angle)
    ms.set_angle(ms_angle)
    rs.set_angle(rs_angle)
    time.sleep(3)

def grab(ls_angle:int = 105, rs_angle:int = 75, distance:int = 3): ## 抓
    while int(us.get_distance()) <= distance:
        ls.set_angle(ls_angle)
        rs.set_angle(rs_angle)
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

# Test

def detected(distance:int = 5): ## 當障礙物同機械人距離少於5cm時停下, 並在LED板顯示P
    m1.cw()
    m2.cw()
    while int(us.get_distance()) > distance:
        print("%d cm Still detecting"%(int(us.get_distance())))
        time.sleep(5)
    print("%d cm Obstacle detected!"%(int(us.get_distance())))
    m1.brake()
    m2.brake()
    display.show("P", delay=0)
    time.sleep(3)
    display.clear()