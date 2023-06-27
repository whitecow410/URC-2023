from pyatcrobo2.parts import IRPhotoReflector, DCMotor, Servomotor
from pystubit.board import button_a, display
import time

# ir = IRPhotoReflector("P0")
# ir2 = IRPhotoReflector('P1')
m1 = DCMotor("M1")
m2 = DCMotor("M2")

ls = Servomotor("P13")
# 越大越內

ms = Servomotor("P15")
# 0向天,100向地

rs = Servomotor("P16")
# 越細越內

speed = 100
m1.power(speed)
m2.power(speed)
# m1.cw()
# m2.cw()


def default():
    ls.set_angle(40)
    ms.set_angle(100)
    rs.set_angle(140)
    time.sleep(3)


default()
threshold = 1800


def grab():
    # 抓
    ls.set_angle(105)
    rs.set_angle(75)
    time.sleep(1)
    ms.set_angle(0)


display.show("S", delay=0)
while True:
    while not button_a.is_pressed():
        pass
    display.clear()
    grab()
    time.sleep(5)
    default()

m1.brake()
m2.brake()
