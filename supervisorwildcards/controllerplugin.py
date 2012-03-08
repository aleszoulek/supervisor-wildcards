from threading import Thread
import fnmatch

from supervisor.supervisorctl import ControllerPluginBase

class WildCardsControllerPlugin(ControllerPluginBase):
    name = 'wildcards'

    def __init__(self, controller, **config):
        self.ctl = controller

    def _expand_wildcards(self, arg, command):
        patterns = arg.split()
        supervisorProcesses = self.ctl.get_supervisor().getAllProcessInfo()
        matchedProcesses = []

        if 'all' in patterns:
            for supervisorProcess in supervisorProcesses:
                matchedProcesses.append(supervisorProcess['group'] + ':' + supervisorProcess['name'])
        else:
            for supervisorProcess in supervisorProcesses:
                for pattern in patterns:
                    if fnmatch.fnmatch(supervisorProcess['group'], pattern):
                        matchedProcesses.append(supervisorProcess['group'] + ':' + supervisorProcess['name'])

        threads = []

        for matchedProcess in set(matchedProcesses):
            t = Thread(target=self.ctl.onecmd, args=('%s %s' % (command, matchedProcess), ))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        if not threads:
            self.ctl.output('No process matched given expression.')

    def _wrap_help(self, command):
        self.ctl.output('The same as %s, but accepts wildcard expressions to match the process name.' % command)
        self.ctl.output('m%s a* - %ss all processes begining with "a".' % (command, command))


    def do_mstop(self, arg):
        self._expand_wildcards(arg, command='stop')
    def do_mstart(self, arg):
        self._expand_wildcards(arg, command='start')
    def do_mrestart(self, arg):
        self._expand_wildcards(arg, command='restart')

    def help_mstop(self):
        return self._wrap_help('stop')
    def help_mstart(self):
        return self._wrap_help('start')
    def help_mrestart(self):
        return self._wrap_help('restart')




def make_wildcards_controllerplugin(controller, **config):
    return WildCardsControllerPlugin(controller, **config)
