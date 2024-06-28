from pyatcrobo2.parts import Servomotor, IRPhotoReflector, DCMotor
from pystubit.board import button_a, display
import time


class IRSensor:
    def __init__(self, port, threshold=2000) -> None:
        self.sensor = IRPhotoReflector(port)
        self.threshold = threshold

    def get_value(self) -> int:
        return self.sensor.get_value()

    def set_threshold(self, threshold) -> None:
        self.threshold = threshold

    def is_black(self) -> bool:
        value = self.get_value()
        return True if value < self.threshold else False


class CarMotor:
    def __init__(self, port, power=150) -> None:
        self.motor = DCMotor(port)
        self.power = power

    def set_power(self, power) -> None:
        self.power = power

    def forward(self) -> None:
        self.motor.power(self.power)
        self.motor.ccw()

    def backward(self) -> None:
        self.motor.power(self.power)
        self.motor.cw()

    def stop(self):
        self.motor.brake()


class ServoMotor:
    def __init__(self, port) -> None:
        self.servo = Servomotor(port)
        self.angle = 0

    def set_angle(self, angle) -> None:
        self.angle = angle
        self.servo.set_angle(angle)


ir_left = IRSensor('P0')
ir_right = IRSensor('P1')
ir_center = IRSensor('P2')

motor_left = CarMotor('M1')
motor_right = CarMotor('M2')

servo1 = ServoMotor('P15')
servo2 = ServoMotor('P13')
servo3 = ServoMotor('P14')


def set_power(left, right):
    motor_left.set_power(left)
    motor_right.set_power(right)


def move_forward():
    motor_left.forward()
    motor_right.forward()


def move_backward():
    motor_left.backward()
    motor_right.backward()


def turn_left():
    motor_right.forward()
    motor_left.backward()


def turn_right():
    motor_left.forward()
    motor_right.backward()


def stop():
    motor_left.stop()
    motor_right.stop()


def auto_left():
    turn_left()
    while ir_right.is_black():
        pass
    while not ir_right.is_black():
        pass
    stop()


def auto_right():
    turn_right()
    while ir_left.is_black():
        pass
    while not ir_left.is_black():
        pass
    stop()


def pick(L_start, r_start, l_end, r_end):
    for i, r in zip(range(servo2.angle, targetAngle, 1 if servo2.angle < targetAngle else -1),
                    range(servo3.angle, targetAngle, 1 if servo3.angle < targetAngle else -1)):
        servo3.set_angle(r)
        servo2.set_angle(i)
    
def drop(left=60, right=60):
    servo2.set_angle(left)
    servo3.set_angle(right)


def set_hight(hight, speed=None):
    for i in range(servo1.angle, speed or (hight, 1 if servo1.angle < hight else -1)):
        servo1.set_angle(hight)


def fix(event=stop):
    while ir_left.is_black() or ir_right.is_black():
        if ir_left.is_black() and not ir_right.is_black():
            turn_left()
        elif ir_right.is_black() and not ir_left.is_black():
            turn_right()
        else:
            break
    event()

def forward_line(move, times=1):
    move()
    for _ in range(times):
        while ir_left.is_black() and ir_right.is_black():
            pass
        while True:
            if ir_left.is_black() and ir_right.is_black():
                break
            else:
                fix(move)
    stop()


def square():
    forward_line(move_forward, 3)
    auto_left()
    while True:
        move_forward()
        forward_line(move_forward, 2)
        auto_left()


def setup(threshold='auto'):
    temp = []
    if not threshold:
        for i in range(2):
            while button_a.is_pressed():
                pass
            display.show("W" if i == 0 else "B", delay=0)
            while not button_a.is_pressed():

                pass
            temp += [ir_left.get_value(), ir_right.get_value()]
        while button_a.is_pressed():
            pass
        ir_left.set_threshold(int((temp[0] + temp[2]) / 2))
        ir_right.set_threshold(int((temp[1] + temp[3]) / 2))
    elif threshold == 'auto':
        display.show("Auto", delay=0)
        while button_a.is_pressed():
            pass
        while not button_a.is_pressed():
            pass
        # if not ir_left.get_value() >= ir_left.threshold or not ir_right.get_value() >= ir_right.threshold:
        #     move_forward()
        #     while not ir_left.get_value() >= ir_left.threshold or not ir_right.get_value() >= ir_right.threshold:
        #         pass
        #     stop()
        temp += [ir_left.get_value(), ir_right.get_value()]
        for index, ir in enumerate([ir_left, ir_right]):
            if temp[index] - ir.get_value() <= 1000:
                move_forward()
                while temp[index] - ir.get_value() <= 1000:
                    pass
            stop()
            temp += [ir.get_value()]
        ir_left.set_threshold(int((temp[0] + temp[2]) / 2))
        ir_right.set_threshold(int((temp[1] + temp[3]) / 2))
    elif isinstance(threshold, list):
        ir_left.set_threshold(threshold[0])
        ir_right.set_threshold(threshold[1])
    servo1.set_angle(10)
    drop()
    display.show("G", delay=0)
    while not button_a.is_pressed():
        pass
    display.clear()

setup()
# Part 1
pick(50, 50)
forward_line(move_forward, 3)
move_forward()
time.sleep(0.3)
stop()
time.sleep(0.5)
pick([60, 90], [60, 90])
time.sleep(0.5)
forward_line(move_backward, 2)
time.sleep(0.5)
drop()

# # Part 2
# forward_line(move_backward)
# move_forward()
# time.sleep(0.5)
# auto_right()
# time.sleep(0.5)
# forward_line(move_forward)
# time.sleep(0.5)
# pick([60, 90, 2], [60, 90, 2])
# time.sleep(0.5)
# set_hight(180)
# time.sleep(0.5)
# move_forward()
# time.sleep(0.5)
# auto_left()
# time.sleep(0.5)
# move_forward()
# while ir_center.get_value() <= 590:
#     move_forward()
#     fix()
# stop()
# time.sleep(0.5)
# for i in range(100, -1):
#     set_hight(i)
#     time.sleep(0.1)
# drop(160, 160)
# time.sleep(0.5)
# drop()
# time.sleep(0.5)
# set_hight(0)
# time.sleep(0.5)
# pick()
# time.sleep(0.5)
# set_hight(50)
# move_forward()
# time.sleep(0.5)
# auto_left()
# time.sleep(0.5)
# while ir_center.get_value() <= 490:
#     move_forward()
#     fix()
# stop()
# time.sleep(0.5)
# set_hight(50)
# time.sleep(0.5)
# drop()

