from kavenegar import *

def send_otp_code(phone_number, code):

    try:
        api = KavenegarAPI('3962506778616E4E436E6D54473276662B462B674256666C595036736566726F7A33376C72565A546242343D')
        params = {
            'sender': '',#optional
            'receptor': phone_number,#multiple mobile number, split by comma
            'message': f'{code}کد تایید شما',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)

