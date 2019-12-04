'''
Provides functionality for parsing email messages
'''

import email
import datetime
from typing import List
from dataclasses import dataclass

from . import exception


@dataclass(eq=True, frozen=True)
class Message:
    sender: str
    subject: str
    timestamp: datetime.datetime
    body: List


def make_email_message(email_message: email.message) -> Message:
    '''
    ARGS:
        email_message: An instance of email.message
    RETURNS:
        An instance of Email
    '''
    try:
        return Message(
            sender=email_message['From'],
            subject=email_message['Subject'],
            timestamp=parse_email_date(email_message['DATE']),
            body=parse_email_body(email_message)
        )
    except Exception as err:
        raise exception.MessageException(err)


def parse_email_body(email_message: email.message) -> List:
    '''
    ARGS:
        email_message: Instance of email.message
    RETURNS:
        List containing text of multipart message

    Parses email body and returns a list
    '''
    content = []
    for part in email_message.iter_parts():
        content.append(part.get_content())

    return content


def parse_email_date(email_date: str):
    '''
    ARGS:
        email_date: Email date as string
    RETURNS:
        Equivalent instance of datetime.datetime
    '''
    datetime_str = email_date.split(',')[1].split('-')[0].strip()
    datetime_str = datetime_str.split('+')[0].strip()   # Ignoring timezone if present
    datetime_obj = datetime.datetime.strptime(datetime_str, '%d %b %Y %H:%M:%S')
    return datetime_obj
