import logging

from infra.report.console_reporter_new import ConsoleReporter
from infra.report.report_portal_reporter import ReportPortalReporter


def add_logging_level(level_name: str, level_num: int, method_name: str = None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    # >>> add_logging_level('TRACE', logging.DEBUG - 5)
    # >>> logging.getLogger(__name__).setLevel("TRACE")
    # >>> logging.getLogger(__name__).trace('that worked')
    # >>> logging.trace('so did this')
    # >>> logging.TRACE
    5

    """
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError('{} already defined in logging module'.format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError('{} already defined in logging module'.format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError('{} already defined in logger class'.format(method_name))

    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


def invoke_if_exists(reporter, method_name, *args):
    if hasattr(reporter, method_name):
        method = getattr(reporter, method_name, None)
        if callable(method):
            try:
                method(*args)
            except Exception as e:
                print(f'Exception {e} while calling {method_name} in reporter {reporter}')


class ReportManager(object):
    class __ReportManager:
        def __init__(self):
            self.reporters = [ConsoleReporter(), ReportPortalReporter()]
            add_logging_level('TRACE', logging.DEBUG - 5, 'trace')

        def add_reporter(self, reporter):
            self.reporters.append(reporter)

        def info(self, message):
            for reporter in self.reporters:
                invoke_if_exists(reporter, "info", message)

        def debug(self, message):
            for reporter in self.reporters:
                invoke_if_exists(reporter, "debug", message)

        def warning(self, message):
            for reporter in self.reporters:
                invoke_if_exists(reporter, "warning", message)

        def error(self, message):
            for reporter in self.reporters:
                invoke_if_exists(reporter, "error", message)

        def image(self, image_name, description=None):
            for reporter in self.reporters:
                if hasattr(reporter, "image"):
                    method = getattr(reporter, "image", None)
                    if callable(method):
                        method(image_name, description)

        def file(self, file_name, description=None):
            for reporter in self.reporters:
                if hasattr(reporter, "file"):
                    method = getattr(reporter, "file", None)
                    if callable(method):
                        method(file_name, description)

        def end_run(self):
            for reporter in self.reporters:
                invoke_if_exists(reporter, "end_run")

        def start_test(self, nodeid: str, location):
            for reporter in self.reporters:
                invoke_if_exists(reporter, "start_test", nodeid, location)

        def end_test(self, nodeid: str, location):
            for reporter in self.reporters:
                invoke_if_exists(reporter, "end_test", nodeid, location)

        def test_status(self, nodeid: str, when: str, outcome: str, code: str, message: str):
            for reporter in self.reporters:
                invoke_if_exists(reporter, "test_status", nodeid, when, outcome, code, message)

    instance = None

    def __new__(cls): # __new__ always a classmethod
        if not ReportManager.instance:
            ReportManager.instance = ReportManager.__ReportManager()
        return ReportManager.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
