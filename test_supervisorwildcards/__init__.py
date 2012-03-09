from os.path import dirname, join
import subprocess
import time

_supervisor_processes = []


def setUp():
    if not _supervisor_processes:
        _supervisor_processes.append(
            subprocess.Popen(['supervisord', '-n', '--configuration', join(dirname(__file__), 'supervisord.conf')])
        )
        time.sleep(3)

def tearDown():
    for process in _supervisor_processes:
        process.kill()
    for process in _supervisor_processes:
        process.wait()
