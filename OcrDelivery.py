

import os, time

from CCoolSms import CCoolSms
from CQrCode import CQrCode
from CCamera_Function import CCamera_Function

from CPwmServoControl import CPwmServoControl
from CRgbLedControl import CRgbLedControl
from CTesseractOcr import CTesseractOcr
from CADS1x15_ADConverter import CADS1x15_ADConverter

from imutils.video import VideoStream
import cv2
import CV_Utils

class OcrDelivery:
    def __init__(self):
        print("Start :", str(self))

        self.STR_NAME_NOTDETECTED = '인식불가'  
        self.ADC_THRESHOLD = 15000    

        self.mms = CCoolSms()
        self.qrcode = CQrCode()
        self.ccam = CCamera_Function()
        self.ocr = CTesseractOcr()
        self.doorlock = CPwmServoControl()
        self.doorlock.InitServo(18)
        self.led = CRgbLedControl()

        self.led.InitGpio(17, 22, 27)

        self.adc = CADS1x15_ADConverter()
        self.adc.InitAdc()

       
        if os.name == 'nt':
            self.vs = VideoStream(usePiCamera=False).start()
        else:
            self.vs = VideoStream(usePiCamera=True).start()
        if os.name != 'nt':
            time.sleep(3.0) 


    def __del__(self):
        if self.vs != None:
            self.vs.stop()

    def GeneratePassword(self):
        import random
        return random.randint(1, 9999)  

    def GenerateQrCodePassword(self):
        self.password = str(self.GeneratePassword()) 
        print("QR CODE PASSWORD: ", self.password )
        self.qrcode.TEST_QrCodeGen(str(self.password))

    def SEND_MMS(self, phone, name):
       

        message = "%s 고객님께 택배가 도착하였습니다. 전송된 QR코드를 카메라에 인식시키면 택배함이 열립니다."%name
        
        if os.name == 'nt':
            qrcode = 'qrpassword.png'
        else:
            qrcode = '/home/pi/capture_save/qrpassword.png'

       
        print("message : ", message)
        print("qrcode : ", qrcode)

        if True:  
            self.mms.SendMMS(phone, message, qrcode)
        else:
            print("didn't send mms for test")

    def getFrame(self, GetFrom="CAMERA"):
        if GetFrom == "IMAGE":
            import imutils
            img=cv2.imread("cam_qr_name4.jpg", 1)
            #img=cv2.imread("cam_crop.jpg", 1)
            img = imutils.resize(img, width=450) 
            return img
        else:
            frame = self.vs.read()
            return frame


    def isPhonenumber(self, number):
        import re
        regex= "\w{3}-\w{4}-\w{4}" # XXX-XXXX-XXXX

        if re.search(regex, number):
            # print("Valid phone number")
            return True
        else:
            # print("Invalid phone number")
            return False


    def SCAN_CUSTOMER_INFORMATION(self):

        
        ocr_phone = '010-2345-6787'
        ocr_name = '홍길동1'

        
        while(True):

            
            img = self.getFrame("CAMERA")

            import imutils
            

            result = self.qrcode.DetectQrcode(img)
            if result == "":
                
                continue

            else:
                print ("QR Code is Detected")
               
                (result_text, x, y, w, h, polygon) = result
                print(result_text)  
                print(x,y,w,h)      
                print(polygon)      

                
                if abs(x - polygon[0].x) > 10 or abs(y - polygon[0].y) > 10: 
                    print("new point")
                    polygon2 = [0,0,0,0]
                    polygon2[0] = polygon[3]
                    polygon2[1] = polygon[0]
                    polygon2[2] = polygon[1]
                    polygon2[3] = polygon[2]
                else:
                    polygon2 = polygon

                print("polygon1: ", polygon)
                print("polygon2: ", polygon2)

                img2 = CV_Utils.Transform(img, polygon2)



                result = self.ocr.ReadOcrPyTesseract(img2)
                print(result)

                

                result = result.split('\n')

                print (result)
                if len(result) > 1:
                    ocr_name = result[0]
                    ocr_phone = result[1]
                else:
                    ocr_name = self.STR_NAME_NOTDETECTED
                    ocr_phone = '인식불가'
                    continue

                
                cv2.imshow("Detecting", img)
                cv2.imshow("CROP", img2)

                
                cv2.waitKey(3000)
                cv2.destroyAllWindows()


                if not self.isPhonenumber(ocr_phone):
                    ocr_phone = result_text
                    print("OCR phone number is not valid. using QR Code Data")

                return ocr_phone, ocr_name
    def SCAN_BOX_SENSOR(self):

        while(True):

            adc = self.adc.GetAdcValue(0)
            print("sensor:", adc)
            if adc > self.ADC_THRESHOLD:
                print("POSTBOX is DETECTED")
                self.led.SetLED(0,1,0)  
                self.doorlock.SET_DOORLOCK(True)  
                break
            time.sleep(0.5)

    def SCAN_PASSQRCODE(self):

        print ("QR코드 스캔중..")

        while(True):
            img = self.getFrame("CAMERA")

            import imutils
            

            result = self.qrcode.DetectQrcode(img)

            if result == "":
                #print ("QR is not Detected")
                continue

            else:
                (result_text, x, y, w, h, polygon) = result
                print ("QR Code is Detected")
                if result_text.find(self.password) != -1:  
                    print("PASSWORD is MATCHED")
                    self.led.SetLED(1,0,0)             
                    self.doorlock.SET_DOORLOCK(False)  
                    return
                else:
                    print("PASSWORD is NOT MATCHED")



    def APP_MAIN(self):
        #1. 택배기사가 이름과 폰번호가 적힌 택배스티커를 파이캠에 OCR인식
        #2. QR코드 생성 및 해당 번호로 MMS 전송
        #3. 택배기사가 택배를 택배함에 넣을때까지 압력센서 스캔
        #4. 압력센서 인식으로 택배함 잠금
        #5. 사용자는 파이캠에 수신한 QR코드 비쳐서 잠금해제

        if os.name != 'nt':
            time.sleep(2.0) 


        
        while(True):

            # 초기 상태 설정
            self.doorlock.SET_DOORLOCK(False) 
            self.led.SetLED(0,0,1) 
            print("QR코드인식 대기중...")

            phone, name = self.SCAN_CUSTOMER_INFORMATION()
            self.GenerateQrCodePassword()
            self.SEND_MMS(phone, name)
            self.SCAN_BOX_SENSOR()
            self.SCAN_PASSQRCODE()


if __name__ == "__main__":

    try:
        obj = OcrDelivery()
        obj.APP_MAIN()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    except Exception as e:
        print('EXCEPTION:', e)

    finally:
        #GPIO.cleanup()
        print("EXIT:", str(obj))


