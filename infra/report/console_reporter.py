import os
import traceback
import ntpath

from rich.syntax import Syntax
from rich.panel import Panel
from rich.console import Console
from datetime import datetime as dt
from definitions import root_dir
from infra.report.function_parser import FunctionParser


class ConsoleReporter(object):
    def __init__(self):
        self.console = Console(record=True)
        if not self.console.color_system:
            self.console = Console(color_system="windows", record=True)
        if not os.path.isdir(os.path.join(root_dir, 'reports')):
            os.mkdir(os.path.join(root_dir, 'reports'))
        self.filename = f'report-{dt.now().strftime("%H_%M_%S")}.html'
        ''' Since pytest is reporting the progress and status of tests we want avoid this to push our report 
         line so we have to keep track if this is the first log message and if so we will create an empty 
         log'''
        self.first_log_in_test = None

    def start_test(self, nodeid: str, location):
        self.first_log_in_test = True
        self.console.print(' ')
        self.console.print(Panel(f"Test: {location[2]}"), style="purple red", justify='left')

        file = os.path.join(root_dir, location[0])
        if os.path.isfile(file):
            content = None
            with open(file, 'r') as f:
                content = f.read()
            if not content:
                raise Exception(f'Failed to read content of file {file}')
            parser = FunctionParser(content, location[2]).parse()
            if parser.docstring():
                self.console.print(parser.docstring(), style='grey74')

    def info(self, message):
        self._log('INFO', 'white', message)

    def warning(self, message):
        self._log('WARNING', 'yellow', message)

    def debug(self, message):
        self._log('DEBUG', 'cyan', message)

    def error(self, message):
        self._log('ERROR', 'red', message)

    def image(self, image_name, description=None):
        self._log('INFO', 'white', f"File: '{image_name}' with description '{description}'")

    def file(self, file_name, description=None):
        self._log('INFO', 'white', f"File: '{file_name}' with description '{description}'")

    def test_status(self, nodeid: str, when: str, outcome: str, code: str, message: str):
        if 'failed' in outcome:
            self._log('ERROR', 'red', message)
            if code:
                syntax = Syntax(code, 'python', theme='ansi')
                self.console.print(syntax, width=140)

    def end_run(self):
        full_file_name = os.path.join(root_dir, 'reports', self.filename)
        if os.path.exists(full_file_name):
            os.remove(full_file_name)
        try:
            self.console.save_html(full_file_name)
        except Exception as e:
            print(f"Exception '{e}' while calling end run from ConsoleReporter")

    def _log(self, level, color, message):
        if self.first_log_in_test:
            ''' We want to avoid the first line interruption of pytest'''
            self.console.print(' ')
            self.first_log_in_test = False
        time = dt.now().strftime("%H:%M:%S")
        self.console.print(f'[blue][{time}][/] [{color}]{"{:<7}".format(level)} [/]', end=' ')
        if len(message) < 140:
            message = "{:<140}".format(message)
        # if '*' in message or '#' in message:
        #     self.console.print(Markdown(message), end=' ', soft_wrap=True)
        # else:
        self.console.print(message + '|', end='', soft_wrap=True)
        call_frame = None
        for frame in traceback.extract_stack():
            if not call_frame:
                call_frame = frame
                continue
            if 'report_manager.py' in frame.filename:
                break
            call_frame = frame
        self.console.print(f'{ntpath.basename(call_frame.filename).replace(".py","")}:{call_frame.name}:{call_frame.lineno}', style='grey78')
