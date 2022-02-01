from time import time
import logging
import sys

import pytest

from pytest_reportportal import RPLogger, RPLogHandler


def timestamp():
    """Time for difference between start and finish tests."""
    return str(int(time() * 1000))


@pytest.fixture(scope="session")
def rp_logger(request):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create handler for Report Portal if the service has been
    # configured and started.
    if hasattr(request.node.config, 'py_test_service'):
        # Import Report Portal logger and handler to the test module.
        logging.setLoggerClass(RPLogger)
        rp_handler = RPLogHandler(request.node.config.py_test_service)
        # Add additional handlers if it is necessary
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
    else:
        rp_handler = logging.StreamHandler(sys.stdout)
    # Set INFO level for Report Portal handler.
    rp_handler.setLevel(logging.INFO)
    return logger


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
