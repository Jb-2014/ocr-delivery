#!/usr/bin/python
# -*- coding: utf-8 -*

import cv2

def rotate_img(src, angle=90):
    height, width, channel = src.shape
    matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
    dst = cv2.warpAffine(src, matrix, (width, height))
    return dst

def frame_flip(frame):
    frame = cv2.flip(frame, 0)  # 0:updown 1:left right

def image_resize(img, width):
    import imutils
    img = imutils.resize(img, width=width) # debug
    return img

def image_crop(img):
    #src = cv2.imread("Image/pawns.jpg", cv2.IMREAD_COLOR)
    # dst = img.copy()
    dst = img[0:100, 80:230]
    # roi = img[100:600, 200:700]
    # dst[0:100, 0:300] = roi

    return dst
    # cv2.imshow("src", src)
    # cv2.imshow("dst", dst)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def Transform(img, polygon):

    # 기울어진 이미지를 똑바로 보정하기
    # http://blog.naver.com/PostView.nhn?blogId=samsjang&logNo=220504966397&redirect=Dlog&widgetTypeCall=true

    import numpy as np

    # print(polygon)      # [Point(x=547, y=424), Point(x=559, y=885), Point(x=1087, y=839), Point(x=1043, y=388)] 좌상, 좌하, 우하, 우상

    #cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)  #사각형 범위
    cv2.line(img, (polygon[0].x, polygon[0].y), (polygon[1].x, polygon[1].y), (255,0,0), 2)
    cv2.line(img, (polygon[1].x, polygon[1].y), (polygon[2].x, polygon[2].y), (255,0,0), 2)
    cv2.line(img, (polygon[2].x, polygon[2].y), (polygon[3].x, polygon[3].y), (255,0,0), 2)
    cv2.line(img, (polygon[3].x, polygon[3].y), (polygon[0].x, polygon[0].y), (255,0,0), 2)


    extend_x = polygon[3].x + (polygon[3].x - polygon[0].x) *3  # 우상
    extend_y = polygon[3].y + (polygon[3].y - polygon[0].y) *3  # 우상

    extend2_x = polygon[2].x + (polygon[2].x - polygon[1].x) *3 # 우하
    extend2_y = polygon[2].y + (polygon[2].y - polygon[1].y) *3  # 우하

    cv2.line(img, (polygon[0].x, polygon[0].y), (extend_x, extend_y), (255,255,0), 2)
    cv2.line(img, (polygon[1].x, polygon[1].y), (extend2_x, extend2_y), (255,255,0), 2)

    h, w = img.shape[:2]


    crop_width = extend_x - polygon[0].x
    crop_height = extend_y - polygon[0].y

    #crop_height += 100
    print (h,w)
    print (extend_x, extend_y)
    print (extend2_x, extend2_y)
    print (crop_width, crop_height)
    pts1 = np.float32([[polygon[0].x, polygon[0].y], [extend_x, extend_y], [polygon[1].x, polygon[1].y], [extend2_x, extend2_y]])

    pts2 = np.float32([[0, 0], [300, 0], [0, 100], [300, 100]])
    # pts2 = np.float32([[0, 0], [crop_width, 0], [0, crop_height], [crop_width, crop_height]])


    M = cv2.getPerspectiveTransform(pts1, pts2)

    img2 = cv2.warpPerspective(img, M, (w, h))
    img2 = image_crop(img2)

    return img2




def image_open_show_basic():
    import cv2
    import imutils

    img=cv2.imread("cam_qr_name4.jpg", 1)
    #img=cv2.imread("cam_crop.jpg", 1)
    img = imutils.resize(img, width=450) # debug

    # show the frame
    cv2.imshow("Detecting", img)
    # cv2.imshow("trans", img2)

    # cv2.imshow('original', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    """
    key = cv2.waitKey(1) & 0xFF

    while(1):
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print("Quit")
            break
    """


def TEST_image_open_show():
    import cv2
    import imutils
    from CQrCode import CQrCode
    from CCamera_Function import CCamera_Function
    from CTesseractOcr import CTesseractOcr
    ocr = CTesseractOcr()
    cc = CCamera_Function()
    qr = CQrCode()

    img=cv2.imread("cam_qr_name4.jpg", 1)
    #img=cv2.imread("cam_crop.jpg", 1) 
    img = imutils.resize(img, width=450) # debug



    result = qr.DetectQrcode(img)
    if result == "":
        print ("QR is not Detected")
    
    else:
        #print(result)      #('Hello World!', 40, 40, 210, 210)
        (result_text, x, y, w, h, polygon) = result
        print(result_text)  # 'Hello World!'
        print(x,y,w,h)      # '40 40 210 210'
        print(polygon)      # [Point(x=547, y=424), Point(x=559, y=885), Point(x=1087, y=839), Point(x=1043, y=388)] 좌상, 좌하, 우하, 우상


        img2 = Transform(img, polygon)

    # show the frame
    cv2.imshow("Detecting", img)
    cv2.imshow("trans", img2)

    result = ocr.ReadOcrPyTesseract(img2)
    print(result)

    # result = 'a'

    result = result.split('\n')

    print (result)
    if len(result) == 2:
        ocr_name = result[0]
        ocr_phone = result[1]
    else:
        ocr_name = '인식불가'
        ocr_phone = '인식불가'

    # cv2.imshow('original', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    """
    key = cv2.waitKey(1) & 0xFF

    while(1):
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print("Quit")
            break
    """



if __name__ == "__main__":
    # image_open_show_basic()
    TEST_image_open_show()