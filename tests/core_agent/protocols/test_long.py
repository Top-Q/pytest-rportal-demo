import logging
import time
log = logging.getLogger('tests')


def test_long():
    log.info('About to go to sleep. zzzz')
    time.sleep(5)