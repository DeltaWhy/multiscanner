from __future__ import division, absolute_import, print_function, unicode_literals
import sys
import os
# Makes sure we use the multiscanner in ../
CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(CWD))
import multiscanner

sys.path.append(os.path.join(CWD, '..', 'libs'))
import common

class _runmulti_tests(object):
    @classmethod
    def setup_class(cls):
        cls.real_mod_dir = multiscanner.MODULEDIR
        multiscanner.MODULEDIR = os.path.join(CWD, "modules")
        cls.filelist = common.parseDir(os.path.join(CWD, 'files'))
        multiscanner.CONFIG = '.tmpfile.ini'

    @classmethod
    def teardown_class(cls):
        multiscanner.MODULEDIR = cls.real_mod_dir


class Test_multiscan(_runmulti_tests):
    def setup(self):
        self.result = multiscanner.multiscan(self.filelist, recursive=False, configregen=False, configfile='.tmpfile.ini')
        self.report = multiscanner.parse_reports(self.result, includeMetadata=False, python=True)
        self.report_m = multiscanner.parse_reports(self.result, includeMetadata=True, python=True)

    def teardown(self):
        os.remove('.tmpfile.ini')

    def test_multiscan_results(self):
        for f in self.filelist:
            assert f in self.report
            assert f in self.report_m['Files']

class Test_main(_runmulti_tests):
    def setup(self):
        sys.argv = ['']

    def teardown(self):
        try:
            os.remove('.tmpfile.ini')
            os.remove('tmp_report.json')
        except:
            pass

    def test_basic_main(self):
        sys.argv = ['-z', '-j', 'tmp_report.json']
        sys.argv.extend(self.filelist)
        multiscanner._main()
