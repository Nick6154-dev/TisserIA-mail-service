import os
import logging
import asyncio
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


class EmailService:

    def __init__(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.environ.get('MAIL_API_KEY', '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')
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    async def send_email(self, email_model):
        loop = asyncio.get_event_loop()

        def send_email_sync():
            subject = email_model.subject
            sender = email_model.sender
            to = email_model.to
            html_content = email_model.html_content
            template_id = email_model.template_id
            params = email_model.params
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, sender=sender, subject=subject,
                                                           html_content=html_content,
                                                           template_id=template_id, params=params)
            try:
                print("Sending email..." + subject)
                return self.api_instance.send_transac_email(send_smtp_email)
            except ApiException as e:
                logging.debug("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

        api_response = await loop.run_in_executor(None, send_email_sync)
        logging.debug(api_response)
