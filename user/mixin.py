from django.conf import settings
from twilio.rest import Client


def send_message(otp, phone_number):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            messaging_service_sid="MG859803b3a99454fddcd325a8546356a0", body=f"your otp is {otp}", to=phone_number
        )
        print(message.sid)
    except Exception as e:
        print(e)
