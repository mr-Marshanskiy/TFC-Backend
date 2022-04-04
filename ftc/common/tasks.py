import pdb
from typing import List

from django.conf import settings
from pysendpulse.pysendpulse import PySendPulse

from sendpulse.models import Template, Logging
from ftc.celery import app


@app.task
def send_email(template_id: int, subject: str = None, to: List = None, variables: dict = None):
    template = Template.objects.get(id=template_id)
    proxy = PySendPulse(
        getattr(settings, 'SENDPULSE_ID'),
        getattr(settings, 'SENDPULSE_SECRET'),
        getattr(settings, 'SENDPULSE_STORAGE'),
        getattr(settings, 'SENDPULSE_ROOT')
    )
    if to is None:
        to_emails = [getattr(settings, 'EMAIL_ADMIN')]
    else:
        to_emails = to if getattr(settings, 'DEBUG') is False else [getattr(settings, 'EMAIL_ADMIN')]

    email = {
        'subject': subject if subject else template.theme,
        'from': {
            'name': getattr(settings, 'ROBOT_NAME'),
            'email': getattr(settings, 'ROBOT_EMAIL')
        },
        'to': [{'email': email} for email in to_emails],
        'template': {
            'id': template.id,
            'variables': variables,
        }
    }
    result = proxy.smtp_send_mail_with_template(email)

    Logging.objects.create(
        response_guid=result.get('id'),
        status=result.get('result'),
        template=template.id,
        subject=subject,
        sender=email.get('from').get('email'),
        recipient=email.get('to')[0],
        result=result,
    )
