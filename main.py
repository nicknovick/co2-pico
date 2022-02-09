import machine
import time
import ssd1306

tx_pin=machine.Pin(4)
rx_pin=machine.Pin(5)

sensor=machine.UART(1, baudrate=9600, bits=8, parity=None,stop=1,tx=tx_pin, rx=rx_pin)

i2c = machine.I2C(1,scl=machine.Pin(19), sda=machine.Pin(18))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def is_valid(buf):
        if buf is None or buf[0] != 0xFF or buf[1] != 0x86:
            return False
        i = 1
        checksum = 0x00
        while i < 8:
            checksum += buf[i] % 256
            i += 1
        checksum = ~checksum & 0xFF
        checksum += 1

while True:
    sensor.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')
    time.sleep(2)
    buf = sensor.read(9)
    if is_valid(buf) == False:
        oled.text("Wrong sensor value!", 0, 10)
        oled.show()
        break
    else:
        co2 = buf[2] * 256 + buf[3]
        text1="CO2 level:"
        text2=str(co2) + " PPM"
        oled.text(text1, 0, 20)
        oled.text(text2, 0, 40)
        oled.show()
        time.sleep(5)
        oled.fill(0)
        oled.show()