import atexit
import datetime
import os
import pathlib
import platform
import sys
import unittest
import warnings

from contextlib import contextmanager
from datetime import date
from unittest.mock import patch, Mock, PropertyMock

from tecplot.exception import *
import tecplot as tp

from test import LATEST_SDK_VERSION, skip_if_sdk_version_before, skip_if_connected, mocked_connected
from ..sample_data import sample_data


@contextmanager
def patch_env(key, val=None):
    saved_val = os.environ.get(key, None)
    try:
        try:
            del os.environ[key]
        except KeyError:
            pass
        if val is not None:
            os.environ[key] = val
        yield
    finally:
        if saved_val is None:
            try:
                del os.environ['HOME']
            except KeyError:
                pass
        else:
            os.environ[key] = saved_val


class TestSession(unittest.TestCase):
    def test_tecplot_directories_are_pathlib_objs(self):
        self.assertIsInstance(tp.session.tecplot_install_directory(), pathlib.Path)
        self.assertIsInstance(tp.session.tecplot_examples_directory(), pathlib.Path)

    def test_examples_is_under_install(self):
        install_dir = tp.session.tecplot_install_directory()
        examples_dir = tp.session.tecplot_examples_directory()
        self.assertEqual(examples_dir, install_dir / 'examples')

    @skip_if_connected
    def test_tecplot_directories(self):
        mock_tec360_dir = '/path/to/tec360'
        if platform.system() == 'Darwin':
            mock_tec360_dir = mock_tec360_dir + '/Contents/MacOS'
        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.tecsdkhome',
                   PropertyMock(return_value=mock_tec360_dir)):
            with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.start', Mock()) as start:
                indir = tp.session.tecplot_install_directory()
                exdir = tp.session.tecplot_examples_directory()
                self.assertEqual(indir.parts[1], 'path')
                self.assertEqual(indir.parts[:4], exdir.parts[:4])
                self.assertEqual(start.call_count, 2)

            with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.start', Mock()) as start:
                with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.connected',
                           PropertyMock(return_value=True)):
                    indir = tp.session.tecplot_install_directory()
                    exdir = tp.session.tecplot_examples_directory()
                    self.assertEqual(indir.parts[1], 'path')
                    self.assertEqual(indir.parts[:4], exdir.parts[:4])
                    self.assertEqual(start.call_count, 0)

        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.tecsdkhome',
                   PropertyMock(return_value=None)):
            self.assertIsNone(tp.session.tecplot_install_directory())
            self.assertIsNone(tp.session.tecplot_examples_directory())

    def test_stop(self):
        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.stop',
                   Mock(return_value=True)) as stop:
            self.assertIsNone(tp.session.stop())
            stop.assert_called_once()

    def test_acquire_license(self):
        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.acquire_license',
                   Mock(return_value=True)) as acquire:
            self.assertIsNone(tp.acquire_license())
            acquire.assert_called_once()

    def test_release_license(self):
        with patch(
                'tecplot.tecutil.tecutil_connector.TecUtilConnector.release_license',
                Mock(return_value=True)) as release:
            self.assertIsNone(tp.release_license())
            release.assert_called_once()

    @skip_if_connected
    def test_roaming(self):
        def LicenseStartRoaming(ndays):
            return True
        _LicenseStartRoaming = tp.tecutil._tecutil_connector.handle.LicenseStartRoaming
        tp.tecutil._tecutil_connector.handle.LicenseStartRoaming = LicenseStartRoaming
        try:
            warnings.simplefilter('ignore')
            with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.connected',
                       PropertyMock(return_value=True)):
                with self.assertRaises(TecplotLogicError):
                    tp.session.start_roaming(10)
                with self.assertRaises(TecplotLogicError):
                    tp.session.stop_roaming()

            tp.session.start_roaming(10)
            tp.session.stop_roaming()
        finally:
            tp.tecutil._tecutil_connector.handle.LicenseStartRoaming = _LicenseStartRoaming

    def test_expiration_date(self):
        if tp.tecutil._tecutil_connector.handle is not None:
            expdate = None
            def LicenseExpirationDate():
                return expdate
            _LicenseExpirationDate = tp.tecutil._tecutil_connector.handle.LicenseExpirationDate
            tp.tecutil._tecutil_connector.handle.LicenseExpirationDate = LicenseExpirationDate
            try:
                expdate = b'2020-01-01'
                self.assertEqual(tp.session.license_expiration(), datetime.date(year=2020, month=1, day=1))
                expdate = b'unknown'
                self.assertIsNone(tp.session.license_expiration())
            finally:
                tp.tecutil._tecutil_connector.handle.LicenseExpirationDate = _LicenseExpirationDate

    @skip_if_connected
    def test_connect(self):
        connected_fn = 'tecplot.tecutil.tecutil_connector.TecUtilConnector.connected'

        if tp.tecutil._tecutil_connector.client is None:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                from tecplot.tecutil.tecutil_client import TecUtilClient
            tp.tecutil._tecutil_connector.client = TecUtilClient()
            is_listening_fn = 'tecplot.tecutil.tecutil_client.TecUtilClient.is_server_listening'
        else:
            is_listening_fn = 'tecplot.tecutil.tecutil_client.TecUtilClient.is_server_listening'

        with patch(connected_fn, PropertyMock(return_value=False)):
            self.assertFalse(tp.session.connected())

        with patch(connected_fn, PropertyMock(return_value=True)):
            with patch(is_listening_fn, Mock(return_value=True)):
                self.assertTrue(tp.session.connected())
            with patch(is_listening_fn, Mock(return_value=False)):
                self.assertFalse(tp.session.connected())

        if not tp.session.connected():
            with self.assertRaises(TecplotTimeoutError):
                tp.session.connect(port=1, timeout=0.1, quiet=True)

        with patch('tecplot.tecutil.tecutil_connector.TecUtilConnector.disconnect',
                   Mock(return_value=None)):
            self.assertIsNone(tp.session.disconnect())

    def test_suspend(self):
        tp.new_layout()
        with tp.session.suspend():
            with tp.session.suspend():
                ds = tp.active_frame().create_dataset('D', ['x', 'y'])
                zn = ds.add_ordered_zone('Z', (1,))
        self.assertEqual(zn.values(0).shape, (1,))

    def test_suspend_enter_exit(self):
        tp.new_layout()
        try:
            tp.session.suspend_enter()
            ds = tp.active_frame().create_dataset('D', ['x', 'y'])
            zn = ds.add_ordered_zone('Z', (1,))
        finally:
            tp.session.suspend_exit()
        self.assertEqual(zn.values(0).shape, (1,))

    @skip_if_connected
    def test_disconnect(self):
        class Client(Mock):
            def quit():
                pass
        with patch('tecplot.session.session.connected', Mock(return_value=True)) as conn:
            with patch.object(tp.session.session, '_tecutil_connector') as TUConnMock:
                TUConnMock.client = Client
                def disconnect(self):
                    pass
                TUConnMock.disconnect = disconnect
                with patch.object(TUConnMock, 'disconnect') as disconn:
                    with patch.object(Client, 'quit') as quit:
                        tp.session.disconnect()
                        self.assertGreater(conn.call_count, 0)
                        self.assertGreater(disconn.call_count, 0)
                        quit.assert_not_called()
                        conn.reset_mock()
                        disconn.reset_mock()

                        tp.session.disconnect(True)
                        self.assertGreater(conn.call_count, 0)
                        self.assertGreater(disconn.call_count, 0)
                        self.assertGreater(quit.call_count, 0)
                        conn.reset_mock()
                        disconn.reset_mock()

                        tp.session.disconnect(quit=True)
                        self.assertGreater(conn.call_count, 0)
                        self.assertGreater(disconn.call_count, 0)
                        self.assertGreater(quit.call_count, 0)

    def test_atexit(self):
        try:
            connected = tp.tecutil._tecutil_connector.connected
            if connected:
                atexit.unregister(tp.tecutil._tecutil_connector.client.disconnect)
            with patch.object(tp.tecutil.tecutil_connector._tecutil_connector, 'stop') as stop:
                atexit._run_exitfuncs()
                self.assertEqual(stop.call_count, 1)
        finally:
            if connected:
                atexit.register(tp.tecutil._tecutil_connector.client.disconnect)

    def test_redraw(self):
        tp.new_layout()
        self.filename, dataset = sample_data('10x10x10')
        tp.session.redraw()  # just exercising the method here


if __name__ == '__main__':
    import test
    test.main()
