import utime
from machine import Pin, I2C, PWM, ADC
from ds3231_port import DS3231
import onewire, ds18x20
from neopixel import NeoPixel
import uos 
import sdcard

# 글로벌 변수
sensing_active = False
recording_active = False
recording_interval = 1800  # 데이터 기록 간격을 초 단위로 설정 (예: 30분마다 데이터 기록)
#recording_interval = 1  # 데이터 기록 간격을 초 단위로 설정 (예: 1초마다 데이터 기록)
file = None # 파일 객체 초기화
write_count = 0 # 안정적인 파일쓰기를 위한 카운터 초기화
write_threshold = 50 # 몇 회이상 쓰이면 파일을 다시 열도록 횟수 설정 

# LED, 버튼, 부저 설정
Led = Pin("LED", Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(22))

# I2C 설정
sdaPIN = Pin(4)
sclPIN = Pin(5)
i2c = I2C(0, sda=sdaPIN, scl=sclPIN)

# DS3231 RTC 및 DS18x20 온도 센서 설정
ds3231 = DS3231(i2c)
data = Pin(26)
temp_wire = onewire.OneWire(data)
temp_sensor = ds18x20.DS18X20(temp_wire)
roms = temp_sensor.scan()

# 네오픽셀 핀 초기화
np0 = NeoPixel(Pin(21), 1)

# 네오픽셀 상태를 추척하는 변수 초기화
def np_red():
    for i in range(0, np0.n):
        np0[i] = (64,0,0)
    np0.write()
def np_green():
    for i in range(0, np0.n):
        np0[i] = (0,64,0)
    np0.write()
def np_blue():
    for i in range(0, np0.n):
        np0[i] = (0,0,64) # blue with 25% brightness
    np0.write()
def np_yellow():
    for i in range(0, np0.n):
        np0[i] = (64,64,0) # yellow with 25% brightness
    np0.write()
def np_off():
    for i in range(0, np0.n):
        np0[i] = (0,0,0)
    np0.write()

# sdcard cs 핀 설정
cs = machine.Pin(17, machine.Pin.OUT)

# sdcard spi 설정
spi = machine.SPI(0,
    baudrate = 100000,
    polarity = 0,
    phase = 0,
    firstbit = machine.SPI.MSB,
    sck = machine.Pin(18),
    mosi = machine.Pin(19),
    miso = machine.Pin(16)
)

# sdcard 초기화
sd = sdcard.SDCard(spi, cs)

# sdcard 마운트
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/SDCARD")

# 베터리 전압을 읽는 변수 초기화
batt_adc = machine.ADC(27)
VOLTAGE_DROP_FACTOR = 1

# 버튼 핸들러 함수
def button_handler(pin):
    global recording_active, file
    if pin.value() == 0:  # 버튼이 눌렸을 때
        recording_active = not recording_active
        if recording_active:
            print("recording active")
            np_blue()
            button_buzzer(2000)
            utime.sleep(0.1)
            np_off()
            file = open('01.csv', 'a')
        else:
            print("recording deactive")
            np_yellow()
            button_buzzer(2000)
            utime.sleep(0.1)
            np_off()
            if file:
                file.close()

# 부저를 울리는 함수
def button_buzzer(freq):
    buzzer.duty_u16(30000)
    buzzer.freq(freq)
    utime.sleep(0.1)
    buzzer.duty_u16(0)

# 부팅을 알리는 부저 소리
def start_buzzer():
    buzzer.freq(1000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.freq(2000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.freq(3000)
    buzzer.duty_u16(30000)
    utime.sleep(0.1)
    buzzer.duty_u16(0)

# 파일에 데이터를 기록하는 함수
def record_data():
    global file
    # 베터리 전압을 읽어서 data_line에 저장
    batt_adc_value = batt_adc.read_u16()
    batt_voltage = batt_adc_value * 3.3 / 65535 * VOLTAGE_DROP_FACTOR
    for rom in roms:
        temp_sensor.convert_temp()
        utime.sleep_ms(100)
        t = temp_sensor.read_temp(rom)
        dateTime = ds3231.get_time()
        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(dateTime[0], dateTime[1], dateTime[2], dateTime[3], dateTime[4], dateTime[5])
        data_line = "{}, {:6.2f}, {:6.2f}\n".format(timestamp, t, batt_voltage)
        #print(t)
        if file:
            file.write(data_line)
            #Led.value(1)
            utime.sleep(recording_interval)  # 사용자가 설정한 기록 간격에 따라 대기
            #Led.value(0)

# 버튼에 핸들러 등록
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_handler)

start_buzzer()
np_green()

while True:
    # 버튼 상태에 따라 LED 상태 변경
    if recording_active:
        Led.value(1)
    else:
        Led.value(0)
    if recording_active:
        record_data()

