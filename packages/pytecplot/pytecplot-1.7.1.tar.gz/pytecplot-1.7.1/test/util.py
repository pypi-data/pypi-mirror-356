import collections
import contextlib
import functools
import os
import platform
import re
import tempfile
import time
import unittest
import warnings

from unittest.mock import patch, Mock, PropertyMock

from .hide_modules import hide_modules


class AutoAttr:
    def __call__(self, *args, **kwargs):
        pass
    def __getattr__(self, attr):
        return self


@contextlib.contextmanager
def patched_tecplot_module():
    patches = []

    # patch for all platforms
    patches.append(patch('ctypes.cdll.LoadLibrary',
                         Mock(return_value=AutoAttr())))

    # patch for darwin
    if platform.system() == 'Darwin':
        from ctypes.util import find_library
        find_library_orig = find_library
        def find_library_mock(name):
            if re.search(r'tecutilbatch', name):
                return '/path/to/file'
            else:
                return find_library_orig(name)
        patches.append(patch('ctypes.util.find_library',
                                  Mock(side_effect=find_library_mock)))

    # patch for windows
    if platform.system() == 'Windows':
        path_exists_orig = os.path.exists
        def path_exists_mock(name):
            if re.search(r'tecutilbatch', name):
                return True
            else:
                return path_exists_orig(name)
        patches.append(patch('os.path.exists',
                                  Mock(side_effect=path_exists_mock)))

    for p in patches:
        p.start()

    yield patches

    for p in patches:
        p.stop()


def patch_tecplot_module():
    with patched_tecplot_module():
        import tecplot
        tecplot.sdk_version_info = (9999, 9999, 9999)


@contextlib.contextmanager
def closed_tempfile(suffix=''):
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as fout:
        try:
            fout.close()
            yield fout.name
        finally:
            try:
                #print('removing', fout.name)
                os.remove(fout.name)
            except Exception as e:
                print(e)


### convenience methods for patching tecutil
def patch_tecutil(fn_name, **kwargs):
    import tecplot
    return patch.object(tecplot.tecutil._tecutil, fn_name, Mock(**kwargs))


@contextlib.contextmanager
def patched_tecutil(fn_name, **kwargs):
    with patch_tecutil(fn_name, **kwargs) as p:
        yield p


@contextlib.contextmanager
def mocked_sdk_version(*version):
    import tecplot
    _sdk_vinfo = tecplot.version.sdk_version_info
    try:
        if len(version) < 3:
            # extend version tuple to at least three numbers (appending 0's)
            version = tuple(list(version) + [0] * (3 - len(version)))
        tecplot.version.sdk_version_info = version
        yield
    finally:
        tecplot.version.sdk_version_info = _sdk_vinfo


@contextlib.contextmanager
def mocked_connected():
    import tecplot

    class TecUtilClient(Mock):
        host = 'localhost'

    class LocalStringList(list):
        def __init__(self, *args):
            super().__init__(args)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    class LocalArgList(collections.OrderedDict):
        def __init__(self, *args):
            super().__init__(args)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.connected',
               PropertyMock(return_value=True)):
        _client = tecplot.tecutil._tecutil_connector.client
        _sus = tecplot.tecutil._tecutil_connector.suspended
        _ArgList = tecplot.tecutil.ArgList
        _StringList = tecplot.tecutil.StringList
        try:
            tecplot.tecutil._tecutil_connector.client = TecUtilClient()
            tecplot.tecutil._tecutil_connector.suspended = True
            tecplot.tecutil._tecutil_connector._delete_caches = []
            tecplot.tecutil.ArgList = LocalArgList
            tecplot.tecutil.StringList = LocalStringList
            yield
        finally:
            tecplot.tecutil.StringList = _StringList
            tecplot.tecutil.ArgList = _ArgList
            delattr(tecplot.tecutil._tecutil_connector, '_delete_caches')
            tecplot.tecutil._tecutil_connector.suspended = _sus
            tecplot.tecutil._tecutil_connector.client = _client


