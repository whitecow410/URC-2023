# 載入模組
from pyatcrobo2.parts import Servomotor, IRPhotoReflector, DCMotor
from pystubit.board import button_a, display, Image
import time

# 功能設置 / 定義
threshold = [1700, 2000]  # 1700, 2000

fast = 120
slow = 50

times = 0
x = y = z = 0
a = b = 0

ir = IRPhotoReflector("P1")
ir2 = IRPhotoReflector('P0')
ir3 = IRPhotoReflector('P2')

m1 = DCMotor("M1")
m2 = DCMotor("M2")
m1.brake()
m2.brake()

servoM_a = Servomotor("P15")
servoM_b = Servomotor("P13")
servoM_c = Servomotor("P14")

m1.power(fast)
m2.power(fast)


# 記錄最後行動
class event:
    move = None
    turn = None


class motor:
    # 設置 Motor
    def servoMA(angle=90):
        servoM_a.set_angle(angle)

    def servoMB(angleb=55, anglec=115):
        servoM_b.set_angle(angleb)
        servoM_c.set_angle(anglec)

    def set_speed(speed):
        m1.power(speed)
        m2.power(speed)


def detect(color=""):
    # 檢查2個紅外線感應器是否皆為黑色
    if color.lower() == "black":
        return True if ir.get_value() < threshold[0] and ir2.get_value() < threshold[1] else False
    # 檢查2個紅外線感應器是否皆為白色
    elif color.lower() == "white":
        return True if ir.get_value() > threshold[0] and ir2.get_value() > threshold[1] else False
    # 返回目前紅外線感應器所檢測到的顏色
    else:
        return "white" if ir.get_value() > threshold[0] and ir2.get_value() > threshold[1] else "black"


class move:
    global event

    # 停止
    def stop():
        m1.brake()
        m2.brake()

    # 向前
    def forward():
        event.move = lambda: move.forward  # <- lambda 可以將一個function以變數形式儲存
        m1.cw()
        m2.cw()

    # 向後
    def backward():
        event.move = lambda: move.backward  # <- lambda 可以將一個function以變數形式儲存
        m1.ccw()
        m2.ccw()

    # 轉左
    def left(auto=False):
        event.turn = lambda: move.left  # <- lambda 可以將一個function以變數形式儲存
        if not auto:
            m1.cw()
            m2.ccw()
        else:
            # 自動檢測
            move.left()
            time.sleep(1)
            while ir.get_value() > threshold[0]:
                move.left()
            move.stop()

    # 轉右
    def right(auto=False):
        event.turn = lambda: move.right  # <- lambda 可以將一個function以變數形式儲存
        if not auto:
            m1.ccw()
            m2.cw()
        else:
            # 自動檢測
            move.right()
            time.sleep(1)
            while ir2.get_value() > threshold[1]:
                move.right()
            move.stop()


# 抓實貨物
def pick(a=110, b=98, c=82):  # 55 115
    motor.servoMA(80)
    time.sleep(0.3)
    motor.servoMB(b, c)
    time.sleep(1)
    motor.servoMA(a)


# 放開貨物
def drop(a=None):
    if a:
        motor.servoMA(a)
        time.sleep(0.3)
    motor.servoMB()
    motor.servoMA()


# 自動修正路線
def fix():
    while (ir.get_value() < threshold[0] or ir2.get_value() < threshold[1]) and event.move != move.backward:
        # <- 如果左邊的紅外線感應器檢測到黑色, 自動向左修正
        if ir.get_value() < threshold[0] and ir2.get_value() > threshold[1]:
            move.left()
        # <- 如果右邊的紅外線感應器檢測到黑色, 自動向右修正
        elif ir.get_value() > threshold[0] and ir2.get_value() < threshold[1]:
            move.right()
        else:
            break


# 預備啟動
def setup():
    # 初始化階段
    global threshold, t
    motor.servoMA()
    motor.servoMB()
    m1.brake()
    m2.brake()
    if not threshold:
        # 掃描白值和黑值之間的數值
        data = []
        for i in range(2):
            while button_a.is_pressed():
                pass
            display.show("W" if i == 0 else "B", delay=0)
            while not button_a.is_pressed():
                pass
            value = [ir.get_value(), ir2.get_value()]
            print(value)
            data += value
        threshold.append(
            int((data[0] + data[2]) / 2)
        )
        threshold.append(
            int((data[1] + data[3]) / 2)
        )
        print(threshold)
        while button_a.is_pressed():
            pass
    # 當按下按鈕 A 時啓動
    display.show("G", delay=0)
    while not button_a.is_pressed():
        pass
    display.clear()


