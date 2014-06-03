import re
from nose import tools
from os.path import dirname, join
from subprocess import PIPE, Popen
from unittest import TestCase



CONFIG_FILE = join(dirname(__file__), 'supervisord.conf')
CONFIG_FILE_MATCH_GROUP = join(dirname(__file__), 'supervisord_match_group.conf')

class TestPlugin(TestCase):

    def setUp(self):
        self._supervisorctl('start all')

    def _supervisorctl(self, cmd, config_file=CONFIG_FILE):
        c = 'supervisorctl --configuration="%s" %s' % (config_file, cmd)
        out = Popen(c, shell=True, stdout=PIPE).stdout.read().decode("utf-8")
        print(out)
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

    def test_match_group_off(self):
        self._supervisorctl("mstop 'r*'")
        self.assert_status({
            'colors:red': 'STOPPED',
            'colors:green': 'RUNNING',
            'one': 'RUNNING',
        })

    def test_match_group_on(self):
        self._supervisorctl("mstop 'col*'", config_file=CONFIG_FILE_MATCH_GROUP)
        self.assert_status({
            'colors:red': 'STOPPED',
            'colors:green': 'STOPPED',
            'one': 'RUNNING',
        })
