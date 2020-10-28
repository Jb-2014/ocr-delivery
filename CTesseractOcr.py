#-*- coding:utf-8 -*-

import os, time


import pytesseract
from PIL import Image
import cv2


class CTesseractOcr:
    def __init__(self):
        print("Start :", str(self))

    def __del__(self):
        pass

    # 검증안됨
    def PreProcessForTesseract(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        #image = cv2.medianBlur(image, 10)
        return image


    def ReadOcrPyTesseract(self, img):
        # for reference
        # print(pytesseract.image_to_string(Image.open('english.png')))
        # print(pytesseract.image_to_string(Image.open('sinsinpas.jpg'), lang='Hangul'))
        # print(pytesseract.image_to_string(Image.open('sinsinpas.jpg'), lang='kor'))
        #result = pytesseract.image_to_string(img, lang='kor')
        #result = pytesseract.image_to_string(img, lang='eng')
        #result = pytesseract.image_to_string(img, lang='Hangul')
                
        #original = pytesseract.image_to_string(gray, config='', lang='kor')


        result = pytesseract.image_to_string(img, lang='kor')
        #result = pytesseract.image_to_string(img, config='-l kor --oem 3 --psm 12')
        #print(result)
        return result


    # Tesseract 실행 예제
    def TEST_OCR(self):

        img=cv2.imread("helloworld_qrcode.png")
        self.ReadOcrPyTesseract(img)



if __name__ == "__main__":

    try:
        #while(True):
            obj = CTesseractOcr()
            obj.TEST_OCR()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    except Exception as e:
        print('EXCEPTION:', e)

    finally:
        #GPIO.cleanup()
        print("EXIT:", str(obj))