# 懶得解釋.... XD 總之就係沿住路線工作
def tracking():
    global times, x, y, z, a
    if times < 1:
        times += 1
    else:
        if x == 0:
            time.sleep(0.1)
            motor.servoMA(145)
            move.backward()
            time.sleep(1)
            move.left(auto=True)
            fix()
            move.backward()
            time.sleep(0.5)
            move.forward()
            x += 1
        elif x == 1:
            time.sleep(2.5)
            move.left()
            time.sleep(1.3)
            move.forward()
            time.sleep(0.5)
            while detect('white'):
                pass
            time.sleep(0.5)
            move.left(auto=True)
            motor.set_speed(fast)
            fix()
            x += 1
        elif x == 2:
            move.backward()
            while ir3.get_value() > 1800:
                pass
            move.stop()
            pick()
            time.sleep(0.3)
            move.forward()
            while detect('white'):
                pass
            time.sleep(0.35)
            fix()
            move.left(auto=True)
            fix()
            move.forward()
            x += 1
        elif x == 3:
            while detect('black'):
                pass
            time.sleep(0.35)
            fix()
            move.right(auto=True)
            fix()
            move.forward()
            x += 1
        elif x == 4:
            move.stop()
            move.backward()
            while detect('black'):
                pass
            time.sleep(0.15)
            move.stop()
            drop(98)
            move.backward()
            x += 1
        elif x == 5:
            move.forward()
            while detect('black'):
                pass
            time.sleep(0.35)
            fix()
            if z < 1:
                move.right(auto=True) if y < 1 else move.left(auto=True)
            else:
                move.left(auto=True) if y < 1 else move.right(auto=True)
            y += 1
            if y >= 2:
                y = 0
                x += 1
        elif x == 6:
            while ir3.get_value() < 2850:
                pass
            move.stop()
            pick(160) if z == 0 else pick(145)
            move.right(auto=True) if z == 0 else move.left(auto=True)
            move.forward()
            x += 1
            times = 0
        elif x == 7:
            time.sleep(2.5)
            move.right() if z == 0 else move.left()
            time.sleep(1.3)
            move.forward()
            time.sleep(0.5)
            while detect('white'):
                pass
            time.sleep(0.5)
            move.right(auto=True) if z == 0 else move.left(auto=True)
            motor.set_speed(fast)
            fix()
            x += 1
        elif x == 8:
            l = 145
            if z == 0:
                time.sleep(0.35)
                move.stop()
                while l > 80:
                    l -= 5
                    motor.servoMA(l)
                    time.sleep(0.3)
                move.stop()
                motor.servoMB(88, 92)
                motor.servoMA(90)
                move.forward()
                time.sleep(1.6)
                move.stop()
                motor.servoMB()
            elif z > 0:
                while ir3.get_value() < 2850:
                    pass
                move.stop()
                time.sleep(0.3)
                sg = [100, 80]
                while l > 120:
                    l -= 5
                    motor.servoMA(l)
                    time.sleep(0.3)
                while sg[0] > 85 and sg[1] < 95:
                    sg[0] -= 2
                    sg[1] += 2
                    motor.servoMB(sg[0], sg[1])
                    time.sleep(0.3)
                time.sleep(0.2)
                motor.servoMB()
            motor.servoMA(145)
            move.backward()
            if z <= 0:
                z += 1
                x = 5
            else:
                x += 1
        elif x == 9:
            move.stop()
            motor.servoMA(90)
            for i in range(12):
                motor.servoMB(100, 80)
                time.sleep(0.3)
                motor.servoMB()
                time.sleep(0.3)
            time.sleep(1000)

    fix()
    event.move()()
    while detect('black'):  # <- 防止在同一個黑色線上觸發多次, 當車子已經觸發上述功能後將會在此階段無限重複直至車子離開黑色線
        pass


# if __name__ == "__main__":
setup()
move.forward()
while True:
    if detect('black'):  # <- 當檢測到兩邊黑色時皆為十字路口
        tracking()  # 當上述條件觸發事, 執行工作
    else:
        fix()  # 自動修復路線
        event.move()()  # 根據上一次移動的方向繼續移動 ( if 機器人上一次移動是向前的話, 這次一樣會向前)
