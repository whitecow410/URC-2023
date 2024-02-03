from pyatcrobo2.parts import DCMotor, IRPhotoReflector, ColorSensor
from pystubit.board import button_a, button_b, display, Image
import time

m1 = DCMotor("M1")
m2 = DCMotor("M2")
m1.brake()
m2.brake()

ir = IRPhotoReflector('P0')
# colorSen = ColorSensor('I2C')

threshold = 2780
x = 0

# ColorMap = {
#     'white': [range(55, 60), range(65, 70), range(36, 41)],
#     'black': [range(24), range(22, 27), range(7, 11)],
#     # 'red': [range(57, 62), range(48, 53), range(5, 10)],
#     # 'yellow': [range(55, 60), range(51, 56), range(6, 11)],
#     # 'bule': [range(50, 55), range(71, 76), range(81, 85)],
#     # 'pruple': [range(28, 33), range(14, 19), range(12, 17)]
# }

# for _color in ColorMap:
#     ColorMap[_color] = [tuple(i) for i in ColorMap[_color]]

# ColorCode = {
#     'red': 6,
#     'yellow': 0,
#     'blue': 7,
#     'purple': 1
# }


class setSpeed:
    def forward():
        return 100, 100

    def backward():
        return 100, 100

    def set_speed(m01, m02):
        m1.power(m01)
        m2.power(m02)


class move:
    def stop():
        m1.brake()
        m2.brake()
        display.clear()

    def forward():
        m1.cw()
        m2.cw()
        display.show(Image('00100:01110:00000:00100:00100'))

    def backward():
        m1.ccw()
        m2.ccw()
        display.show(Image('00100:00100:00000:01110:00100'))

    def left():
        m1.ccw()
        m2.cw()
        display.show(Image('00000:01100:01000:00010:00000'))

    def right():
        m1.cw()
        m2.ccw()
        display.show(Image('00000:00110:00010:01000:00000'))


def setup():
    global threshold
    move.stop()

    # get threhold
    if not threshold:
        value = []
        for i in range(2):
            while button_a.is_pressed():
                pass
            display.show("W" if i == 0 else "B", delay=0)
            while not button_a.is_pressed():
                pass
            value.append(ir.get_value())
        threshold = int((value[0] + value[1]) / 2)
        print(threshold)
        while button_a.is_pressed():
            pass

    # Run
    setSpeed.set_speed(147, 150)
    display.show("G", delay=0)
    while not button_b.is_pressed():
        pass
    display.clear()


# def fix():
#     while ir.get_value() < threshold:
#         move.right()
#     while colorSen.get_values in ColorMap['black']:
#         move.left()


def tracking():
    global x
    if x == 0:
        move.stop()
        move.backward()
        time.sleep(0.6)
        move.left()
        time.sleep(0.2)
        move.forward()
    if x == 1:
        move.stop()
        move.backward()
        time.sleep(0.6)
        move.left()
        time.sleep(0.2)
        move.forward()
    elif x in [2, 3]:
        move.stop()
        move.backward()
        time.sleep(0.55)
        move.right()
        time.sleep(0.2)
        move.forward()
    elif x == 4:
        move.stop()
        time.sleep(0.1)  
        move.right()
        time.sleep(0.1)
        move.stop()
        move.forward()
    elif x == 5:
        move.stop()
        for x in range(5):
            for y in range(5):
                display.set_pixel(x, y, (31, 31, 31))
        
    while ir.get_value() < threshold:
        pass
    x += 1


setup()
move.forward()
while True:
    while ir.get_value() < threshold   :
        tracking()
