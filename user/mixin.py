from django.conf import settings
from twilio.rest import Client


def send_message(otp, phone_number):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            messaging_service_sid=settings.MESSAGING_SERVICE_SID, body=f"your otp is {otp}", to=phone_number
        )
        print(message.sid)
    except Exception as e:
        print(e)
