#-*- coding:utf-8 -*-

import os, time

import numpy as np


class CQrCode:
    def __init__(self):
        print("Start :", str(self))

    def __del__(self):
        pass


    # QR코드 생성 예제
    def TEST_QrCodeGen(self, data):
    
        """
        #https://blog.naver.com/chandong83/221767329995
        > pip install qrcode[pil]
        or
        > pip install qrcode pillow  # rpi에서 이거로 설치함
        """

        import qrcode

        # Hello World! 로 QR 코드 생성
        img = qrcode.make(data)

        # 생성된 이미지를 helloworld_qrcode.png로 저장
        # img.save('/home/pi/capture_save/phone_%s.png'%phonenumber)  # rpi에서 동작확인함
        if os.name == 'nt':
            img.save('qrpassword.png')
        else:
            img.save('/home/pi/capture_save/qrpassword.png')
    
    # QR코드 읽기 예제(이미지 파일로 읽기)
    def TEST_QrCodeScan(self):
            
        #pip3 install pyzbar
        import pyzbar.pyzbar as pyzbar
        import cv2
        import imutils

        img=cv2.imread("cam_qr_name4.jpg", 1)
        #img=cv2.imread("cam_crop.jpg", 1) 
        img = imutils.resize(img, width=450) # debug
        result = self.DetectQrcode(img)
        if result == "":
            print ("QR is not Detected")
        
        else:
            #print(result)      #('Hello World!', 40, 40, 210, 210)
            (result_text, x, y, w, h, polygon) = result
            print(result_text)  # 'Hello World!'
            print(x,y,w,h)      # '40 40 210 210'
            print(polygon)      # [Point(x=547, y=424), Point(x=559, y=885), Point(x=1087, y=839), Point(x=1043, y=388)] 좌상, 좌하, 우하, 우상




        # show the frame
        # cv2.imshow("Detecting", img)
        # cv2.imshow("trans", img2)

        # cv2.imshow('original', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        """
        key = cv2.waitKey(1) & 0xFF

        while(1):
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                print("Quit")
                break
        """

    # QR코드 검출 : image frame
    def DetectQrcode(self, frame):
        #pip3 install pyzbar
        import pyzbar.pyzbar as pyzbar
        import cv2
    
        ret_str = ""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        decoded = pyzbar.decode(gray)

        for d in decoded:
            x, y, w, h = d.rect
            print(d.polygon)
            #print(x, y, w, h)

            barcode_data = d.data.decode("utf-8")
            barcode_type = d.type

            ret_str = barcode_data
        
            return ret_str, x, y, w, h, d.polygon
        return ""




if __name__ == "__main__":

    try:
        #while(True):
            obj = CQrCode()
            obj.TEST_QrCodeScan()
            # obj.TEST_QrCodeGen('010-2345-6789')
            
            
    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    except Exception as e:
        print('EXCEPTION:', e)

    finally:
        #GPIO.cleanup()
        print("EXIT:", str(obj))
        
        
        