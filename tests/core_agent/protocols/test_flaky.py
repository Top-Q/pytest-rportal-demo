import logging

import pytest
import random

log = logging.getLogger('tests')


@pytest.mark.component("web")
@pytest.mark.os("linux")
def test_that_flakes0(report):
    report.info('Flaky test')
    if random.randint(0, 1):
        report.info('This time will fail')
        raise Exception("Failed by purpose")
    report.info('This time will pass')


@pytest.mark.component("web")
@pytest.mark.os("linux")
def test_that_flakes1(report):
    report.info('Flaky test')
    if random.randint(0, 1):
        report.info('This time will fail')
        raise Exception("Failed by purpose")
    report.info('This time will pass')


@pytest.mark.component("web")
@pytest.mark.os("linux")
def test_that_flakes2(report):
    report.info('Flaky test')
    if random.randint(0, 1):
        report.info('This time will fail')
        raise Exception("Failed by purpose")
    report.info('This time will pass')