@contextlib.contextmanager
def mocked_tuserver_version(ver):
    import tecplot
    with mocked_connected():
        class C:
            tuserver_version = ver
        _client = tecplot.tecutil._tecutil_connector.client
        tecplot.tecutil._tecutil_connector.client = C()
        try:
            _sus = tecplot.tecutil._tecutil_connector.suspended
            try:
                tecplot.tecutil._tecutil_connector.suspended = False
                yield
            finally:
                tecplot.tecutil._tecutil_connector.suspended = _sus
                pass
        finally:
            tecplot.tecutil._tecutil_connector.client = _client


# This will print out timing information for each TestCase
'''
@classmethod
def setUpClass(cls):
    cls.startTime = time.time()
@classmethod
def tearDownClass(cls):
    print("\n{}.{}: {:.3f}".format(cls.__module__, cls.__name__, time.time() - cls.startTime))
unittest.TestCase.setUpClass = setUpClass
unittest.TestCase.tearDownClass = tearDownClass
'''


def skip_windows():
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            if platform.system() != 'Windows':
                test_item(*args, **kwargs)
        return skip_wrapper
    return decorator


def skip_on(*ex):
    """
    Unconditionally skip a test on specfic exceptions
    """
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            if __debug__:
                try:
                    warnings.simplefilter('ignore')
                    test_item(*args, **kwargs)
                except ex:
                    raise unittest.SkipTest(str(ex[0]))
                finally:
                    warnings.simplefilter('default')
            else:
                import tecplot
                if tecplot.sdk_version_info < LATEST_SDK_VERSION:
                    raise unittest.SkipTest(str(ex[0]))
                else:
                    test_item(*args, **kwargs)
        return skip_wrapper
    return decorator


def skip_if_sdk_version_before(*ver, **kwargs):
    msg = kwargs.pop('msg', 'Added to SDK in {}')
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            import tecplot
            if tecplot.sdk_version_info < ver:
                raise unittest.SkipTest(msg.format('.'.join(str(x) for x in ver)))
            else:
                test_item(*args, **kwargs)
        return skip_wrapper
    return decorator


def skip_if_tuserver_version_before(ver, **kwargs):
    msg = kwargs.pop('msg', 'Added to TecUtil Server in version {}')
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            from tecplot.tecutil import _tecutil_connector
            if (
                _tecutil_connector.connected and
                _tecutil_connector.client.tuserver_version < ver
            ):
                raise unittest.SkipTest(msg.format(ver))
            else:
                test_item(*args, **kwargs)
        return skip_wrapper
    return decorator


def skip_if_connected(test_item):
    @functools.wraps(test_item)
    def skip_wrapper(*args, **kwargs):
        import tecplot
        if tecplot.tecutil._tecutil_connector.connected:
            raise unittest.SkipTest('Batch only')
        else:
            test_item(*args, **kwargs)
    return skip_wrapper


@contextlib.contextmanager
def assert_style(value, *svargs, **kwargs):
    once = kwargs.pop('once', True)
    with patch('tecplot.session.style.get_style', Mock()) as g, \
         patch('tecplot.session.style.set_style', Mock()) as s:
        yield
    if once:
        g.assert_called_once_with(type(value), *svargs, **kwargs)
        s.assert_called_once_with(value, *svargs, **kwargs)
    else:
        g.assert_called_with(type(value), *svargs, **kwargs)
        s.assert_called_with(value, *svargs, **kwargs)


@contextlib.contextmanager
def assert_warning(cls, expected_warning, num_expected):
    with warnings.catch_warnings(record=True) as w:
        yield
        if __debug__:
            cls.assertEqual(len(w), num_expected)
            cls.assertEqual(w[-1].category, expected_warning)
        else:
            cls.assertEqual(len(w), 0)
