import re
import unittest

import tecplot as tp

from test import skip_if_connected

class TestRecording(unittest.TestCase):
    @skip_if_connected
    def setUp(self):
        tp.new_layout()

    def check_mcr_file_header(self, file_header):
        first_line = file_header.split('\n')[0]
        self.assertIsNotNone(re.match(r'^#!MC\s\d\d\d\d\s*', first_line))

    def test_play_macro(self):
        with tp.tecutil.temporary_closed_file(suffix='.mcr') as fmcr:
            with tp.tecutil.temporary_closed_file(suffix='.py') as fpy:
                # No need to actually record any macro commands since we're
                # going to be checking for the filename.
                tp.tecutil._tecutil_connector.macro_record_start(fmcr)
                tp.tecutil._tecutil_connector.macro_record_end()

                tp.tecutil._tecutil_connector.macro_record_start(fpy)
                # The closest way to simulate the user selecting
                # Macro/Play Macro is to record an macro.execute_file() command,
                # which will end up in Action_RunFile(), which will record
                # macro.execute_file()
                tp.macro.execute_file(fmcr)
                tp.tecutil._tecutil_connector.macro_record_end()

                file_contents = fpy.read_text()
                final_name = str(fmcr.resolve()).replace('\\', '\\\\')
                self.assertIn(f"macro.execute_file('{final_name}')",
                              file_contents)

    def test_that_a_real_pytecplot_file_is_recorded(self):
        with tp.tecutil.temporary_closed_file(suffix='.py') as ftmp:
            with tp.macro.record(ftmp):
                pass
            file_contents = ftmp.read_text()
        self.assertIn('import tecplot', file_contents)

    def test_without_raw_data(self):
        with tp.macro.record(header='#!MC 1410\n') as buf:
            tp.macro.execute_command('''\
                $!CREATERECTANGULARZONE
                      IMAX = 10
                      JMAX = 10
                      KMAX = 10
                      X1 = 0
                      Y1 = 0
                      Z1 = 0
                      X2 = 1
                      Y2 = 1
                      Z2 = 1
                      XVAR = 1
                      YVAR = 2
                      ZVAR = 3''')
        file_contents = buf.getvalue()
        self.check_mcr_file_header(file_contents)
        self.assertIn('$!CREATERECTANGULARZONE', file_contents.upper())

    def test_with_raw_data(self):
        expected_contents ='''
$!ATTACHGEOM
  ANCHORPOS
    {
    X = 0.2787855444785277
    Y = 0.8375070552147239
    }
  RAWDATA
1
6
0 0
0.0122711658478 -0.561405837536
0.26843175292 -0.475507676601
0.427956908941 -0.0828303694725
0.233152151108 -0.0306779146194
0.665710747242 -0.549134671688'''
        with tp.macro.record(header='#!MC 1410\n') as buf:
            tp.macro.execute_command(expected_contents)
        file_contents = buf.getvalue()
        self.check_mcr_file_header(file_contents)
        self.assertIn(expected_contents, re.sub(r'\s*\n', r'\n', file_contents.upper()))


if __name__ == '__main__':
    import test
    test.main()
