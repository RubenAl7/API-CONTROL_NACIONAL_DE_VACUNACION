from twilio.rest import Client

def sendSms(origin, msg, to):
    account_sid = os.environ.get('TWILIO_ID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    return client.messages.create(
        from_=origin,
        body=msg,
        to=to
    )
    