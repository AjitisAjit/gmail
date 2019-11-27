'''
pytest test configurations
'''

import os
import pytest


@pytest.fixture(scope='session')
def gmail_username():
    return os.environ.get('TEST_USERNAME', 'random_user')


@pytest.fixture(scope='session')
def gmail_password():
    return os.environ.get('TEST_PASSWORD', 'random_pass')
