import logging

from django.conf import settings

from boto3.session import Session
from botocore.exceptions import ClientError


def send_email(source='', to_addresses=None, reply_addresses=None, subject='', body='', email_format='html'):
    session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    client = session.client('ses', region_name='us-east-1')

    to_addresses = to_addresses or []
    reply_addresses = reply_addresses or []

    try:
        response = client.send_email(
            Source=source,
            Destination={
                'ToAddresses': to_addresses,
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Html' if email_format == 'html' else 'Text': {
                        'Data': body
                    }
                }
            },
            ReplyToAddresses=reply_addresses,
        )
    except ClientError as e:
        logging.error('There was a problem sending email from {} to {}'.format(source, to_addresses))
        raise e
