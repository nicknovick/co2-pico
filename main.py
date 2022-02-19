class Mhz19b:

    # initializes a new instance
    def __init__(self, rx_pin, tx_pin):
        self.uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, rx=rx_pin ,tx=tx_pin)

    # measure CO2
    def measure(self):
        while True:
            # send a read command to the sensor
            self.uart.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')

            # a little delay to let the sensor measure CO2 and send the data back
            utime.sleep_ms(20)
            
            # read and validate the data
            buf = self.uart.read(9)
            if self.is_valid(buf):
                break

            # retry if the data is wrong  
            print('error while reading MH-Z19B sensor: invalid data')
            print('retry ...')


        # make this operation
        co2 = buf[2] * 256 + buf[3]
        temperature = buf[4] - 40
        return [co2, temperature]

    # check data returned by the sensor 
    def is_valid(self, buf):
        if buf is None or buf[0] != 0xFF or buf[1] != 0x86:
            return False
        i = 1
        checksum = 0x00
        while i < 8:
            checksum += buf[i] % 256
            i += 1
        checksum = ~checksum & 0xFF
        checksum += 1
        return checksum == buf[8]


# Here starts the program
try:
    import usys
    import uio
    from machine import Pin, I2C, UART
    import utime
    import sh1106

    def blink():
        led.value(1)
        machine.lightsleep(1000)
        led.value(0)

    def cleanup():
        led.value(0)
        led_power.value(0)

    # Config for the LED to blink (Pin 25 for built-in green LED)
    led = Pin(25, Pin.OUT, value=0)
    co2_high = 700

    # Config for the CO2 sensor
    rx_pin = machine.Pin(5)  # use one of UART RX pin, provide the GPx number of the pin. Connect to a TX(!) Pin on the sensor
    tx_pin = machine.Pin(4)  # use one of UART TX pin, provide the GPx number of the pin. Connect to a RX(!) Pin on the sensor
    SensorCO2 = Mhz19b(rx_pin, tx_pin)

    # Config for the display
    led_power = Pin(18, Pin.OUT, value=1)                 # 3,3V for the display, switched on by deafult
    WIDTH  = 128                                          # oled display width
    HEIGHT = 64                                           # oled display height

    #Init display
    i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=200000)         # Init I2C using pins GP8 & GP9 (default I2C0 pins)
    machine.lightsleep(100)                                         # short delay to wait until the I2C port has finished activating
    #print("I2C Configuration: "+str(i2c))                      # Print I2C config
    oled = sh1106.SH1106_I2C(WIDTH, HEIGHT, i2c, rotate=180)    # Init oled display

    while True:
        reading = SensorCO2.measure()
        co2_reading = reading[0]
        temp_reading = reading[1]
        print("CO2 reading =", co2_reading, ", Temp =", temp_reading)
        
        # Clear the oled display in case it has junk on it.
        oled.fill(0)
        # Add the CO2 reading
        oled.text("CO2:  "+str(co2_reading), 1, 1)
        oled.text("Temp: "+str(temp_reading), 1, 20)
        if co2_reading > co2_high:
            oled.text("Lueften!", 1, 50)
        # Finally update the oled display so the image & text is displayed
        oled.show()
        if co2_reading > co2_high:
            blink()
        machine.lightsleep(2000)
except KeyboardInterrupt:
    cleanup()
    usys.exit(0)
except BaseException as e:
    buf = uio.StringIO()
    usys.print_exception(e, buf)
    s = buf.getvalue()
    print(s)

    year, month, mday, hour, minute, second, weekday, yearday = utime.localtime()
    filename = str(year) + str(month) + str(mday) + str(hour) + str(minute) + str(second) + "_exception.txt"
    file = open(filename, "w")
    file.write(s)
    file.close()
    cleanup()