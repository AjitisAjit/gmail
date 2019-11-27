'''
Test parsing emails
'''

import pytest
import datetime
from email import message
from gmail import message as gmail_message


@pytest.fixture(scope='function')
def email_object():
    msg = message.EmailMessage()
    msg['From'] = 'sender'
    msg['To'] = 'reciever'
    msg['Subject'] = 'subject'
    msg['Date'] = datetime.datetime.now()
    msg.set_content('Body')
    return msg


def test_email_constructor(email_object):
    message = gmail_message.make_email_message(email_object)
    assert message
