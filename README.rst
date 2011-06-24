====================
Supervisor wildcards
====================

Description
===========

Adds ``mstop``, ``mstart`` and ``mrestart`` commands to Supervisor_. Those commands works exacatly the same way as ``stop``, ``start`` and ``restart`` respectively, except they support process name wildcarding.

In some usecases you can use groups support in Supervisor_, but it doesn't allow you to have one process in multiple groups. That's when wildcarding can be really useful.

Example
=======

::

  supervisor> status
  celery-a                                RUNNING    pid 15085, uptime 0:00:11
  celery-b                                RUNNING    pid 15086, uptime 0:00:12
  gunicorn-a                              RUNNING    pid 14151, uptime 0:05:18
  gunicorn-b                              RUNNING    pid 14237, uptime 0:04:45
  supervisor> mstop *-a
  celery-a: stopped
  gunicorn-a: stopped
  supervisor>

Installation
============

::

  pip install supervisor-wildcards

And then add into your supervisor.conf:

::

  [ctlplugin:wildcards]
  supervisor.ctl_factory = supervisorwildcards.controllerplugin:make_wildcards_controllerplugin




.. _Supervisor: http://supervisord.org/
