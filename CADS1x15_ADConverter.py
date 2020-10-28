#!/usr/bin/python
# -*- coding: utf-8 -*

# Import the ADS1x15 module.

import os, time
if os.name != 'nt':
    import Adafruit_ADS1x15



if os.name == 'nt':
    import GPIO_Dummy as GPIO
else:
    import RPi.GPIO as GPIO


class CADS1x15_ADConverter:
    def __init__(self):
        print("Start :", str(self))
        #self.InitGpio()

    def InitAdc(self):
        if os.name == 'nt':
            # print("NT: InitAdc SKIP")
            return

        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = Adafruit_ADS1x15.ADS1115()

        # Or create an ADS1015 ADC (12-bit) instance.
        #adc = Adafruit_ADS1x15.ADS1015()

        # Note you can change the I2C address from its default (0x48), and/or the I2C
        # bus by passing in these optional parameters:
        #adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        self.GAIN = 1

        #print('Reading ADS1x15 values, press Ctrl-C to quit...')
        # Print nice channel column headers.
        #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        #print('-' * 37)

        
    def TEST_PrintAnalogValue(self):
        while True:
            # Read all the ADC channel values in a list.
            values = [0]*4
            for i in range(4):
                # Read the specified ADC channel using the previously set gain value.
                values[i] = self.adc.read_adc(i, gain=self.GAIN)
                # Note you can also pass in an optional data_rate parameter that controls
                # the ADC conversion time (in samples/second). Each chip has a different
                # set of allowed data rate values, see datasheet Table 9 config register
                # DR bit values.
                #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
                # Each value will be a 12 or 16 bit signed integer value depending on the
                # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
            # Print the ADC values.
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
            # Pause for half a second.
            time.sleep(0.5)
            
    def GetAdcValue(self, channel):
        if os.name == 'nt':
            # print("NT: GetAdcValue SKIP")
            return

        result = self.adc.read_adc(channel, gain=self.GAIN)
        return result

    def GetSoilHumidSensorValue(self, channel):
        if os.name == 'nt':
            # print("NT: GetSoilHumidSensorValue SKIP")
            return
        result = self.adc.read_adc(channel, gain=self.GAIN)
        
        # soid humid sensor test value = nowater 32767, full water = 11000
        
        result = 32768 - result # 0~ 21000
        
        result = result / 210  # 0~100
        if result < 0: result = 0
        if result > 100: result = 100
        return round(result, 1)
    

    def __del__(self):
        pass
       

    def APP_MAIN(self):
        self.InitAdc()
        try:
            #self.TEST_PrintAnalogValue()
            while(True):
                #print(self.GetSoilHumidSensorValue(0))
                print(self.GetAdcValue(0))
                time.sleep(.5)
        except Exception as e :
            import sys
            _, _ , tb = sys.exc_info()    # tb  ->  traceback object
            print ("EXCEPTION ###", e, "[{}]".format(__file__), "[{}]".format(tb.tb_lineno))



if __name__ == "__main__":

    obj = CADS1x15_ADConverter()
    obj.APP_MAIN()
            
        
        