from brynq_sdk_brynq import BrynQ
import os
import mandrill
import codecs
import base64
from typing import Union, List, Optional, BinaryIO, Literal


class MailClient(BrynQ):
    def __init__(self, system_type: Optional[Literal['source', 'target']] = None, debug=False):
        # This is built in so you can use this class as a query generator for the BrynQ Agent
        super().__init__()
        self.debug = debug
        try:
            credentials = self.interfaces.credentials.get(system="mandrill", system_type=system_type)
            credentials = credentials.get('data')
            self.api_token = credentials['token']
            self.email_from = 'support@brynq.com' if credentials['email_from'] is None else credentials['email_from']
            self.name_from = 'BrynQ' if credentials['name_from'] is None else credentials['name_from']
            if self.debug:
                print('Retrieved credentials from BrynQ')
        except ValueError as e:
            print("No authorization found connected to interface, falling back to environment variables")
            self.api_token = None


        if self.api_token is None:
            if os.getenv("MANDRILL_TOKEN") is not None:
                self.api_token = os.getenv("MANDRILL_TOKEN")
                self.email_from = 'connect@salure.nl' if os.getenv("MANDRILL_EMAIL_FROM") is None else os.getenv("MANDRILL_EMAIL_FROM")
                self.name_from = 'BrynQ' if os.getenv("MANDRILL_NAME_FROM") is None else os.getenv("MANDRILL_NAME_FROM")
                if self.debug:
                    print('Retrieved credentials from environment variables')
            else:
                raise ValueError('No credentials found for Mandrill. Either authorize Mandrill to your interface in BrynQ or set the environment variables MANDRILL_TOKEN, MANDRILL_EMAIL_FROM and MANDRILL_NAME_FROM')

    def send_mail(self, email_to: list, subject: str, language='NL', content:  Optional[str] = None, attachment: Optional[BinaryIO | List[BinaryIO]] = None, cc: Optional[List | str] = None) -> List[dict]:
        """
        Send a mail with the BrynQ layout and using mandrill
        :param email_to: a list with name and mailadress to who the mail must be send
        :param subject: The subject of the email
        :param language: Determines the salutation and greeting text. For example Beste or Dear
        :param content: The message of the email
        :param attachment: The attachment/attachments of an email loaded as binary file (NOT the location of the file)
        :param cc: A list with name and mail address to be CC'd
        :return: If the sending of the mail is successful or not
        """

        mandrill_client = mandrill.Mandrill(self.api_token)
        # Load the html template for e-mails
        html_file_location = '{}/templates/mail_brynq.html'.format(os.path.dirname(os.path.abspath(__file__)))
        html_file = codecs.open(html_file_location, 'r')
        html = html_file.read()
        if language == 'NL':
            salutation = 'Beste '
            greeting_text = 'Met vriendelijke groet'
        else:
            salutation = 'Dear '
            greeting_text = 'Kind regards'

        # Process attachments
        encoded_attachments = []
        if attachment is not None:

            # add single attachment to a list
            if not isinstance(attachment, list):
                attachment = [attachment]

            for file in attachment:
                opened_attachment = file.read()
                encoded_attachments.append({
                    'content': base64.b64encode(opened_attachment).decode('utf-8'),
                    'name': file.name.split('/')[-1]
                })

        # Prepare CC list
        cc_list = []
        if cc is not None:
            for cc_object in cc:
                cc_list.append({
                    'email': cc_object['mail'],
                    'name': cc_object['name'],
                    'type': 'cc'
                })

        # Pick the configurations from the config file and create the mail
        response = []
        for email_object in email_to:
            if self.debug:
                print(f"Sending mail to: {email_object['mail']}")
            new_html = html.replace('{', '{{'). \
                replace('}', '}}'). \
                replace('{{subject}}', '{subject}'). \
                replace('{{title}}', '{title}'). \
                replace('{{salutation}}', '{salutation}'). \
                replace('{{name}}', '{name}'). \
                replace('{{content}}', '{content}'). \
                replace('{{greeting}}', '{greeting}').format(subject=subject, title=subject, salutation=salutation, name=email_object['name'], content=content, greeting=greeting_text)
            mail = {
                'from_email': self.email_from,
                'from_name': self.name_from,
                'subject': subject,
                'html': new_html,
                'to': [{'email': email_object['mail'],
                        'name': email_object['name'],
                        'type': 'to'}] + cc_list  # Add CC recipients
            }

            if encoded_attachments:
                mail['attachments'] = encoded_attachments

            # Send the mail and return the result per mail address
            result = {
                'Send to': email_object,
                'result': mandrill_client.messages.send(mail, False, 'Main Pool')
            }
            response.append(result)

        return response
