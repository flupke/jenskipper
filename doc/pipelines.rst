Defining jobs pipelines
=======================

Sometimes you want to chain multiple jobs together. For example you might have
a deploy job that must only be run after integration and unit tests succeeded.

In jenkins, you assemble such pipelines by editing the jobs configurations,
hooking jobs to each other on by one. This process is cumbersome, and it can be
hard to visualize the whole pipeline.

Jenskipper solves this by separating the pipelines definitions from the jobs.
Pipelines are defined in the top-level ``pipelines`` text file. Here is the
representation of the example above::

    unit-tests > integration-tests > deployment

By default the jobs chain is interrupted if one of the jobs fail. If you need
to continue running jobs in the pipeline after a failure or an unstable result,
use the ``~>`` and ``?>`` operators respectively::

    unit-tests > integration-tests ~> deployment

Here the ``deployment`` job will be executed even if the ``integration-tests``
fails, but nothing will run if ``unit-tests`` fails.

A job may also trigger more than one job::

    A > B > D
    A > C

Or a job can be triggered by multiple jobs::

    A > C
    B > C

In this last example, ``C`` will be triggered if ``A`` *or* ``B`` finishes
successfully.
