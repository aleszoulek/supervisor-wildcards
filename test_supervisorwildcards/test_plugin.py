import re
from nose import tools
from os.path import dirname, join
from subprocess import PIPE, Popen
from unittest import TestCase



config_file = join(dirname(__file__), 'supervisord.conf')

class TestPlugin(TestCase):

    def setUp(self):
        self._supervisorctl('start all')

    def _supervisorctl(self, cmd):
        print cmd
        out = Popen('supervisorctl --configuration="%s" %s' % (config_file, cmd), shell=True, stdout=PIPE).stdout.read()
        print out
        return out

    def assert_status(self, expected):
        status = dict(
            re.findall('^([^ ]+) +([^ ]+) .*', line)[0]
            for line
            in self._supervisorctl('status').split('\n')
            if line
        )
        tools.assert_equals(
            expected,
            status
        )

    def test_stopall(self):
        self._supervisorctl("mstop '*'")
        self.assert_status({
            'colors:red': 'STOPPED',
            'colors:green': 'STOPPED',
            'one': 'STOPPED',
        })

    def test_match_group(self):
        self._supervisorctl("mstop 'r*'")
        self.assert_status({
            'colors:red': 'STOPPED',
            'colors:green': 'RUNNING',
            'one': 'RUNNING',
        })
