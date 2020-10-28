#-*- coding:utf-8 -*-
"""

// GND --- 커먼단자(2번째다리)
// 2pin -- 220옴저항(빨빨갈) -- 1번다리 R
// 3pin -- 220옴저항(빨빨갈) -- 3번다리 G
// 4pin -- 220옴저항(빨빨갈) -- 4번다리 B


GPIO_LED_RED = 17
GPIO_LED_GREEN = 22
GPIO_LED_BLUE = 27

"""

import os, time
if os.name == 'nt':
    import GPIO_Dummy as GPIO
else:
    import RPi.GPIO as GPIO


class CRgbLedControl:
    def __init__(self):
        print("Start :", str(self))
        #self.initGpio()
        self.pin_red = 0
        self.pin_green = 0
        self.pin_blue = 0

    def __del__(self):
        pass

    def InitGpio(self, r, g, b):

        self.pin_red = r
        self.pin_green = g
        self.pin_blue = b

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_red,GPIO.OUT)
        GPIO.setup(self.pin_green,GPIO.OUT)
        GPIO.setup(self.pin_blue,GPIO.OUT)

        self.SetLED(0,0,0)


    def SetLED(self, red, green, blue):
        if red == True:
            GPIO.output(self.pin_red,True)
        else:
            GPIO.output(self.pin_red,False)

        if green == True:
            GPIO.output(self.pin_green,True)
        else:
            GPIO.output(self.pin_green,False)

        if blue == True:
            GPIO.output(self.pin_blue,True)
        else:
            GPIO.output(self.pin_blue,False)

    def APP_MAIN(self):
        self.InitGpio(17, 22, 27)

        while(True):
            self.SetLED(1,0,0)
            time.sleep(1)
            self.SetLED(0,1,0)
            time.sleep(1)
            self.SetLED(0,0,1)
            time.sleep(1)


if __name__ == "__main__":

    try:
        #while(True):
            obj = CRgbLedControl()
            obj.APP_MAIN()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    except Exception as e:
        print('EXCEPTION:', e)

    finally:
        GPIO.cleanup()
        print("EXIT:", str(obj))



