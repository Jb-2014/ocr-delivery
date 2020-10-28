# vi:set sw=4 ts=4 expandtab:
# -*- coding: utf8 -*-

import sys

sys.path.insert(0, "../../")

from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


class CCoolSms:
    def __init__(self):
        print("Start :", str(self))

        # set api key, api secret
        self.api_key_eve = "NCSY3QIWB4PNKFLA"
        self.api_secret_eve = "EWWW38VRBSXZUXTA1NVTLKAB0679TCKD"

        self.api_key_client = "NCSPLMR7ZZSUI3YW"
        self.api_secret_client = "FUGTPR8GKU8QJQTSR1ROU6K84GKEKJCT"

        self.api_key = "NCSPLMR7ZZSUI3YW"
        self.api_secret = "FUGTPR8GKU8QJQTSR1ROU6K84GKEKJCT"


    def __del__(self):
        pass

    def TEST_SendSMS(self):  # 동작확인함
        ## 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
        params['to'] = '01051012648' # Recipients Number '01000000000,01000000001'
        params['from'] = '01064222974' # Sender number
        params['text'] = 'Test Message 테스트 메시지 api' # Message

        # Optional parameters for your own needs. more informations visit to http://www.coolsms.co.kr/SMS_API_v2#POSTsend
        # params["image"] = "desert.jpg" # image for MMS. type must be set as "MMS"
        # params["mode"] = "test" # 'test' 모드. 실제로 발송되지 않으며 전송내역에 60 오류코드로 뜹니다. 차감된 캐쉬는 다음날 새벽에 충전 됩니다.
        # params["delay"] = "10" # 0~20사이의 값으로 전송지연 시간을 줄 수 있습니다.
        # params["force_sms"] = "true" # 푸시 및 알림톡 이용시에도 강제로 SMS로 발송되도록 할 수 있습니다.
        # params["refname"] = "" # Reference name
        # params["country"] = "KR" # Korea(KR) Japan(JP) America(USA) China(CN) Default is Korea
        # params["sender_key"] = "5554025sa8e61072frrrd5d4cc2rrrr65e15bb64" # 알림톡 사용을 위해 필요합니다. 신청방법 : http://www.coolsms.co.kr/AboutAlimTalk
        # params["template_code"] = "C004" # 알림톡 template code 입니다. 자세한 설명은 http://www.coolsms.co.kr/AboutAlimTalk을 참조해주세요.
        # params["datetime"] = "20140106153000" # Format must be(YYYYMMDDHHMISS) 2014 01 06 15 30 00 (2014 Jan 06th 3pm 30 00)
        # params["mid"] = "mymsgid01" # set message id. Server creates automatically if empty
        # params["gid"] = "mymsg_group_id01" # set group id. Server creates automatically if empty
        # params["subject"] = "Message Title" # set msg title for LMS and MMS
        # params["charset"] = "euckr" # For Korean language, set euckr or utf-8
        # params["app_version] = "Python SDK v2.0" # 어플리케이션 버전

        cool = Message(self.api_key, self.api_secret)

        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

        sys.exit()


    def SendMMS(self, phone, message, image):
        ## 4 params(to, from, type, text) are mandatory. must be filled


        ## 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'mms' # Message type ( sms, lms, mms, ata )
        params['to'] = phone # Recipients Number '01000000000,01000000001'
        params['from'] = '01064222974' # Sender number
        params['text'] = message # Message
        params["image"] = image # image for MMS. type must be set as "MMS"


        cool = Message(self.api_key, self.api_secret)

        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

        # sys.exit()

    def TEST_OcrDelivery(self):
        name = '홍길동'
        #save QR CODE NUMBER
        message = "%s 고객님께 택배가 도착하였습니다. 전송된 QR코드를 카메라에 인식시키면 택배함이 열립니다."%name
        phone = '010-5101-2648'
        qrcode = '/home/pi/capture_save/phone_010-2345-6789.png'

        self.SendMMS(phone, message, qrcode)


if __name__ == "__main__":

    try:
        #while(True):
            obj = CCoolSms()
            obj.TEST_OcrDelivery()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    except Exception as e:
        print('EXCEPTION:', e)

    finally:
        #GPIO.cleanup()
        print("EXIT:", str(obj))


