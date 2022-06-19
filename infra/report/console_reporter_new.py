import os

from datetime import datetime as dt, datetime
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from definitions import root_dir
from infra.report.function_parser import FunctionParser


class ConsoleReporter(object):
    def __init__(self):
        self.screen_width = 210
        self.console = Console(record=True, width=self.screen_width)
        if not self.console.color_system:
            self.console = Console(color_system="windows", record=True, width=self.screen_width)
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
        self.console.rule(Text.styled(f'Test Start: {nodeid}', style='bold red'))
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
        # decorator = '=' * 20
        # self.debug(f'[cyan]{decorator} {when} {decorator}[/]')
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
        grid = Table().grid()
        log_time_w = 11
        log_type_w = 9
        log_meta_w = 30
        grid.add_column('Log Time', width=log_time_w)
        grid.add_column("Log Type", width=log_type_w)
        grid.add_column("Log Message", width=self.screen_width - (log_meta_w + log_type_w + log_time_w), overflow="fold")
        filename, line_no, locals = self.console._caller_frame_info(4)
        grid.add_column("Log Meta", width=log_meta_w, justify='right')

        grid.add_row(f'[cyan][{datetime.now().strftime("%H:%M:%S")}][/]',
                     f'[{color}]{level}[/]',
                     self.console.render_str(message, highlight=True),
                     f'{filename.rpartition(os.sep)[-1]}:{line_no}')
        self.console.print(grid)

