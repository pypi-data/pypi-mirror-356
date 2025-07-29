import os
import tempfile
import unittest
from unittest.mock import *

import filetype

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

from ..sample_data import sample_data
from .. import (
    patch_tecutil,
    closed_tempfile,
    skip_if_sdk_version_before,
    mocked_sdk_version,
)
from .test_animation import isvideo


class TestTimeAnimation(unittest.TestCase):
    _OPTS = dict(width=32, supersample=1)

    def setUp(self):
        tp.new_layout()
        self.filename, _ = sample_data('3x3x3_3zones_time')
        tp.active_frame().plot(PlotType.Cartesian3D).activate()

    def tearDown(self):
        tp.new_layout()
        os.remove(self.filename)

    # Since 2021.2, AVI is generated with ffmpeg and additionally controlled via
    # the ffmpeg parameter, format_options.
    @skip_if_sdk_version_before(2021, 2)
    def test_animation_avi(self):
        opts = TestTimeAnimation._OPTS.copy()
        opts.update(timestep_step=None, format_options='-vcodec mjpeg -q:v 1')
        with closed_tempfile('.avi') as fname:
            tp.export.save_time_animation_avi(fname, **opts)
            self.assertTrue(isvideo(self, fname))

    def test_animation_mpeg4(self):
        opts = TestTimeAnimation._OPTS.copy()
        opts.update(
            start_time=1,
            end_time=2,
            timestep_step=1,
        )
        with closed_tempfile('.mp4') as fname:
            tp.export.save_time_animation_mpeg4(fname, **opts)
            self.assertTrue(isvideo(self, fname))

    def test_animation_mpeg4_byext(self):
        with closed_tempfile('.mp4') as fname:
            tp.export.save_time_animation(fname, **TestTimeAnimation._OPTS)
            self.assertTrue(isvideo(self, fname))

    def test_animation_wmv(self):
        with closed_tempfile('.wmv') as fname:
            tp.export.save_time_animation_wmv(fname, **TestTimeAnimation._OPTS)
            self.assertTrue(isvideo(self, fname))

    def test_animation_raster_metafile(self):
        with closed_tempfile('.rm') as fname:
            tp.export.save_time_animation_raster_metafile(
                fname, **TestTimeAnimation._OPTS
            )
            # no good way to determine video format for
            # raster metafiles so just check the file size
            with open(fname, 'rb') as fin:
                self.assertGreater(len(fin.read()), 800)

    def test_animation_flash(self):
        with closed_tempfile('.flv') as fname:
            opts = TestTimeAnimation._OPTS.copy()
            opts.update(
                compression=FlashCompressionType.SmallestSize,
                image_type=FlashImageType.Color256,
            )
            tp.export.save_time_animation_flash(fname, **opts)
            self.assertTrue(isvideo(self, fname))

    def test_failures(self):
        with closed_tempfile('.mp4') as fname:
            with patch_tecutil('AnimateTimeX', return_value=False):
                with self.assertRaises(TecplotSystemError):
                    tp.export.save_time_animation_mpeg4(fname)

    def test_animation_bmp(self):
        opts = TestTimeAnimation._OPTS.copy()
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                tp.export.save_time_animation_bmp('img.bmp', **opts)
                self.assertFalse(os.path.exists('img.bmp'))
                self.assertTrue(os.path.exists('img_000001.bmp'))
                self.assertTrue(os.path.exists('img_000002.bmp'))
                self.assertTrue(os.path.exists('img_000003.bmp'))
                self.assertFalse(os.path.exists('img_000004.bmp'))
                self.assertEqual(
                    filetype.guess('img_000001.bmp').mime, 'image/bmp'
                )
            finally:
                os.chdir(cwd)

    def test_animation_jpeg(self):
        opts = TestTimeAnimation._OPTS.copy()
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                tp.export.save_time_animation_jpeg('img.jpeg', **opts)
                self.assertFalse(os.path.exists('img.jpeg'))
                self.assertTrue(os.path.exists('img_000001.jpeg'))
                self.assertTrue(os.path.exists('img_000002.jpeg'))
                self.assertTrue(os.path.exists('img_000003.jpeg'))
                self.assertFalse(os.path.exists('img_000004.jpeg'))
                self.assertEqual(
                    filetype.guess('img_000001.jpeg').mime, 'image/jpeg'
                )
            finally:
                os.chdir(cwd)

    def test_animation_png(self):
        opts = TestTimeAnimation._OPTS.copy()
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                tp.export.save_time_animation_png('img.png', **opts)
                self.assertFalse(os.path.exists('img.png'))
                self.assertTrue(os.path.exists('img_000001.png'))
                self.assertTrue(os.path.exists('img_000002.png'))
                self.assertTrue(os.path.exists('img_000003.png'))
                self.assertFalse(os.path.exists('img_000004.png'))
                self.assertEqual(
                    filetype.guess('img_000001.png').mime, 'image/png'
                )
            finally:
                os.chdir(cwd)

    def test_animation_tiff(self):
        opts = TestTimeAnimation._OPTS.copy()
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                tp.export.save_time_animation_tiff('img.tiff', **opts)
                self.assertFalse(os.path.exists('img.tiff'))
                self.assertTrue(os.path.exists('img_000001.tiff'))
                self.assertTrue(os.path.exists('img_000002.tiff'))
                self.assertTrue(os.path.exists('img_000003.tiff'))
                self.assertFalse(os.path.exists('img_000004.tiff'))
                self.assertEqual(
                    filetype.guess('img_000001.tiff').mime, 'image/tiff'
                )
            finally:
                os.chdir(cwd)


if __name__ == '__main__':
    import test

    test.main()
