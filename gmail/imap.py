'''
Read emails using imap
'''

import email
import contextlib
import imaplib

from . import exception, message


GMAIL_IMAP_HOST = 'imap.gmail.com'
GMAIL_IMAP_PORT = 993


@contextlib.contextmanager
def get_connection(
        username: str,
        password: str,
        host=GMAIL_IMAP_HOST,
        port=GMAIL_IMAP_PORT
):
    '''
    ARGS:
        username: Email user
        password: Email password
        host: IMAP email server address
        port: IMAP email server port

    Creates a connection object, authenticates and returns an instance to inbox
    connection.
    '''
    conn = None

    try:
        conn = connect(host, port)
        conn = authenticate(conn, username, password)
        yield conn
    finally:
        if conn is not None:
            conn.close()
            conn.logout()


def connect(host=GMAIL_IMAP_HOST, port=GMAIL_IMAP_PORT):
    '''
    ARGS:
         host: Hostname for the email server
         port: Port number for email server

    Connect to gnd return an instance of connection
    '''
    try:
        return imaplib.IMAP4_SSL(host, port)
    except Exception as err:
        raise exception.IMAPException(err)


def authenticate(conn, username, password):
    '''
    ARGS:
        conn: Instance of connection
        username: gmail username
        password: gmail password

    Authenticates user with gmail and returns an iterator mailboxes
    '''
    try:
        conn.login(username, password)
        response, _ = conn.select('INBOX')
    except Exception as err:
        raise exception.IMAPException(err)

    if response != 'OK':
        raise exception.IMAPException('An error occurred authenticating - {}'.format(response))

    return conn


def get_emails(connection, filters='ALL'):
    '''
    ARGS:
        connection: Connection instance for reading emails
        filters: A comma seperated string for filtering out emails
    RETURNS:
        A list of email messages

    Searches for emails based upon filter string passed as
    argument and returns a list of emails
    '''
    try:
        resp,  data = connection.search(None, filters)
    except Exception as err:
        raise exception.IMAPException(err)

    if resp != 'OK':
        raise exception.IMAPException('An error getting emails for filter  - {filters} - {resp}'.format(
            filters=filters,
            resp=resp
        ))

    ids = data[0].split()

    return _get_emails_from_ids(connection, ids)


def _get_emails_from_ids(connection, ids):
    email_list = []

    for id in ids:
        try:
            resp, data = connection.fetch(id, '(RFC822)')  # Allows reading emails
        except Exception as err:
            raise exception.IMAPException(err)

        if resp != 'OK':
            raise exception.IMAPException('An error occured reading email for ID - {id} - {resp}'.format(
                id=id,
                resp=resp
            ))

        message_str = data[0][1].decode('utf8')  # Based on the protocol, contains email data
        email_msg = email.message_from_string(message_str)
        mail = message.make_email_message(email_msg)
        email_list.append(mail)

    return email_list
