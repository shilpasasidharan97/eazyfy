from django.conf import settings
from twilio.rest import Client 
import random



sid = 'ACb80999fdb3adb236ada4ee3700403ea2'
auth_token = '40df1ab4f59e468f4ffac3b42d122581'

class MessageHandler:
    phone_number = None
    otp = None

    def __init__(self,phone_number,otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_on_phone(self):
        client = Client(sid,auth_token)

        message = client.messages.create(
                                    messaging_service_sid='MG859803b3a99454fddcd325a8546356a0', 
                                    body=f'your otp is {self.otp}',
                                    to= self.phone_number
                                )

        print(message.sid)

