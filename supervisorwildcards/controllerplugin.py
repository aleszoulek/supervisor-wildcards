import fnmatch

from supervisor.supervisorctl import ControllerPluginBase

class WildCardsControllerPlugin(ControllerPluginBase):
    name = 'wildcards'

    def __init__(self, controller, **config):
        self.ctl = controller

    def do_mstop(self, arg):
        patterns = arg.split()
        supervisor = self.ctl.get_supervisor()
        matched = False
        if 'all' in patterns:
            self.ctl.onecmd('stop all')
        for process in supervisor.getAllProcessInfo():
            for pattern in patterns:
                if fnmatch.fnmatch(process['name'], pattern):
                    self.ctl.onecmd('stop %s' % process['name'])
                    matched = True
        if not matched:
            self.ctl.output('No process matched given expression.')

    def help_mstop(self):
        self.ctl.output('The same as stop, but accepts wildcard expressions to match the process name.')
        self.ctl.output('mstop a* - stops all processes begining with "a".')




def make_wildcards_controllerplugin(controller, **config):
    return WildCardsControllerPlugin(controller, **config)
