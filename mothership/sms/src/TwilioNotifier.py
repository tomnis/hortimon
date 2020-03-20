import os
from twilio.rest import Client

class TwilioNotifier:
    """
    Exposes static methods for sending sms notifications.

    Assumes that the following environment variables are set:
        TWILIO_ACCOUNT_SID
        TWILIO_AUTH_TOKEN
        TWILIO_SENDER

    export TWILIO_ACCOUNT_SID=<id>
    export TWILIO_AUTH_TOKEN=<token>
    export TWILIO_SENDER=+15101234567
    """

    # Your Account SID from twilio.com/console
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # Your Auth Token from twilio.com/console
    auth_token  = os.environ['TWILIO_AUTH_TOKEN']

    sender = os.environ['TWILIO_SENDER']

    @classmethod
    def send_sms(self, to, body):
        """
        Sends an sms containing body to the number specified.
        """

        client = Client(TwilioNotifier.account_sid, TwilioNotifier.auth_token)
        message = client.messages.create(
            to=to, 
            from_= TwilioNotifier.sender,
            body=body)

        print("sent message to {0} with response id {1}".format(to, message.sid))
        return message
