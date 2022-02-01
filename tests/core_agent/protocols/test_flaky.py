import logging

import pytest
import random

log = logging.getLogger('tests')


@pytest.mark.component("web")
@pytest.mark.os("linux")
def test_that_flakes0():
    log.info('Flaky test')
    if random.randint(0, 1):
        log.info('This time will fail')
        raise Exception("Failed by purpose")
    log.info('This time will pass')


@pytest.mark.component("web")
@pytest.mark.os("linux")
def test_that_flakes1():
    log.info('Flaky test')
    if random.randint(0, 1):
        log.info('This time will fail')
        raise Exception("Failed by purpose")
    log.info('This time will pass')


@pytest.mark.component("web")
@pytest.mark.os("linux")
def test_that_flakes2():
    log.info('Flaky test')
    if random.randint(0, 1):
        log.info('This time will fail')
        raise Exception("Failed by purpose")
    log.info('This time will pass')
