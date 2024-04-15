# GPIO 연결  
## I2C (RTC / Light Sensor) 
### RTC
| RaspberryPi Pico W | DS3231 |
|-----------|------|
|   GP4     | SCL  |
|   GP5     | SDA  |

### Light Sensor
| RaspberryPi Pico W | BH1750 |
|-----------|------|
|   GP4     | SCL  |
|   GP5     | SDA  |

## SPI
| RaspberryPi Pico W | SDcard |
|-----------|------|
|   GP20    | MOSI |
|   GP19    | SCK  |
|   GP17    | SC   |
|   GP16    | MISO |
## One-Wire
| RaspberryPi Pico W| ds18b20 |
|-----------|------|
|   GP26    | DI   |
## NeoPixel 
| RaspberryPi Pico W | WS281B |
|-----------|------|
|   GP21    | LED  |

## Buzz 
| RaspberryPi Pico W | MLT-7525 |
|-----------|------|
|   GP22    | Buzz |

## Button
| RaspberryPi Pico W | TacktileSwitch |
|-----------|------|
|   GP20    | SW1 |

## ADC
| RaspberryPi Pico W | TacktileSwitch |
|-----------|------|
|   GP27    | BAT_DIV |



# [하드웨어 검증 코드](/src/simpletest/) 
- [Blink.py](/src/simpletest/Blink.py)
- [Button.py](/src/simpletest/Button.py)
- [Buzzer.py](/src/simpletest/Buzzer.py)
- [i2C.py](/src/simpletest/i2c.py)
- [Light.py](/src/simpletest/Light.py)
- [Neopixel.py](/src/simpletest/Neopixel.py)
- [RTC.py](/src/simpletest/RTC.py)
- [sd_test.py](/src/simpletest/sd_test.py)
- [Temp.py](/src/simpletest/Temp.py)








