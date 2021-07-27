from threading import Thread
import fnmatch

from supervisor.supervisorctl import ControllerPluginBase

class WildCardsControllerPlugin(ControllerPluginBase):
    name = 'wildcards'

    def __init__(self, controller, **config):
        self.ctl = controller
        self.match_group = bool(int(config.get('match_group', '0')))

    def _match_process(self, process, pattern):
        name = process['name']
        if self.match_group:
            name = "%s:%s" % (process['group'], process['name'])
        return fnmatch.fnmatch(name, pattern)

    def _expand_wildcards(self, arg, command, offset=0):
        patterns = arg.split()
        if offset:
            command = '%s %s' % (command, ' '.join(patterns[0:offset]))
            patterns = patterns[offset:]
        supervisor = self.ctl.get_supervisor()
        if 'all' in patterns:
            # match any process name
            patterns = ['*']

        threads = []
        for process in supervisor.getAllProcessInfo():
            for pattern in patterns:
                if self._match_process(process, pattern):
                    t = Thread(target=self.ctl.onecmd, args=('%s %s:%s' % (command, process['group'], process['name']), ))
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
    def do_mstatus(self, arg):
        self._expand_wildcards(arg, command='status')
    def do_mpid(self, arg):
        self._expand_wildcards(arg, command='pid')
    def do_msignal(self, arg):
        # signal <signal name> <patterns>
        self._expand_wildcards(arg, command='signal', offset=1)

    def help_mstop(self):
        return self._wrap_help('stop')
    def help_mstart(self):
        return self._wrap_help('start')
    def help_mrestart(self):
        return self._wrap_help('restart')
    def help_mstatus(self):
        return self._wrap_help('status')
    def help_mpid(self):
        return self._wrap_help('pid')
    def help_msignal(self):
        return self._wrap_help('signal')



def make_wildcards_controllerplugin(controller, **config):
    return WildCardsControllerPlugin(controller, **config)
