from typing import List, TypedDict, Union, Dict
from typing_extensions import NotRequired

from mailjet_rest import Client as MailerClient

class NotifMessage(TypedDict):
    """ A message to send to a list of recipients """
    subject: str
    mail_content: str
    recipient: str
    bcc_recipients: NotRequired[list[str]]
    sender: str
    app_name: str


class Client(MailerClient):
    def __init__(self, api_key=None, api_secret=None, version=None):
        super().__init__(auth=(api_key, api_secret), version=version)

    def send_to_recipients(
        self,
        recipients: List[Union[str, Dict]],
        subject: str,
        mail_content: str,
        sender: str,
        app_name: str,
        bcc_recipients: List[Union[str, Dict]] = []):
        """ Send one mail to a list of recipients """
        return self.send.create(data={
            'Messages': [
                {"From": {"Email": sender, "Name": f"{app_name} alerting"},
                "To": [{'Email': single_recipient}],
                "Bcc": bcc_recipients,
                "Subject": subject,
                "HTMLPart": mail_content}
                for single_recipient in recipients]
        })

    def send_bulk(
        self,
        messages: list[NotifMessage],
        ):
        """ Send one mail to a list of recipients """
        formated_messages = [{"From": {"Email": msg['sender'], "Name": f"{msg['app_name']} alerting"},
                              "To": [{'Email': msg['recipient']}],
                              "Bcc": msg.get('bcc_recipients', []),
                              "Subject": msg['subject'],
                              "HTMLPart": msg['mail_content']} for msg in messages]
        return self.send.create(data={
            'Messages': formated_messages
        })

