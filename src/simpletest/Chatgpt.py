
# ChatGPT API를 Rasberry pi pico w에서 micropython을 사용하여 원하는 모델로 텍스트 생성을 요청하고,
# OLED에 텍스트를 표시하고, 부저로 알림을 주는 코드입니다.
import json
import ujson
import network
import urequests
from machine import RTC, Pin, SoftI2C, PWM
import utime as time
import usocket as socket
import ustruct as struct
from time import sleep
import ssd1306

# 부저 설정
buzzer = PWM(Pin(22))

def play_buzzer():
    buzzer.freq(500)
    buzzer.duty_u16(32768)
    time.sleep(0.05)
    buzzer.duty_u16(0)

# OLED 설정
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def display_on_oled(text):
    oled.fill(0)
    max_line_length = 20 # 21 characters per line
    lines = []
    
    # 줄을 나누기 위해 텍스트를 max_line_length로 나눕니다.
    while len(text) > max_line_length:
        line = text[:max_line_length]
        lines.append(line)
        text = text[max_line_length:]
    lines.append(text) # 마지막 줄 추가 

    y = 0
    for line in lines:
        for i in range(0, len(line)):
            oled.text(line[:i+1], 0, y)
            oled.show()
            # 타자기 소리를 내기 위해 부저를 울립니다.
            if line[i] != ' ':
                play_buzzer()
            time.sleep(0.05) 
        y += 10

# Config 파일 로드
def load_config(filename):
    try: 
        with open(filename, 'r') as f:
            config = ujson.load(f)
            return config
    except OSError as e:
        print("Failed to load config file", filename)
        print(e)
        return None
    except ValueError as e:
        print("Failed to load config file", filename)
        print(e)
        return None

if __name__ == "__main__":
    config = load_config("secure_config.json")
    if config is None:
        raise RuntimeError("Failed to load config file")


# ChatGPT 설정
api_key = config['apikey'] 

def chat_gpt(ssid, password, endpoint, api_key, model, prompt, max_tokens):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config['wifi']['ssid'], config['wifi']['password'])
        
    max_wait = 100
    print('Waiting for connection')
    while max_wait > 10:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1    
        sleep(1)
    status = None
    if wlan.status() != 3:
        raise RuntimeError('Connections failed')
    else:
        status = wlan.ifconfig()
        print('connection to', ssid,'succesfull established!', sep=' ')
        print('IP-adress: ' + status[0])
    ipAddress = status[0]


    ## Begin formatting request
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + api_key}
    data = {"model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
    }

    print("Attempting to send Prompt")
    r = urequests.post("https://api.openai.com/v1/chat/completions",
                        json=data, 
                        headers=headers)

    if r.status_code >=300 or r.status_code <200:
        print("There was an error with the request \n" +
              "Response Status: " + str(r.text))
    else:
        print("Success")
        response_data = json.loads(r.text)
        completion = response_data['choices'][0]['message']['content']
        print("Completion: " + completion)
        display_on_oled(completion)
    r.close()

chat_gpt(config['wifi']['ssid'], 
         config['wifi']['password'], 
         "completions",
         config['apikey'],
         "gpt-3.5-turbo",
         # 프롬프트를 변경하여 다른 텍스트를 생성할 수 있습니다.
         "Proverb for teacher",
         100)

     