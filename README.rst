====================
Supervisor wildcards
====================

Description
===========

Adds ``mstop``, ``mstart`` and ``mrestart`` commands to Supervisor_. Those commands works similar to ``stop``, ``start`` and ``restart`` respectively, but they:

* add support for process name wildcarding,
* sends the start/stop/restart signal in parallel (which makes the batch commands finish faster).

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

Configuration
=============

::

  [ctlplugin:wildcards]
  supervisor.ctl_factory = supervisorwildcards.controllerplugin:make_wildcards_controllerplugin
  match_group = 1

By default, supervisorwildcards plugin match the wildcards just against process name (not group). Setting match_group = 1 will try to match the pattern against "group_name:process_name" instead.

Changelog
=========

 * 0.1.3

   * ``all`` parameter expands to ``*``
   * Added ``match_group`` config option

 * 0.1.2

   * Fixed matching processes that are assigned to a group

 * 0.1.1

   * Commands are run in parallel (Thanks, Honza Kral)

 * 0.1.0

   * Simple support for ``mstop``, ``mstart``, ``mrestart``



.. _Supervisor: http://supervisord.org/
