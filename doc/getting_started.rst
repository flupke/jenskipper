Getting Started
===============

Install jenskipper::

    $ pip install jenskipper

Import your jobs::

    $ jenskipper import http://my.jenkins.server/ jenkins

This will import all jobs from ``http://my.jenkins.server/`` in the ``jenkins``
directory::

    jenkins
    |
    +- jobs.yaml
    |
    +- default_context.yaml
    |
    +- pipelines.txt
    |
    `- templates
       |
       +- foo-tests.xml
       |
       `- bar-tests.xml

You can now have a look at the XML files in the ``templates`` directory, and
modify them. Once you're done with your modifications, you can push all of them
at once to the server::

    $ cd jenkins
    $ jenskipper push

You can also push only some jobs by specifying their names on the command
line::

    $ jenskipper push bar-tests

If you want to pull new jobs from the server::

    $ jenskipper fetch-new

Note that you can't update existing jobs from the server. This is wanted,
jenskipper operations are meant to be one way: after the initial import,
Jenkins jobs are only updated from the jenskipper repository.

Overview of the imported directory
----------------------------------

jobs.yaml
    The list of jobs that are managed by jenskipper; see :doc:`jobs`.

default_context.yaml
    The variables available to all templates.

pipelines.txt
    A high-level view of how jobs are chained together; see :doc:`pipelines`.

templates/
    The jobs templates directory.
