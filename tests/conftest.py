from time import time
import logging
import sys

import pytest
from _pytest.main import Session
from _pytest.reports import TestReport

# from pytest_reportportal import RPLogger, RPLogHandler

from infra.report.report_manager import ReportManager

from reportportal_client import RPLogger


@pytest.fixture(scope="session")
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)
    return logger


def timestamp():
    """Time for difference between start and finish tests."""
    return str(int(time() * 1000))




@pytest.fixture
def step(pytestconfig):
    if not hasattr(pytestconfig, 'py_test_service'):
        return

    pytest_service = pytestconfig.py_test_service
    rp_service = pytest_service.rp

    test_item_id = pytest_service.log_item_id

    class Step:
        def __init__(self, name):
            self.name = name
            self.step_id = None
            self.old_parent_id = None

        def __enter__(self):
            # Create a 'STEP' item
            self.step_id = rp_service.start_test_item(name=self.name,
                                                      start_time=timestamp(),
                                                      item_type='STEP',
                                                      has_stats=False,
                                                      parent_item_id=test_item_id)

            self.old_parent_id = pytest_service.parent_item_id

            pytest_service.log_item_id = self.step_id
            pytest_service.parent_item_id = self.step_id

        def __exit__(self, type, value, traceback):
            pytest_service.log_item_id = test_item_id
            pytest_service.parent_item_id = self.old_parent_id
            if type:
                status = 'FAILED'
            else:
                status = 'INFO'
            rp_service.finish_test_item(item_id=self.step_id,
                                        end_time=timestamp(),
                                        status=status)
            rp_service.terminate()

    yield Step

@pytest.hookimpl
def pytest_runtest_logstart(nodeid: str, location) -> None:
    """
    Creates end test event for the report manager
    :param nodeid:
    :param location:
    :return:
    """
    report = ReportManager()
    report.start_test(nodeid, location)


@pytest.hookimpl
def pytest_runtest_logfinish(nodeid: str, location) -> None:
    """
    Creates start test event for the report manager

    :param nodeid:
    :param location:
    :return:
    """
    report = ReportManager()
    report.end_test(nodeid, location)


@pytest.hookimpl
def pytest_runtest_logreport(report: TestReport):
    message = None
    if report.longrepr:
        message = report.longrepr.reprcrash.message
    ReportManager().test_status(report.nodeid, report.when, report.outcome,report.longreprtext, message)


@pytest.hookimpl
def pytest_sessionfinish(session: Session, exitstatus):
    ReportManager().end_run()


@pytest.fixture(scope="session")
def report():
    """
    Configures the report portal reporter and add it to the report manager
    :param request:
    :return: report manager
    """
    return ReportManager()
