from machine import Pin, SoftI2C
from utime import sleep
import utime 
import ssd1306
from neopixel import NeoPixel

led = Pin('LED', Pin.OUT)

# GPIO 20번 핀에 연결된 버튼을 입력 모드로 설정합니다. 내부 풀업 저항을 활성화합니다.
button = Pin(20, Pin.IN, Pin.PULL_UP)

i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

np0 = NeoPixel(machine.Pin(21), 1)

def np_on():
    np0[0] = (255, 255, 255)
    np0.write()

def np_off():
    np0[0] = (0, 0, 0)
    np0.write()


# 무한 루프를 통해 버튼의 상태를 지속적으로 확인하고 LED를 제어합니다.
while True:


    # button의 상태를 출력합니다. (눌렸을 때 0, 눌리지 않았을 때 1)
    print(button.value())

    # oled에 button의 상태를 출력합니다.
    oled.fill(0)
    oled.text("Button: ", 0, 0)
    oled.text(str(button.value()), 0, 10)
    oled.show()


    if button.value() == 0:
        #led.value(False)
        np_on()
    else:
        #led.value(True)
        np_off()

    # 0.1초마다 반복합니다.
    utime.sleep(0.1)



