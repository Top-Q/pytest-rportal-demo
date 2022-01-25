import logging

import pytest

log = logging.getLogger('api.endpoint')

@pytest.mark.component("agent")
@pytest.mark.os("windows")
def test_publish_to_portal(step):
    """
    This is the test description
    :param step:
    :return:
    """
    log.info("Some info message")
    with step('I\'m a [W]rapper!'):
        log.info('Nested message!')
        log.warning('Please leave')
    log.info('Info from test')