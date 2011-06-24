from setuptools import setup
from os import path


VERSION = (0, 1, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

long_description = ''
try:
    f = open(path.join(path.dirname(__file__), 'README.rst'))
    long_description = f.read().strip()
    f.close()
except:
    pass


setup(
    name = 'supervisor-wildcards',
    description = "Implemenents start/stop/restart commands with wildcard support for Supervisor",
    url = "http://github.com/aleszoulek/supervisor-wildcards",
    long_description = long_description,
    version = __versionstr__,
    author = "Ales Zoulek",
    author_email = "ales.zoulek@gmail.com",
    license = "BSD",
    packages = ['supervisorwildcards'],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
    ]
)


