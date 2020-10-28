#!/usr/bin/python
# -*- coding: utf-8 -*


import os, time
if os.name == 'nt':
    import GPIO_Dummy as GPIO
else:
    import RPi.GPIO as GPIO


class CPwmServoControl:
    def __init__(self):
        print("Start :", str(self))
        #self.InitGpio()

    def __del__(self):
        pass

    def InitServo(self, pin):
        self.pin_servo = pin

        #GPIO.setmode(GPIO.BOARD) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_servo, GPIO.OUT) 

        self.p = GPIO.PWM(self.pin_servo, 50)
        
        #print ("GPIO initialize", self.gpio_pin, self.gpio_dir)
        # self.p.start(0)
        

    def TEST_SERVO(self):

        self.p.start(0)            

        self.p.ChangeDutyCycle(3)  # 0
        time.sleep(1)

        self.p.ChangeDutyCycle(12) # 180
        time.sleep(1) 

        self.p.ChangeDutyCycle(7.5) # 90
        time.sleep(1)
    
    def SET_DOORLOCK(self, bLock):
        self.p.start(0)
        time.sleep(1)
        if bLock == True:
            self.p.ChangeDutyCycle(3)  # 0
        else:
            self.p.ChangeDutyCycle(7.5) # 90
        time.sleep(1)
        self.p.start(0)
            
            
    def APP_MAIN(self):
    
        self.InitServo(18)
        
        #self.TEST_SERVO()
        self.SET_DOORLOCK(True)
        time.sleep(2)
        self.SET_DOORLOCK(False)
        time.sleep(2)
        if os.name == 'nt':
            pass
            #self.EXEC_SOMETHING()
        else:
            try:
                pass
                #self.EXEC_SOMETHING()
            except Exception as e :
                import sys
                _, _ , tb = sys.exc_info()    # tb  ->  traceback object
                print ("EXCEPTION ###", e, "[{}]".format(__file__), "[{}]".format(tb.tb_lineno))

        self.p.stop()                

        GPIO.cleanup() 


if __name__ == "__main__":

    obj = CPwmServoControl()
    obj.APP_MAIN()
            
        
