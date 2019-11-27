'''
exceptons.py
-----------------
Exception classes for mailbox
'''


class GmailException(Exception):
    '''
    Base class for all gmail exceptions
    '''
    pass


class MessageException(GmailException):
    '''
    Exceptions related to parsing and opening
    emails
    '''
    pass


class IMAPException(GmailException):
    '''
    Exceptions related to accessing email server, connecting
    and authenticating using IMAP
    '''
    pass
