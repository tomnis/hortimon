import os
from twilio.rest import Client

class TwilioNotifier:
    """
    Exposes static methods for sending sms notifications.

    Assumes that the following environment variables are set:
        twilio_account_sid
        twilio_auth_token
        twilio_sender

    export twilio_account_sid=<id>
    export twilio_auth_token=<token>
    """

    # Your Account SID from twilio.com/console
    account_sid = os.environ['twilio_account_sid']
    # Your Auth Token from twilio.com/console
    auth_token  = os.environ['twilio_auth_token']

    sender = os.environ['twilio_sender']

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
