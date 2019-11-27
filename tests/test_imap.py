'''
test_imap
'''

import imaplib
import datetime

import pytest

from gmail import imap, exception


def test_connect():
    connection = imap.connect()
    assert isinstance(connection, imaplib.IMAP4_SSL)


def test_authenticate(gmail_username, gmail_password):
    connection = imap.connect()
    auth = imap.authenticate(connection, gmail_username, gmail_password)
    assert auth


def test_get_emails(gmail_username, gmail_password):
    today = datetime.datetime.now().date().strftime('%d-%b-%Y')

    with imap.get_connection(gmail_username, gmail_password) as conn:
        emails = imap.get_emails(conn, '(ALL SINCE {})'.format(today))

    assert isinstance(emails, list)

    for e in emails:
        assert isinstance(e.subject, str)
        assert isinstance(e.sender, str)
        assert isinstance(e.timestamp, datetime.datetime)
        assert isinstance(e.body, list) and e.body


def test_connect_fail():
    with pytest.raises(exception.IMAPException):
        connection = imap.connect(host='unknown host', port=1000)
        assert connection


def test_authenticate_fail():
    connection = imap.connect()
    with pytest.raises(exception.IMAPException):
        auth = imap.authenticate(connection, 'fake username', 'fake_password')
        assert auth


def test_get_emails_fail(gmail_username, gmail_password):
    connection = imap.connect()
    imap.authenticate(connection, gmail_username, gmail_password)

    with pytest.raises(exception.IMAPException):
        emails = imap.get_emails(connection, 'UNKNOWN FILTER')
        assert emails
