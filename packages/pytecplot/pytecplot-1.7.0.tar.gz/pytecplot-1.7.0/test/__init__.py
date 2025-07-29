LATEST_SDK_VERSION = (2025, 2)

import argparse
import logging
import os
import sys
import unittest

from . import patch_pylibs
from .util import *


### Mock out DLL if all we are going to do is list out test cases
parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=False)
parser.add_argument('-l', '--list',action='store_true',
    help='''just list out the test cases, but do not run them.''')
args,_ = parser.parse_known_args(sys.argv)
if args.list:
    patch_tecplot_module()


def main():
    logging.basicConfig()

    parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
    parser.add_argument(
        '-r', '--random', action='store_true',
        help='''randomize ordering of test cases and further randomize
                test methods within each test case''')
    parser.add_argument('-d', '--debug', action='store_true',
        help='''Set logging output to DEBUG''')
    parser.add_argument('-i', '--info', action='store_true',
        help='''Print DEBUG logging output only during initial import of tecplot''')
    parser.add_argument('-l', '--list', action='store_true',
        help='''just list out the test cases, but do not run them.''')
    parser.add_argument('-c', '--connect', action='store_true',
        help='''connect to a running instance of Tecplot 360.''')
    parser.add_argument('-p', '--port', type=int, default=7600,
        help='''port to use when connecting to the TecUtil Server.''')

    def print_help(parser=parser):
        try:
            unittest.main(argv=[sys.argv[0], '--help'])
        except SystemExit:
            parser._print_help()
            sys.exit(0)

    parser._print_help = parser.print_help
    parser.print_help = print_help
    args,unknown_args = parser.parse_known_args(sys.argv)

    if args.debug:
        logging.root.handlers[0].stream = sys.stdout
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.handlers[0].stream = open(os.devnull, 'w')

    if args.list:

        def list_of_tests(tests):
            if unittest.suite._isnotsuite(tests):
                yield tests
            else:
                for test in tests._tests:
                    for t in list_of_tests(test):
                        yield t

        here = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
        tests = unittest.defaultTestLoader.discover('test',
            top_level_dir=os.path.dirname(here))

        tests = sorted(set([str(t) for t in list_of_tests(tests)]))
        tests = [str(t).replace(' (','-').replace(')','') for t in tests]

        for test in tests:
            fnname, namespace = test.split('-')
            if re.search(r'test\.examples\.', namespace):
                continue
            if platform.system() == 'Windows':
                if re.search(r'captured_output', namespace):
                    continue
            print(test)

    else:
        if args.info and not args.debug:
            logging.root.handlers[0].stream = sys.stdout
            logging.root.setLevel(logging.DEBUG)

        logging.debug('PATH:')
        for p in os.environ['PATH'].split(os.pathsep):
            logging.debug('    ' + p)

        if platform.system() == 'Linux':
            logging.debug('LD_LIBRARY_PATH:')
            for p in os.environ.get('LD_LIBRARY_PATH', '').split(os.pathsep):
                logging.debug('    ' + p)
        elif platform.system() == 'Darwin':
            logging.debug('DYLD_LIBRARY_PATH:')
            for p in os.environ.get('DYLD_LIBRARY_PATH', '').split(os.pathsep):
                logging.debug('    ' + p)

        import tecplot as tp
        if args.connect:
            tp.session.connect(port=args.port, timeout=600, quiet=True)
            if not args.debug:
                tp.session._tecutil_connector.client.processing_mode = \
                    tp.constant.TecUtilServerProcessingMode.Unspecified
            tp.new_layout()
        else:
            tp.session._tecutil_connector.start()

        if args.info and not args.debug:
            logging.root.handlers[0].stream = open(os.devnull, 'w')
            logging.root.setLevel(logging.WARNING)

        try:
            if args.random:
                unittest.defaultTestLoader.sortTestMethodsUsing = \
                    lambda *a: random.choice((-1,1))
                def suite_init(self,tests=()):
                    self._tests = []
                    self._removed_tests = 0
                    if isinstance(tests, list):
                        random.shuffle(tests)
                    self.addTests(tests)
                unittest.defaultTestLoader.suiteClass.__init__ = suite_init

            from unittest.runner import TextTestResult

            class TimeLoggingTestResult(TextTestResult):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.test_timings = []

                def startTest(self, test):
                    self._test_started_at = time.time()
                    super().startTest(test)

                def addSuccess(self, test):
                    elapsed = time.time() - self._test_started_at
                    num = len(self.test_timings)
                    name = self.getDescription(test)
                    self.test_timings.append((num, name, elapsed))
                    super().addSuccess(test)

            if __debug__:
                SLOW_TEST_THRESHOLD = 5 if args.connect else 1
            else:
                SLOW_TEST_THRESHOLD = 1 if args.connect else 0.5

            class TimeLoggingTestRunner(unittest.TextTestRunner):
                def __init__(self, slow_test_threshold=SLOW_TEST_THRESHOLD,
                             *args, **kwargs):
                    self.slow_test_threshold = slow_test_threshold
                    return super().__init__(resultclass=TimeLoggingTestResult,
                                            *args, **kwargs)

                def run(self, test):
                    result = super().run(test)
                    timings = list(filter(lambda item: item[2] > self.slow_test_threshold,
                                          result.test_timings))
                    if timings:
                        self.stream.writeln(
                            "\nSlow Tests (>{:.03f}s):".format(
                                self.slow_test_threshold))
                        for num, name, elapsed in timings:
                            if elapsed > self.slow_test_threshold:
                                self.stream.writeln(
                                    "({:.03f}s) {} {}".format(
                                        elapsed, num, name))
                    else:
                        self.stream.writeln(
                            '\nAll tests ran within {:.03f} s'.format(
                                self.slow_test_threshold))
                    return result

            # ensure we exit with the status of the tests and avoid failing
            # if the SDK crashed on exit (which happens in macos VMs)
            if platform.system() == 'Darwin':
                try:
                    # unittest.main() got exit=False option in python 3.1
                    # we use try/except here to allow for python 2.7
                    unittest.main(argv=unknown_args, testRunner=TimeLoggingTestRunner)
                except SystemExit as e:
                    os._exit(e.code)
            else:
                unittest.main(argv=unknown_args, testRunner=TimeLoggingTestRunner)

        finally:
            if args.connect:
                tp.session.disconnect()
            if platform.system() != 'Darwin':
                tp.session.stop()
